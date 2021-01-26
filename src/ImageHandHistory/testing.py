from PIL import Image
import pyscreenshot as ImageGrab
import threading
import cv2 
import numpy as np 
from PIL import ImageOps
import pytesseract
import re

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

def get_our_stack(img, state):
    
    width, height = img.size  
    
    if (state == True):
        us = img.crop((width*0.64, height*0.70, width*0.74, height*0.76)) 
    else:
        us = img.crop((width*0.55, height*0.66, width*0.65, height*0.72)) 
    
    us = ImageOps.invert(us)
    
    us.show()
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    
    mi0_abs = pytesseract.image_to_string(us, lang = 'eng')
    
    print (mi0_abs)
    
    output = re.findall("[0123456789.,]", mi0_abs)
    
    if (output != None):
        print ("HERE")
        print (output)
        
    return float(''.join(output))

def check_is_table(img):
    
    img = img.convert('L')
    
    data = list(img.getdata())

    WIDTH, HEIGHT = img.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
      
    for row in data:
        count = 0  
        for index in row:
            if (index == 92):
                count += 1
            
            if (count == 100):
                return True
        
        
    return False

def find_winner_byte(img):
    
    img = img.convert('L')
    
    data = list(img.getdata())

    WIDTH, HEIGHT = img.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
      
    rowrow = 0
    for row in data:
        count = 0  
        for index in row:
            if (index == 161):
                count += 1
            
            if (count == 30):
                rowrow += 1
        
        if (rowrow == 3):
            return True
        
        
    return False

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
        
        table = im_colour.crop((i[0][0], i[0][1], i[1][0], i[0][1] + height))
        
        width, height = table.size  
        
        top = table.crop((0, 0, width / 2, height / 2))
        
        bottom = table.crop((height / 2, width / 2, width, height))
        
        if check_is_table(top) and check_is_table(bottom):
            img_tables.append(table)
    
    return img_tables

def check_table(img, last):
    
    if find_winner_byte(img_tables[0]):
        print ("Yaldi")
    else:
        print("Unlucky bud")

if __name__ == '__main__':
    im = ImageGrab.grab()
        
    img_tables = get_tables(im)
    
    last = []
    
    for i in range(0, len(img_tables)):
        last.append(False)
        
    stack = 0
    
    # grab screen
    while(True):
        img = ImageGrab.grab()
            
        img_tables = get_tables(img)
        
        print (len(img_tables))
        
        count = 0
        for i in img_tables:
            
            #if (len(img_tables) != 2):
                #i.show()
            
            #print (count)
            output = find_winner_byte(i)
            
            if (output == True):
                print ("True")
                # Lets get our current stack
                winloss = get_our_stack(i, False) - stack
                
                print (winloss)
            else:
                print ("False")
            
            if (count < len(last)):
                if (last[count] == True and output == False):
                    
                    # Lets get our stack at the start of the hand
                    stack = get_our_stack(i, True)
                    
                    f = open(r"C:\Users\Jack\Poker\SkyHandHistory\Hands\hands.txt", "r")
                    hands = int(f.read())
                    
                    print (hands)
                    
                    with open(r"C:\Users\Jack\Poker\SkyHandHistory\Hands\hands.txt", "w") as file:
                        file.write(str(hands + 1))
                            
                last[count] = output
                count += 1
            