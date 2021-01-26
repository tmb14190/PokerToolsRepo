'''
Created on 20 Sep 2019

@author: Jack
'''
from PIL import Image
import pyscreenshot as ImageGrab
import threading
import cv2 
import numpy as np 
from datetime import datetime
import multiprocessing

def new_session():
    
    f = open(r"hands.txt", "r") 
    
    input = f.read()
    
    f.close()
    
    with open(r"sessions.txt", "a") as file:
        file.write("\n")
        file.write(input)
        file.close()
    
    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    with open(r"hands.txt", "w") as file:
        file.write(dt + " 0 " + dt)
        file.close()
    
    return 0

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
        
        if (rowrow == 2):
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
    
    if find_winner_byte(img):
        print ("Yaldi")
    else:
        print("Unlucky bud")

def main():
    
    print ("Starting")
    
    im = ImageGrab.grab()  
        
    img_tables = get_tables(im)
    
    last_state = []
    
    for i in range(0, len(img_tables)):
        last_state.append(False)
    
    # grab screen
    while(True):
        
        img = ImageGrab.grab()
            
        img_tables = get_tables(img)
        
        if (len(last_state) > len(img_tables)):
            while (len(last_state) != len(img_tables)):
                del last_state[-1]
        elif (len(last_state) < len(img_tables)):
            while (len(last_state) != len(img_tables)):
                last_state.append(False)
            
        print ("Tables: " + str(len(img_tables)))
        
        f = open(r"hands.txt", "r")
        h = f.read().split()
        f.close()
        print ("Session hands: " + "".join(h[2].split(":")))
        
        count = 0
        for i in img_tables:
            
            #print (count)
            output = find_winner_byte(i)
            
            if (count < len(last_state)):
                if (last_state[count] == True and output == False):
                    f = open(r"hands.txt", "r")
                    
                    input = f.read().split()
                    f.close()
                    
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split()
                    
                    if (input[3] == dt[0]):
                        last_time = input[4]
                        current = dt[1]
                        FMT = "%H:%M:%S"
                        
                        tdelta = datetime.strptime(current, FMT) - datetime.strptime(last_time, FMT)
                        print (tdelta)
                        
                        diff = int("".join(str(tdelta).split(":")))
                        print (diff)
                        
                        if (diff > 3000):
                            hands = new_session()
                        else:
                            hands = int(input[2])
                    else:
                        hands = new_session()
                    
                    f = open(r"hands.txt", "r")
                    
                    input = f.read().split()
                    
                    f.close()
                    
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    with open(r"hands.txt", "w") as file:
                        file.write(input[0] + " " + input[1] + " " +  str(hands + 1) + " " + dt)
                        file.close()
                            
                last_state[count] = output
                count += 1
    

if __name__ == '__main__':
    
    multiprocessing.freeze_support()
    
    main()
            
                
    
