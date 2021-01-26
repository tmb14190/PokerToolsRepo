'''
Created on 13 Sep 2019

@author: Jack
'''
import pyscreenshot as ImageGrab
from ImageHandHistory.save_as_bytes import save_as_bytes as SAB
from PIL import Image
from PIL import ImageOps
import time
import cv2 
import numpy as np 
import pytesseract
import re

def find_winner_byte(img):
    
    img = img.convert('L')
    
    data = list(img.getdata())

    WIDTH, HEIGHT = img.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
      
    for row in data:
        count = 0  
        for index in row:
            if (index == 161):
                count += 1
            
            if (count == 20):
                return True
        
        
    return False

def find_winner(img):
    
    opencvImage = np.array(img)
      
    # Convert it to grayscale 
    img_gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY) 
    
    threshold = 0.8
    
    # Read the dot images
    image = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Winner Colour\pattern.png", 0)
    res = cv2.matchTemplate(img_gray,image,cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= threshold)
    print (loc)
    
    ord = loc[1].tolist()
    
    if (len(ord) > 0):
        return  True
    else:
        return False

def find_active_player(img):
    
    return 0

def read_bet(img):
    
    #img.show()
    
    temp = img.resize((img.size[0]*2, img.size[1]*2))
    
    temp = ImageOps.invert(temp)
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    mi0_abs = pytesseract.image_to_string(temp, lang = 'eng')
    
    print (mi0_abs)
    
    output = re.findall("[0123456789.,]", mi0_abs)
    
    if (output != None):
        print ("HERE")
        print (output)
    
    return ''.join(output)

def get_pot_OCR(img):
    
    pot_img = img.crop((img.size[0]*0.4, img.size[1]*0.42, img.size[0]*0.6, img.size[1]*0.53))
    
    temp = pot_img.resize((pot_img.size[0]*1, pot_img.size[1]*1))
    
    temp = ImageOps.invert(temp)
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    mi0_abs = pytesseract.image_to_string(temp, lang = 'eng')
    
    return mi0_abs

def get_pot(img):
    
    pot_img = img.crop((img.size[0]*0.4, img.size[1]*0.42, img.size[0]*0.6, img.size[1]*0.53))
    
    return match_numbers(pot_img)

