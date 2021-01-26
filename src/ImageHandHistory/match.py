'''
Created on 12 Sep 2019

@author: Jack
'''
import cv2 
import numpy as np 
  
# Read the main image 
img_rgb = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Get Players\mi4.png")
  
# Convert it to grayscale 
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
  
# Read the template 
dot = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\dot.png", 0) 
zero = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\0.png", 0) 
one = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\1.png", 0) 
two = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\2.png", 0) 
three = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\3.png", 0) 
four = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\4.png", 0) 
five = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\5.png", 0) 
six = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\6.png", 0) 
seven = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\7.png", 0) 
eight = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\8.png", 0) 
nine = cv2.imread(r"C:\Users\Jack\Poker\SkyHandHistory\Numbers\9.png", 0) 
  
# Perform match operations. 
res_zero = cv2.matchTemplate(img_gray,zero,cv2.TM_CCOEFF_NORMED) 
res_dot = cv2.matchTemplate(img_gray,dot,cv2.TM_CCOEFF_NORMED) 
res_one = cv2.matchTemplate(img_gray,one,cv2.TM_CCOEFF_NORMED) 
res_five = cv2.matchTemplate(img_gray,five,cv2.TM_CCOEFF_NORMED) 
res_six = cv2.matchTemplate(img_gray,six,cv2.TM_CCOEFF_NORMED) 
  
# Specify a threshold 
threshold = 0.8
  
# Store the coordinates of matched area in a numpy array 
loc_zero = np.where( res_zero >= threshold)  
loc_dot = np.where( res_dot >= threshold) 
loc_one = np.where( res_one >= threshold) 
loc_five = np.where( res_five >= threshold) 
loc_six = np.where( res_six >= threshold) 

print (loc_zero)
print (loc_dot)
print (loc_one)
print (loc_five)
print (loc_six)