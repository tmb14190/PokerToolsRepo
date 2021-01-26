'''
Created on 20 Sep 2019

@author: Jack
'''
from PIL import ImageOps
import pytesseract
from PIL import Image
import pyscreenshot as ImageGrab
import threading
import re
from ImageHandHistory.save_as_bytes import save_as_bytes as SAB

def read_bet(img, invert_flag):
    
    
    
    temp = img.resize((img.size[0], img.size[1]))
    
    if (invert_flag):
        temp = ImageOps.invert(temp)
        muh = temp.convert('L')
        
        temp = Image.eval(muh, lambda x: 255 if x == 110 else x)
            
    temp.show()
    pytesseract.pytesseract.tesseract_cmd = r'E:\Jack Data\Tesseract-OCR\tesseract'


    mi0_abs = pytesseract.image_to_string(temp, lang = 'eng')
    
    print (mi0_abs)
    
    output = re.findall("[0123456789.,]", mi0_abs)
    
    if (output != None):
        print ("HERE")
        print (output)
    
    return ''.join(output)

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

def check_table(img, last):
    
    if find_winner_byte(img_tables[0]):
        print ("Yaldi")
    else:
        print("Unlucky bud")

if __name__ == '__main__':
    im = ImageGrab.grab()
        
    img_tables = get_tables(im)
    
    last = []
    last_count = []
    current_count = []
    
    for i in range(0, len(img_tables)):
        last.append(False)
        last_count.append(0)
        current_count.append(0)
    
    # grab screen
    while(True):
        img = ImageGrab.grab()
            
        img_tables = get_tables(img)
        
        count = 0
        for i in img_tables:
            
            width, height = i.size  
            player_img = i.crop((width*0.525, height*0.55, width*0.775, height*0.8))
            width, height = player_img.size 
            
            #print (count)
            output = find_winner_byte(i)
            
            if (output == True):
                print ("True")
                player_img = player_img.crop((width*0.15, height*0.52, width*0.65, height*0.7))
                current_count[count] = (read_bet(player_img, True))
            else:
                print ("False")
            
            if (last[count] == True and output == False):
                f = open(r"E:\Jack Data\Poker\SkyHandHistory\Hands\wl.txt", "r")
                hands = int(f.read()) + 1
                
                print (type(hands))
                print (hands)
                
                with open(r"E:\Jack Data\Poker\SkyHandHistory\Hands\wl.txt", "w") as file:
                    file.write(str(hands))
                
                #with open(r"E:\Jack Data\Poker\SkyHandHistory\Hands\hand_win_loss.txt", "a") as file:
                 #   file.write(str(hands) + " : " + str(last_count[count] - current_count[count]))
                
                player_img = player_img.crop((width*0.475, height*0.65, width*0.875, height*0.8))
                last_count[count] = (read_bet(player_img, False))
                
            last[count] = output
            count += 1
