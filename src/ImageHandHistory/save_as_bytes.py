'''
Created on 20 Sep 2019

@author: Jack
'''
from PIL import Image

def save_as_bytes(img):
    
    data = list(img.getdata())

    WIDTH, HEIGHT = img.size
         
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
        
    with open(r"D:\Jack Data\Poker\SkyHandHistory\getting_colour.txt", "w") as file:
        for row in data:
            for i in row:
                i = str(i)
                while (len(i) < 3):
                    i = "0" + i
                file.write(i + " ")
            file.write("\n")
            