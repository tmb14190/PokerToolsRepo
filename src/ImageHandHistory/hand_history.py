'''
Created on 1 Jun 2020

@author: jackm
'''
from PIL import Image
import pyscreenshot as ImageGrab
import threading
import cv2 
import numpy as np 
from datetime import datetime
import multiprocessing
import pytesseract

def imageProcess(img):

    width, height = img.size
    
    largeImg = img.resize((int(width*5), int(height*5)), 1)
    
    
    processed = Image.eval(largeImg, lambda x: 0 if x >= 150 else 255)

    return processed

def processName(img):
    
    img = img.convert('L')

    width, height = img.size
    
    largeImg = img.resize((int(width*5), int(height*5)), 1)
    
    
    processed = Image.eval(largeImg, lambda x: 0 if x >= 120 and x <= 150 else 255)

    return processed

def readText(img):

    pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract'
    
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 7')
    
    return text

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

def main():

    im = ImageGrab.grab()  
        
    img_tables = get_tables(im)
    
    width, height = img_tables[0].size    

    players = []

    players.append(img_tables[0].crop((width*0.225, height*0.05, width*0.475, height*0.3))) 
    players.append(img_tables[0].crop((width*0.525, height*0.05, width*0.775, height*0.3)))
    players.append(img_tables[0].crop((width*0.75, height*0.3, width, height*0.55)))
    players.append(img_tables[0].crop((width*0.525, height*0.55, width*0.775, height*0.8))) 
    players.append(img_tables[0].crop((width*0.225, height*0.55, width*0.475, height*0.8)))
    players.append(img_tables[0].crop((0, height*0.3, width*0.25, height*0.55)))
    
    pro = processName(players[0])
    
    pro.show()
    
    print (readText(pro))
    
if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    
    main()