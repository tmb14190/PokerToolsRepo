'''
Created on 8 Aug 2019

@author: Jack
'''
from PIL import Image
import pytesseract
import cv2
import PIL.ImageOps  

#include('examples/showgrabfullscreen.py') --#
# import pyscreenshot as ImageGrab
#     
# if __name__ == '__main__':
#    
#     # grab fullscreen
#     im = ImageGrab.grab()
#        
#     print (im)
#    
#     # save image file
#     im.save(r"C:\Users\Jack\Poker\SkyHandHistory\test7.png")
#    
#     # show image in a window
#     im.show()
#     #-#

im = Image.open(r"C:\Users\Jack\Poker\SkyHandHistory\test7.png").convert("L")
im_colour = Image.open(r"C:\Users\Jack\Poker\SkyHandHistory\test7.png")


WIDTH, HEIGHT = im.size
     
#WIDTH = 100
#HEIGHT = 100
     
data = list(im.getdata())
     
data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
     
# chars = '@%#*+=-:. '  # Change as desired.
# scale = (len(chars)-1)/255.
    
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
    
print (start)
print (end)
last = 100000
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

# counter = 0
# for i in img_tables:
#     i.save(r"C:\Users\Jack\Poker\SkyHandHistory\tableT" + str(counter) + ".png")
#     counter += 1

''' Lets get the players '''

width, height = img_tables[0].size    

player0 = img_tables[0].crop((width*0.225, height*0.05, width*0.475, height*0.3)) 
player1 = img_tables[0].crop((width*0.525, height*0.05, width*0.775, height*0.3))
player2 = img_tables[1].crop((width*0.75, height*0.3, width, height*0.55))

player3 = img_tables[1].crop((width*0.525, height*0.55, width*0.775, height*0.8)) 

player4 = img_tables[2].crop((width*0.225, height*0.55, width*0.475, height*0.8))
player5 = img_tables[2].crop((0, height*0.3, width*0.25, height*0.55))

mi0 = player0
mi1 = player1
mi2 = player2
mi3 = player3
mi4 = player4
mi5 = player5

# player0, player5 money invested bottom right - mi = money invest

# mi0 = player0.crop((player0.size[0]*0.5, player0.size[1]*0.5, player0.size[0], player0.size[1]))
# mi5 = player5.crop((player5.size[0]*0.5, player5.size[1]*0.5, player5.size[0], player5.size[1]))
# 
# # player1, player2 bottom left
# 
# mi1 = player1.crop((0, player1.size[1]*0.5, player1.size[0]*0.5, player1.size[1]))
# mi2 = player2.crop((0, player2.size[1]*0.5, player2.size[0]*0.5, player2.size[1]))
# 
# # player3 top left
# 
# mi3 = player3.crop((0, 0, player3.size[0]*0.5, player3.size[1]*0.5))
# 
# # player4 top right
# 
# mi4 = player4.crop((player4.size[0]*0.5, 0, player4.size[0], player4.size[1]*0.5))
# 
# mL = mi0.convert('L')

# dataMI0 = list(mL.getdata())
# WIDTH, HEIGHT = mi0.size
#      
# data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

# for x in range(0, len(data)):
#     for y in range(0, len(data[x])):
#         if (data[x][y] != 255):
#             data[x][y] = 0

# mi0 = Image.eval(mi0, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# mi1 = Image.eval(mi1, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# mi2 = Image.eval(mi2, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# mi3 = Image.eval(mi3, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# mi4 = Image.eval(mi4, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# mi5 = Image.eval(mi5, lambda x: 255 if x == 255 or x >= 220 and x <= 225 else 0)
# 
# mi0.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test0.png")
# mi1.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test1.png")
# mi2.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test2.png")
# mi3.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test3.png")
# mi4.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test4.png")
# mi5.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\test5.png")

# resize for OCR
scale = 3

mi0 = mi0.resize((mi0.size[0]*scale, mi0.size[1]*scale))
mi1 = mi1.resize((mi1.size[0]*scale, mi1.size[1]*scale))
mi2 = mi2.resize((mi2.size[0]*scale, mi2.size[1]*scale))
mi3 = mi3.resize((mi3.size[0]*scale, mi3.size[1]*scale))
mi4 = mi4.resize((mi4.size[0]*scale, mi4.size[1]*scale))
mi5 = mi5.resize((mi5.size[0]*scale, mi5.size[1]*scale))

mi0 = PIL.ImageOps.invert(mi0)
mi1 = PIL.ImageOps.invert(mi1)
mi2 = PIL.ImageOps.invert(mi2)
mi3 = PIL.ImageOps.invert(mi3)
mi4 = PIL.ImageOps.invert(mi4)
mi5 = PIL.ImageOps.invert(mi5)

