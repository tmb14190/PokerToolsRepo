'''
Created on 13 May 2020

@author: jackm
'''
import BrosHH.ImageToText as IT
import re
import numpy as np

class Player():

    name = ""
    action = None
    bet = 0
    position = ""
    starting = 0
    money_committed = 0
    total_money_committed = 0
    hand = ""
    summary = ""
    acceptable_actions = ["Call", "Raise", "Bet", "Check", "Fold", "BB", "SB", "All In", "New"]
    end_state = False

    def __init__(self, seat, img):
        self.seat = seat
        self.setCards(img)
        self.playing = None
        if (not self.cards):
            self.setAction(img)
            if (not self.action == "Fold"):
                self.playing = False
            self.action = None
        if (self.playing is None):
            self.playing = True
            self.initialise(img)

    def initialise(self, img):
        self.setName(img)
        self.setStack(img)

    def setPosition(self, position):
        self.position = position
    
    def setEndState(self, state):
        self.end_state = state

    def setAction(self, img):
        width, height = img.size
        #dict = {1:(width*0.12, height*0.528, width*0.122, height*0.529), 2:(width*0.16, height*0.253, width*0.27, height*0.273), 3:(width*0.39, height*0.098, width*0.48, height*0.113), 4:(width*0.665, height*0.253, width*0.775, height*0.273), 5:(width*0.72, height*0.518, width*0.83, height*0.538), 6:(width*0.38, height*0.725, width*0.48, height*0.742)}
        dict = {1:(width*0.132, height*0.528, width*0.133, height*0.529), 2:(width*0.175, height*0.26, width*0.177, height*0.261), 3:(width*0.394, height*0.105, width*0.396, height*0.106), 4:(width*0.674, height*0.263, width*0.676, height*0.264), 5:(width*0.726, height*0.528, width*0.727, height*0.529), 6:(width*0.38, height*0.733, width*0.381, height*0.734)}
        self.action = IT.actionByColour(img.crop(dict[self.seat]))
        #if (self.position is not None):
        #   print (self.position + str(self.action))

    def setStack(self, img):
        width, height = img.size
        dict = {1:(width*0.057, height*0.642, width*0.197, height*0.662), 2:(width*0.12, height*0.37, width*0.25, height*0.39), 3:(width*0.41, height*0.21, width*0.53, height*0.23), 4:(width*0.695, height*0.37, width*0.825, height*0.39), 5:(width*0.748, height*0.642, width*0.878, height*0.662), 6:(width*0.403, height*0.86, width*0.537, height*0.88)}
        stack = IT.imageProcess(img.crop(dict[self.seat]))
        try:
            self.stack = float(re.sub("[^0123456789.]", "", IT.readText(stack)))
        except ValueError:
            print (self.name + " stack failed to read")

    def setName(self, img):
        if (self.seat != 6):
            width, height = img.size
            dict = {1:(width*0.057, height*0.622, width*0.197, height*0.642), 2:(width*0.115, height*0.35, width*0.255, height*0.37), 3:(width*0.403, height*0.19, width*0.537, height*0.21), 4:(width*0.69, height*0.35, width*0.83, height*0.37), 5:(width*0.745, height*0.622, width*0.885, height*0.642)}
            name = IT.imageProcess(img.crop(dict[self.seat]))
            self.name = IT.readText(name)
        else:
            self.name = "Homie"

    def setBet(self, img):
        width, height = img.size
        dict = {1:(width*0.222, height*0.627, width*0.322, height*0.647), 2:(width*0.265, height*0.355, width*0.365, height*0.375), 3:(width*0.52, height*0.22, width*0.62, height*0.24), 4:(width*0.575, height*0.355, width*0.675, height*0.375), 5:(width*0.6225, height*0.627, width*0.7225, height*0.647), 6:(width*0.403, height*0.685, width*0.537, height*0.705)}
        bet = IT.imageProcess(img.crop(dict[self.seat]))
        try:
            bet = re.sub("[^0123456789.]", "", IT.readText(bet))
            self.bet = float(bet)
        except ValueError:
            if (self.bet != 0 and self.bet is not None and str(self.bet) != ""):
                print (self.name + " bet was read as :" + str(bet) + ":")
            self.bet = None

    def setCards(self, img):
        width, height = img.size
        dict = {1:(width*0.065, height*0.59, width*0.067, height*0.591), 2:(width*0.12, height*0.32, width*0.122, height*0.321), 3:(width*0.537, height*0.165, width*0.539, height*0.166), 4:(width*0.82, height*0.32, width*0.822, height*0.321), 5:(width*0.878, height*0.59, width*0.88, height*0.591), 6:(width*0.563, height*0.772, width*0.564, height*0.773)}
        pixel = img.crop(dict[self.seat])
        p_array = np.array(pixel)
        if (self.seat !=6 and p_array[0][0][0] == 66 and p_array[0][0][1] == 125 and p_array[0][0][2] == 164):
            self.cards = True
        elif (self.seat == 6 and p_array[0][0][0] == 230 and p_array[0][0][1] == 235 and p_array[0][0][2] == 230):
            self.cards = True
        else:
            self.cards = False

    def setHand(self, hand):
        self.hand = hand

    '''
    NEEDS DOING
    '''
    def addSummary(self, summary):
        pass
