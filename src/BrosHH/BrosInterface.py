'''
Created on 4 May 2020

@author: jackm
'''
from pynput.keyboard import Key,  Controller
from pywinauto.application import Application
from pywinauto.keyboard import send_keys, KeySequenceError
import time
from PIL import Image
from PIL import ImageOps
import os, random
import cv2 
import numpy as np

def focusBros():
    app = Application().connect(title_re="LDPlayer")

    dlg = app.LDPlayer

    dlg.set_focus()

def resizeBros():
    app = Application().connect(title_re="LDPlayer")

    dlg = app.LDPlayer

    dlg.set_focus()
    
    dlg.move_window(x=None, y=None, width = 601, height = 1040)
    
    
def getWindowSize():
    app = Application().connect(title_re="LDPlayer")

    dlg = app.LDPlayer

    dlg.set_focus()
    
    print(dlg.Rectangle())

def getImage():
    app = Application().connect(title_re="LDPlayer")
    dlg = app.LDPlayer
    return dlg.capture_as_image()
    #return Image.open("D:\Jack Data\workspace\PokerTools\src\Bot\Hold Cards Database\screenshot.png")

''' 
Should return a list where if we are under action, the table number is added. E.g. table q is under action list = [0]
table w and r are under action, list = [1, 3] 
'''
def checkToolbar():
    
    action = 0
    
    return action

def getTables():
    
    tables = 0
    
    return tables

''' Gets screenshot of full PokerBros, returns images of board cards '''
def findBoardCards():
    
    img = getImage()
    
    WIDTH, HEIGHT = img.size
    
    midColour = img.crop((0, HEIGHT*0.33, WIDTH, HEIGHT*0.66))
    
    mid = midColour.convert('L')
    
    data = list(mid.getdata())

    WIDTH, HEIGHT = mid.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    
    y = 0
    coords = []
    flag = 0
    cardWidth = 0
    
    for row in data:
        counter = 0  
        x = 0
        s = ()
        for index in row:
            if (index >= 230 and index <= 240):
                if (counter == 0):
                    s = (x, y)
                counter+=1
            else:
                if (counter > 40):
                    coords.append(s)
                    flag = 1
                    cardWidth = counter
                elif (counter > 0):
                    s = ()
                counter  = 0
            x+=1
        if (flag == 1):
            break;
        y+=1
    
    board = []
    # Adjust for card angles
    a = -8
    b = 0
    
    for c in coords:
        card = midColour.crop((c[0]+a, c[1], c[0]+cardWidth+b, c[1]+75))
        sizedCard = card.resize((63, 75))
        board.append( sizedCard )
        a+=2
        b+=2
    
    return board

def findHoldCards():
    img = getImage()
    
    WIDTH, HEIGHT = img.size
    
    botColour = img.crop((0, HEIGHT*0.66, WIDTH, HEIGHT))
    
    bot = botColour.convert('L')
    
    data = list(bot.getdata())

    WIDTH, HEIGHT = bot.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    
    y = 0
    flag = 0
    cardWidth = 0
    coords = ()
    
    for row in data:
        counter = 0  
        x = 0
        s = ()
        for index in row:
            if (index >= 230 and index <= 240):
                if (counter == 0):
                    s = (x, y)
                counter+=1
            else:
                if (counter > 35):
                    coords = s
                    flag = 1
                    cardWidth = counter
                elif (counter > 0):
                    s = ()
                counter  = 0
            x+=1
        if (flag == 1):
            break;
        y+=1
    
    if (len(coords) > 0):
        right = botColour.crop((coords[0], coords[1], coords[0]+cardWidth+5, coords[1]+67)).resize((43, 67))
        left = botColour.crop((coords[0]-cardWidth, coords[1], coords[0], coords[1]+67)).resize((38, 67))
    else:
        left = ""
        right = ""
    
    return left, right

def findSuitFromImage(card):
    
    ''' heart (red) = 52
        club (green) = 88
        diamond (blue) = 64
        spade (black) = 31
    '''
    
    cardGrey = card.convert('L')
    
    data = list(cardGrey.getdata())

    WIDTH, HEIGHT = cardGrey.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    
    h = 0
    c = 0
    d = 0
    s = 0
    
    for row in data:
        for index in row:
            if (index >= 51 and index <= 53):
                h+=1
            elif (index >= 87 and index <= 89):
                c+=1
            elif (index >= 63 and index <= 65):
                d+=1
            elif (index >= 30 and index <= 32):
                s+=1

    if (h > c and h > d and h > s):
        return "h"
    if (c > d and c > s):
        return "c"
    if (d > s):
        return "d"
    if (s != 0):
        return "s"
    else:
        print ("No suit found")
        return ""

def findPlayerCardsCoords():
    im = getImage().convert('L')
    
    icon = Image.open("D:\Jack Data\workspace\PokerTools\src\Bot\Hold Cards Database\PlayerCardIcon.png")
    
    width, height = icon.size
    
    icon = np.array(icon)
    npIm = np.array(im)
    
    res = cv2.matchTemplate(npIm, icon, cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= 0.7)
    
    print (loc)
    x = 0
    y = 0
    coords = []
    for i in range(0, len(loc[0])):
        xDiff = loc[1][i] - x
        yDiff = loc[0][i] - y
        if not(xDiff > -50 and xDiff < 50 and yDiff > -50 and yDiff < 50):
            im.crop((loc[1][i], loc[0][i], loc[1][i]+100, loc[0][i]+100)).show()
            coords.append((loc[1][i], loc[0][i]))
        x = loc[1][i]
        y = loc[0][i]
    
    return coords




    

