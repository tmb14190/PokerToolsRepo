'''
Created on 7 Oct 2020

@author: jackm
'''
import BrosHH.BrosInterface as BI
from ImageHandHistory.save_as_bytes import save_as_bytes as SAB
from PIL import Image
import pytesseract
import re
from BrosHH.Player import Player
import numpy as np
import cv2
import glob
from numpy.distutils.misc_util import blue_text
import time

acceptable_actions = ["Call", "Raise", "Bet", "Check", "Fold", "BB", "SB", "All In", "New"]

def setupNewHand(bu):
    
    img = BI.getImage()
    
    players = []
    
    # set up list with only players who were dealt cards
    index = 0
    for i in range(1, 7):
        p = Player(i)
        if (p.playing):
            players.append(p)
            if (bu == i):
                index = len(players) - 1
    
    # TESTING IDEA - maybe check here to make sure index initialised for some form of testing
    
    # Set the order with bb at end of list
    if (len(players) > 2):
        bb = index + 2
    else:
        bb = index + 1
    players[:] = players[bb % (len(players)-1):] + players[:bb % (len(players)-1)]

    # going backwards in list (aka starting with bb) ahh the table position for each player
    sixmax = ["BB", "SB", "BU", "CO", "HJ", "UTG"]
    counter = 0
    for p in reversed(players):
        p.setPosition(sixmax(counter))
        counter+=1
    
    return players
    

def initPlayer(pos, img):
    
    # check seat filled 
    seats = findCardBacks(img)
        
    pass

def imageProcess(img):

    width, height = img.size
    
    largeImg = img.resize((int(width*5), int(height*5)), 1)
    
    
    processed = Image.eval(largeImg, lambda x: 0 if x >= 150 else 255)

    return processed

def imgProcessBoard(img):
    
    img = img.convert('L')
    
    width, height = img.size
    
    largeImg = img.resize((int(width*3), int(height*3)), 1)
    
    
    processed = Image.eval(largeImg, lambda x: 0 if x <= 220 else 255)
    
    #processed.show()

    return processed

def readText(img):

    pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract'
    
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 7')
    
    return text

def readCard(img):
    
    pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract'
    
    text = pytesseract.image_to_string(img, lang='eng', config='-c tessedit_char_whitelist=023456789JQKA --psm 10')
    
    return text
'''
returns 1-6 for where bu is
Might be an issue where button on empty seats is in a different position
'''
def findButton(im):
    
    width, height = im.size 
    
    dict = {1:(width*0.212, height*0.657, width*0.213, height*0.658), 2:(width*0.276, height*0.389, width*0.278, height*0.39), 3:(width*0.384, height*0.238, width*0.386, height*0.239), 4:(width*0.67, height*0.384, width*0.672, height*0.385), 5:(width*0.712, height*0.67, width*0.714, height*0.671), 6:(width*0.359, height*0.78, width*0.361, height*0.781)}
    
    for i in range(1, 7):
        bu = im.crop(dict[i])
        a = np.array(bu)
        if (a[0][0][0] == 255 and a[0][0][1] == 255 and a[0][0][2] == 255):
            return (i)
     
    return (0)
'''
finds if opponent has card backs showing on screen by checking specific pixel
'''
def findCardBacks():
    
    im = BI.getImage()
    width, height = im.size 
    
    p = []
    p.append(im.crop((width*0.065, height*0.59, width*0.067, height*0.591)))
    p.append(im.crop((width*0.12, height*0.32, width*0.122, height*0.321)))
    p.append(im.crop((width*0.537, height*0.165, width*0.539, height*0.166)))
    p.append(im.crop((width*0.82, height*0.32, width*0.822, height*0.321)))
    p.append(im.crop((width*0.878, height*0.59, width*0.88, height*0.591)))
    
    output = []
    for a in p:
        #a.show()
        ar = np.array(a)
        if (ar[0][0][0] == 66 and ar[0][0][1] == 125 and ar[0][0][2] == 164):
            output.append(True)
        else:
            output.append(False)

    us = im.crop((width*0.563, height*0.772, width*0.564, height*0.773))
    a = np.array(us)
    if (a[0][0][0] == 230 and a[0][0][1] == 235 and a[0][0][2] == 230):
        output.append(True)
    else:
        output.append(False)
        
    return output
            
    
    