def match_numbers(img):
    
    opencvImage = np.array(img)
      
    # Convert it to grayscale 
    img_gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY) 
    
    order = {}  
    threshold = 1
    
    # Read the dot images
    image = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\dot.png", 0)
    image2 = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\dot-2.png", 0)
    res = cv2.matchTemplate(img_gray,image,cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(img_gray,image2,cv2.TM_CCOEFF_NORMED)
    
    loc = np.where(res >= threshold)
    print (loc)
    loc2 = np.where(res2 >= threshold)
    print (loc2)
    ord = loc[1].tolist()
    if (len(ord) > 0):
        for i in ord:
            order[i] = "."
    ord = loc2[1].tolist()
    if (len(ord) > 0):
        for i in ord:
            order[i] = "."
    
    temp = len(order)
    folder = "\XS - 7"
    threshold = 0.7
    for i in range(0, 5):
        if (i == 1):
            folder = "\S - 8"
        elif (i == 2):
            folder = "\M - 9"
        elif (i == 3):
            folder = "\L - 10"
        elif (i == 4):
            folder = "\XL - 11"
        
        for j in range(0, 10):
            
            destination = r"C:\Users\Jack\Poker\SkyHandHistory\Numbers" + folder + "\\" + str(j) + ".png"
            print (destination)
            image = cv2.imread(destination, 0)
            res = cv2.matchTemplate(img_gray,image,cv2.TM_CCOEFF_NORMED)
            
            print (int(str(i) + str(j)))
            
            loc = np.where(res >= threshold)
            print (loc)
            
            if (len(loc[1]) > 0):
                for k in loc[1].tolist():
                    order[k] = str(j)
        
        #if (temp - len(order) != 0):
        #    break;
    
    print (dict(sorted(order.items())).values())
    
    characters = ''.join((dict(sorted(order.items())).values()))
    
    print (characters)
    
    return float(characters)
        

def get_tables(im):
    
    im_colour = im
    im = im_colour.convert("L")
    
    WIDTH, HEIGHT = im.size
         
    data = list(im.getdata())
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
        
    y = 0
    start = []
    end = []
        
    for row in data:
        counter = 0
        flag = 0
        x = 0
        s = ()
        for value in row:
            if (value == 255):
                if (counter == 0):
                    s = (x, y)
                counter += 1
            else:
                if (counter > 400):
                    end.append((x-1, y))
                    start.append(s)
                elif (counter > 0):
                    s = ()
                counter = 0
                        
            x+=1
             
        y+=1
        
    unique = []
    exists = []
        
    for i in range (0, len(end)):
        flag = True
        for j in exists:
            if (abs(start[i][0] - j[0]) < 150  and abs(start[i][1] - j[1] < 50)):
                flag = False
        if (flag):
            unique.append((start[i], end[i]))
            exists.append((start[i][0], start[i][1]))
       
    img_tables = []
    
    for i in unique:
        
        width = i[1][0] - i[0][0]
        
        height = int(width * 0.8)
        
        img_tables.append(im_colour.crop((i[0][0], i[0][1], i[1][0], i[0][1] + height)))
    
    return img_tables

def get_players(img_table):
    
    width, height = img_table.size    
    
    players = []

    players.append(img_table.crop((width*0.225, height*0.05, width*0.475, height*0.3))) 
    players.append(img_table.crop((width*0.525, height*0.05, width*0.775, height*0.3)))
    players.append(img_table.crop((width*0.75, height*0.3, width, height*0.55)))
    players.append(img_table.crop((width*0.525, height*0.55, width*0.775, height*0.8))) 
    players.append(img_table.crop((width*0.225, height*0.55, width*0.475, height*0.8)))
    players.append(img_table.crop((0, height*0.3, width*0.25, height*0.55)))
    
    return players

def get_MI(img_players):
    
    mi = []
    
    # player0, player5 money invested bottom right - mi = money invest
  
    mi.append(img_players[0].crop((img_players[0].size[0]*0.5, img_players[0].size[1]*0.5, img_players[0].size[0], img_players[0].size[1])))
    mi.append(img_players[5].crop((img_players[5].size[0]*0.5, img_players[5].size[1]*0.5, img_players[5].size[0], img_players[5].size[1])))
 
    # player1, player2 bottom left
 
    mi.append(img_players[1].crop((0, img_players[1].size[1]*0.5, img_players[1].size[0]*0.5, img_players[1].size[1])))
    mi.append(img_players[2].crop((0, img_players[2].size[1]*0.5, img_players[2].size[0]*0.5, img_players[2].size[1])))
 
    # player3 top left
 
    mi.append(img_players[3].crop((0, 0, img_players[3].size[0]*0.5, img_players[3].size[1]*0.5)))
 
    # player4 top right
 
    mi.append(img_players[4].crop((img_players[4].size[0]*0.5, 0, img_players[4].size[0], img_players[4].size[1]*0.5)))
    
    return mi
     
if __name__ == '__main__':
    
    start = time.time()
    
    #imag = Image.open(r"C:\Users\Jack\Poker\SkyHandHistory\375.png").convert("L")
    
    #print (read_bet(imag))
    
    # grab screen
    im = ImageGrab.grab()
        
    img_tables = get_tables(im)
    
    img_tables[0].show()
    
    img_players = []
    for i in img_tables:
        img_players.append(get_players(i))
        
        print (img_players[0])
    
    mi0 = img_players[0][0].crop((img_players[0][0].size[0]*0.5, img_players[0][0].size[1]*0.5, img_players[0][0].size[0], img_players[0][0].size[1]))
    
    #img_tables[0].save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\table_test.png")
    
    muhh = Image.open(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\table_test.png")
    
    if find_winner_byte(img_tables[0]):
        print ("Yaldi")
    
    #bet = match_numbers(mi0)
    
    
    
    #pot = get_pot(img_tables[0])
    pot_OCR = get_pot_OCR(img_tables[0])
    
    mi = get_MI(img_players[0])
    
    for i in mi:
        print (read_bet(i))
    
    #print ("Bet: " + bet)
    #print ("Pot: " + pot)
    print (pot_OCR)
    
    end = time.time()
    print (end - start)
        
    