'''
Created on 9 Oct 2020

@author: jackm
'''
from bisect import bisect

import BrosHH.ImageToText as IT
import BrosHH.BrosInterface as BI

img = BI.getImage()

width, height = img.size

print(IT.actionByColour(img.crop(width*0.132, height*0.528, width*0.133, height*0.529)))

