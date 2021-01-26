'''
Created on 18 Apr 2020

@author: jackm
'''
import os, random
from PIL import Image

range = []

cpt = sum([len(files) for r, d, files in os.walk("D:\Jack Data\Poker\Pairrd Ranges")])

list = os.listdir("D:\Jack Data\Poker\Pairrd Ranges") # dir is your directory path
number_files = len(list)
print (cpt)

counter = 0

for r, d, files in os.walk("D:\Jack Data\Poker\Pairrd Ranges"):
    for filename in os.listdir(r):
        if (".PNG" in filename):
            range.append(r + "\\" + filename)
    print (r)
    print (d)
    
print (range)

i = random.randint(0, 256)

img = Image.open(range[i])
img.show()