def matchBoardCards(img):
    
    dict = {2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"T", 11:"T", 12:"J", 13:"Q", 14:"K", 15:"A"}
    
    img = img.convert('L')
    
    templates = []
    for i in range(2, 16):
        templates.append(cv2.imread("card_imgs/{a}.png".format(a = i)))
    
    card = np.array(img)
    
    out = []
    
    for t in templates:
        grey = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(card, grey, cv2.TM_CCOEFF_NORMED)
        if (res.max() == 0):
            return 0
        out.append(res.max())
    
    return str(dict[out.index(max(out))+2])

def getSuitFromColour(img):
    
    def myLoop(imgNP):
        for x in imgNP:
            for y in x:
                if (y[0] < 100 and y[1] < 100 and y[2] > 100):
                    return "d"
                if (y[0] < 100 and y[1] > 100 and y[2] < 100):
                    suit = "c"
                    return suit
                if (y[0] > 100 and y[1] < 100 and y[2] < 100):
                    suit = "h"
                    return suit
        return "s"
    
    imgNP = np.array(img)
    
    suit = myLoop(imgNP)
    # if contains (25, 133, 16) then club
    # if (33, 32, 33) spade
    # if (173, 0, 0) then heart
    # if (0, 78, 180) then blue
    return suit

# returns immediate pot size, and pot size at start of betting round post
def getPot():
    
    i = 0
    work = False
    
    while (i<3 and work == False):
        try:
            im = BI.getImage()
    
            width, height = im.size 
            potIm = im.crop((width*0.403, height*0.34, width*0.537, height*0.36))
            potStrt = im.crop((width*0.438, height*0.3, width*0.537, height*0.32))
            
            potIm = imageProcess(potIm)
            potStrt = imageProcess(potStrt)
            
            potImTxt = re.sub("[^0123456789.]", "", readText(potIm))
            potStrtTxt = re.sub("[^0123456789.]", "", readText(potStrt))
            
            outS = 0
            outI = 0
            
            outS = float(potStrtTxt)
            outI = float(potImTxt)
            work = True
        except:
            print ("Pot not read as number - trying again")
            time.sleep(0.1)
            i+=1
    if (i >= 3):
        print ("Pot read timed out - assistance capabilities diminished")
        
    return outS, outI

'''
returns array 2 strings, empty list if no cards visible
'''
def getHoleCards():
    
    im = BI.getImage()
    width, height = im.size 
    left_img = im.crop((width*0.563, height*0.772, width*0.589, height*0.792))
    right_img = im.crop((width*0.619, height*0.769, width*0.654, height*0.789))
    
    left = imgProcessBoard(left_img)
    if (left == 0):
        return []
    right = imgProcessBoard(right_img)
    suitL = getSuitFromColour(left_img)
    suitR = getSuitFromColour(right_img)
    l = matchBoardCards(left)
    r = matchBoardCards(right)
    if (l != 0 and r != 0):
        outleft = l + suitL
        outright = r + suitR
        return outleft, outright
    else:
        return 0, 0

def weRaising(im):
    
    width, height = im.size 
    
    p = im.crop((width*0.08, height*0.95, width*0.082, height*0.951))
    
    a = np.array(p)
    
    if (a[0][0][0] == 0 and a[0][0][1] == 123 and a[0][0][2] == 189):
        return True
    
    return False

'''
return 0 pre, 1 flop, 2 turn, 3 river
calculated using white pixels on showing cards
'''
def getStreet(im):
    
    width, height = im.size 
    flop = im.crop((width*0.25, height*0.41, width*0.252, height*0.411))
    turn = im.crop((width*0.57, height*0.41, width*0.572, height*0.411))
    river = im.crop((width*0.69, height*0.41, width*0.692, height*0.411))
    
    a = np.array(flop)
    b = np.array(turn)
    c = np.array(river)
    
    street = 0
    
    if (a[0][0][0] == 230 and a[0][0][1] == 235 and a[0][0][2] == 230):
        street = 1
    if (b[0][0][0] == 230 and b[0][0][1] == 235 and b[0][0][2] == 230):
        street = 2
    if (c[0][0][0] == 230 and c[0][0][1] == 235 and c[0][0][2] == 230):
        street = 3
    
    return street

