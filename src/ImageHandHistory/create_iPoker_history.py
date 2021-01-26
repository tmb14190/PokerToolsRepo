'''
Created on 12 Sep 2019

@author: Jack
'''
from pynput.keyboard import Key,  Controller
from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto.keyboard import send_keys, KeySequenceError
import time
from PIL import Image
from PIL import ImageOps
import os, random
import cv2 
import numpy as np

app = Application().connect(title_re="Sky Poker", found_index = 0)

w = app.windows()

for win in w:
    print (win)

dlg = app.window(title_re = "[A-Za-z]")

dlg.set_focus()