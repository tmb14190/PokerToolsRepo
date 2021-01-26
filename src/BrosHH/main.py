'''
Created on 7 Oct 2020

@author: jackm
'''
from BrosHH.Player import Player

import BrosHH.BrosInterface as BI
import BrosHH.ImageToText as IT
from BrosHH.Player import Player
    
def initialise():
    
    BI.focusBros()
    BI.resizeBros()
    img = BI.getImage()
    players = IT.setupPlayers(img)
    
    return players

def runHand(players):
    pointer = 2
    
    while(1):
        get_action()
    
def get_action():
    pass

if __name__ == '__main__':
    
    players = initialise()
    
    runHand(players)
    
    