'''
returns list of each board card as string e.g. ["Qd", "Ah", "4h"]
'''
def getBoard():
    
    im = BI.getImage()
    
    width, height = im.size 
    card_imgs = []
    card_imgs.append(im.crop((width*0.203, height*0.403, width*0.24, height*0.423)))
    card_imgs.append(im.crop((width*0.312, height*0.403, width*0.35, height*0.423)))
    card_imgs.append(im.crop((width*0.42, height*0.403, width*0.455, height*0.423)))
    card_imgs.append(im.crop((width*0.528, height*0.403, width*0.563, height*0.423)))
    card_imgs.append(im.crop((width*0.64, height*0.403, width*0.675, height*0.423)))
    
    suits = []
    cards_proc = []
    for c in card_imgs:
        cards_proc.append(imgProcessBoard(c))
        suits.append(getSuitFromColour(c))
    
    output = []
    
    for i in range (0, len(cards_proc)):
        number = matchBoardCards(cards_proc[i])
        if (number != 0):
            output.append(number + suits[i])
        
    
    return output

def actionByColour(pixel):
    
    p = np.array(pixel)[0][0]
    
    #print (p)
    
    # fold = 90 85 90
    # raise = 229 174  99
    # call = 41 170  58
    # check, sb, bb = 25 138 206
    # all in = 206 0 206 
    # bet = 222 142 33 
    
    if (p[0] == 90 and p[1] == 85 and p[2] == 90):
        return "Fold"
    if (p[0] == 25 and p[1] == 138 and p[2] == 206):
        return "Check"
    if (p[0] == 41 and p[1] == 170 and p[2] == 58):
        return "Call"
    if (p[0] == 222 and p[1] == 142 and p[2] == 33):
        return "Bet"
    if (p[0] == 206 and p[1] == 0 and p[2] == 206):
        return "All In"
    
    return None

def getActionBySeat(seat, img):
    width, height = img.size
    dict = {1:(width*0.132, height*0.528, width*0.133, height*0.529), 2:(width*0.175, height*0.26, width*0.177, height*0.261), 3:(width*0.394, height*0.105, width*0.396, height*0.106), 4:(width*0.674, height*0.263, width*0.676, height*0.264), 5:(width*0.726, height*0.528, width*0.727, height*0.529), 6:(width*0.38, height*0.733, width*0.381, height*0.734)}
    action = actionByColour(img.crop(dict[seat]))
    return action

def usInfo():
    
    im = BI.getImage()
    
    width, height = im.size 
    stack = im.crop((width*0.403, height*0.86, width*0.537, height*0.88))
    bet = im.crop((width*0.403, height*0.685, width*0.537, height*0.705))
    
    bet = imageProcess(bet)
    stack = imageProcess(stack)
    
    betTxt = re.sub("[^0123456789.]", "", readText(bet))
    stackTxt = re.sub("[^0123456789.]", "", readText(stack))
    
    return Player("Alieuzz", float(stackTxt), 6)

def usAction():
    
    cards = 1
    action = 0
    
    im = BI.getImage()
    width, height = im.size 
    bet = im.crop((width*0.403, height*0.685, width*0.537, height*0.705))
    bet = imageProcess(bet)
    betTxt = re.sub("[^0123456789.]", "", readText(bet))
    
    return (cards, action, bet)

def matchCards(img):
    im = img.convert('L')
    
    icon = Image.open("D:\Jack Data\workspace\PokerTools\src\Bot\Hold Cards Database\PlayerCardIcon.png")
    
    icon = np.array(icon)
    npIm = np.array(im)
    
    res = cv2.matchTemplate(npIm, icon, cv2.TM_CCOEFF_NORMED)
    
    if (np.amax(res) > 0.7):
        return True
    else:
        return False