# mi0 = Image.eval(mi0, lambda x: 255 if x == 162 else x)
# mi0 = Image.eval(mi0, lambda x: 255 if x >= 145 and x <= 150 else x)
# mi1 = Image.eval(mi1, lambda x: 255 if x == 162 else x)
# mi1 = Image.eval(mi1, lambda x: 255 if x >= 145 and x <= 150 else x)
# mi2 = Image.eval(mi2, lambda x: 255 if x == 162 else x)
# mi2 = Image.eval(mi2, lambda x: 255 if x >= 145 and x <= 150 else x)
# mi3 = Image.eval(mi3, lambda x: 255 if x == 162 else x)
# mi3 = Image.eval(mi3, lambda x: 255 if x >= 145 and x <= 150 else x)
# mi4 = Image.eval(mi4, lambda x: 255 if x == 162 else x)
# mi4 = Image.eval(mi4, lambda x: 255 if x >= 145 and x <= 150 else x)
# mi5 = Image.eval(mi5, lambda x: 255 if x == 162 else x)
# mi5 = Image.eval(mi5, lambda x: 255 if x >= 145 and x <= 150 else x)

mi0.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm0.png")
mi1.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm1.png")
mi2.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm2.png")
mi3.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm3.png")
mi4.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm4.png")
mi5.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\invertm5.png")

data = list(mi2.getdata())

WIDTH, HEIGHT = mi2.size
     
data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    
with open(r"C:\Users\Jack\Poker\SkyHandHistory\inverted_player_ascii.txt", "w") as file:
    for row in data:
        for i in row:
            file.write(str(i) + " ")
        file.write("\n")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

mi0_abs = pytesseract.image_to_string(mi0, lang = 'eng')
mi1_abs = pytesseract.image_to_string(mi1, lang = 'eng')
mi2_abs = pytesseract.image_to_string(mi2, lang = 'eng')
mi3_abs = pytesseract.image_to_string(mi3, lang = 'eng')
mi4_abs = pytesseract.image_to_string(mi4, lang = 'eng')
mi5_abs = pytesseract.image_to_string(mi5, lang = 'eng')
 
print ("Player 0 ---")
print (mi0_abs)
print ("---")

print ("Player 1 ---")
print (mi1_abs)
print ("---")

print ("Player 2 ---")
print (mi2_abs)
print ("---")

print ("Player 3 ---")
print (mi3_abs)
print ("---")

print ("Player 4 ---")
print (mi4_abs)
print ("---")

print ("Player 5 ---")
print (mi5_abs)
print ("---")

# Print player image dimensions and save to file
# print (player0.size)
# print (player1.size)
# print (player2.size)
# print (player3.size)
# print (player4.size)
# print (player5.size)
# 
# player0.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player0.png")
# player1.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player1.png")
# player2.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player2.png")
# player3.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player3.png")
# player4.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player4.png")
# player5.save(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\player5.png")



''' OCR Stuff '''
# img = Image.open(r"C:\Users\Jack\Poker\SkyHandHistory\OCR_stack.png")
# 
# width, height = img.size
# 
# ''' Increase image size by 4x to make the numbers readable and make sure pretty much only the text that we would like read is in the image '''
# 
# img = img.resize((width*4, height*4))
# 
# img.save(r"C:\Users\Jack\Poker\SkyHandHistory\OCR_stack_4x.png")
# 
# text=pytesseract.image_to_string(img, lang = 'eng')
# 
# print ("---")
# print (text)
# print ("---")

  
''' I think for a width of 800, height is about 620 

Height is about 80% of width

283, 30 
874, 506

541
1031
'''
# 
# chars = '@%#*+=-:. '  # Change as desired.
# scale = (len(chars)-1)/255.
#   
# #  
# with open(r"C:\Users\Jack\Poker\SkyHandHistory\text7_ascii.txt", "w") as file:
#     for row in data:
#         file.write(' '.join(chars[int(value*scale)] for value in row))
#         file.write("\n")
#   
# chars = '@%#*+=-:. '  # Change as desired.
# scale = (len(chars)-1)/255.
# print()
# for row in data:
#     print(' '.join(chars[int(value*scale)] for value in row))

#rgb_im = im.convert('RGB')

# p = []
# 
# for i in range(0, 100):
#     for j in range (0, 100):
#         r, g, b = rgb_im.getpixel((i, j))
#         p.append([r, g, b])
# 
# print(r, g, b)
# (65, 100, 137)