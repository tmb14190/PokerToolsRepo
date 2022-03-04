'''
Created on 21 Oct 2020

@author: jackm
'''
from PIL import Image
import pytesseract
import re
import numpy as np
import cv2
import time
from bisect import bisect
import win32api
from sys import getsizeof

import BrosHH.BrosInterface as BI
import BrosHH.ImageToText as IT
from BrosHH.Player import Player
from BrosHH.Pio import Pio
import warnings
warnings.simplefilter('ignore', category=UserWarning)
 
def newHand(bu, img):
    
    players = []
    we_in = False
    
    # set up list with only players who were dealt cards
    bu_index = 0
    t = time.process_time()
    for i in range(1, 7):
        p = Player(i, img)
        if (p.playing):
            players.append(p)
            if (bu == i):
                bu_index = len(players) - 1
            if (i == 6):
                we_in = True
    
    if (len(players) == 0 or len(players) == 1):
        pio = Pio()
        pio.go_again = True
        return players, pio
    
    # K THIS IS KINDA HACKY NGL - but if theres a flop already dont run (maybe too intensive for an edge case?) or if we dont have cards dont run
    street = IT.getStreet(img)
    if (street != 0 or we_in == False):
        print ("Not tracking this hand")
        pio = Pio()
        pio.we_in == False
        return players, pio
    
    print ("Players at Table: " + str(len(players)))
    print ("BU is " + str(bu))
    
    # TESTING IDEA - maybe check here to make sure index initialised for some form of testing
    
    # Set the order with bb at end of list
    if (len(players) > 2):
        bb_index = (bu_index + 2) % (len(players))
    else:
        bb_index = (bu_index + 1) % (len(players))
    
    players[:] = players[bb_index+1:] + players[:bb_index+1]
    pio = Pio()
    
    # going backwards in list (aka starting with bb) add the table position for each player
    sixmax = ["BB", "SB", "BU", "CO", "HJ", "UTG"]
    counter = 0
    for p in reversed(players):
        p.setPosition(sixmax[counter])
        if (p.seat == 6):
            pio.our_position = sixmax[counter]
        counter+=1
    
    players[-1].setBet(img)
    bb_size = players[-1].bet
    work = False
    i = 0
    while (i<3 and work == False):
        try:
            players[-1].money_commited = bb_size
            players[-2].money_commited = bb_size / 2
            print ("BB: " + str(bb_size))
            work = True
        except:
            print ("couldn't get bb size- trying again")
            time.sleep(0.75)
            img = BI.getImage()
            players[-1].setBet(img)
            bb_size = players[-1].bet
            i+=1
    
    if (i >= 3):
        print ("Reading bb bet timed out")
    
    pio.bb = bb_size
    pio.pre = []
    pio.current_bet = bb_size
    pio.bu = bu
    pio.we_in = we_in
    
    if (we_in):
        hand = IT.getHoleCards()
        if (hand[0] != 0):
            pio.hand = "".join(hand)
            print ("Hand: " + pio.hand)
    
    return players, pio

def isNewStreet(players, pio, img):
    street = IT.getStreet(img)
    if (pio.street != street):
        
        if (len(players) > 3):
            if (not pio.dgafWarn):
                print ("We dont give a fuck")
            pio.dgafWarn = True
            time.sleep(1)
            return players, pio, True
        pio.dgafWarn = False
        
        pio.waiting_flag = False
        pio.first_bet = True
        
        old_pot = pio.pot
        pio.pot = IT.getPot()[0]
        print ("Pot read: " + str(pio.pot))
        for p in players:
            pio.ePot += p.money_committed
        print ("Pot expected: " + str(pio.ePot))
        
        pio.street = street
        
        if (not isActionComplete(players)):
            players, pio = estimateAction(players, pio, old_pot, img)
        
        if (pio.street == 1):
            time.sleep(0.5)  # NEED TO EVALUATE EFFECTIVENESS
        board = IT.getBoard()
        pio.board = (" ".join(board))
        print (pio.board)
        resetEndStates(players, 0)
        players = orderWithButton(players, pio.bu)
        resetPlayerActions(players)
        pio.current_bet = 0
        if (street == 1):
            pio.init()
        elif (street == 2 or street == 3):
            pio.addBoardCard(pio.board[-2:])
    
    return players, pio, False

def isActionComplete(players):
    for p in players:
        if (not p.end_state):
            return False
    
    return True

def resetPlayerActions(players):
    
    for p in players:
        p.action = None
        p.bet = None
        #p.total_money_committed += p.money_committed
        p.money_committed = 0

'''
seat = 0 to reset all EndStates
'''
def resetEndStates(players, seat):
    for p in players:
        if (seat != p.seat):
            p.setEndState(False)
            
def orderWithNextPlayer(players, next):
    
    i = 0
    for p in players:
        if (p.seat == next):
            players[:] = players[i:] + players[:i]
            return players
        i += 1 
    
    print ("Seat didnt match any active player when ordering (orderPlayers())")

def orderWithButton(players, bu):
    
    i = 1
    lst = []
    dict = {}
    for p in players:
        if (p.seat == bu):
            players[:] = players[i:] + players[:i]
            return players
        
        lst.append(p.seat - bu)
        dict[p.seat - bu] = p
        i+=1
    
    lst.sort()
    bi = bisect(lst, 0)
    lst_sorted = lst[bi:] + lst[:bi]
    output = []
    for i in lst_sorted:
        output.append(dict[i])
    
    return output

def estimateAction(players, pio, old_pot, img):
    print ("Estimating Action")
    # FOR TURNS AND RIVERS
    if (pio.street == 2 or pio.street == 3):
        
        # If pot is same can assume all checks
        if (old_pot == pio.pot):
            for p in players:
                if (p.end_state == False):
                    print (p.position + " Check")
                    pio.updateAction(p.position, "X", 0)
        
        else:
                
            # can assume all players call the last bet, and if we dont have last bet we're fucked
            if (old_pot + (pio.current_bet * len(players)) == pio.pot):
                for p in players:
                    if (p.end_state == False):
                        print (p.position + " Call")
                        pio.updateAction(p.position, "C", 0)
                        
            else:
                
                # HERE I THINK WE CAN ASSUME ONE PLAYER CALLED AND ONE PLAYER FOLDED TO BET NEED TO FIND THE FOLDER
                
                for i in range(0, len(players)):
                    players[i].setAction(img)
                    if (players[i].action == "Fold"):
                        print (players[i].position + " Fold")
                        pio.updateAction(players[i].position, "F", -1)
                        players.pop(i)
    
    return players, pio
         
# FEELING SKETCH ABOUT THE POT AND STUFF THINK THERES SOMETHING I OVERLOOKED + STR / INTS / FLOATS
# WAY TO FIND OUT IF MISSING ACTION IS TO GET POT ON FLOP/TURN/RIVER AND COMPARE TO EXPECTED POT
def updateAction(players, pio, img):
    
    #print ("Head: " + players[0].name + " Players: " + str(len(players)))
    
    players, pio, dgaf = isNewStreet(players, pio, img)
    
    if (dgaf):
        pio.waiting_flag = True
        return players, pio
    
    if (isActionComplete(players)):
        if (not pio.waiting_flag):
            print ("Waiting on dealer")
            time.sleep(0.1)
            pio.waiting_flag = True
        return players, pio
    
    new_players = []
    counter = 0
    for p in players:
        
        print ("Action on: " + str(p.name))
        
        # SETUP DECISIONS
        old_action = p.action
        old_bet = p.bet
        p.setAction(img)
        p.setBet(img)
        
        # WORK FLAGS
        flag = True
        if ((p.action == "Check" or p.action is None) and pio.street == 0):
            flag = False
        
        if (p.action == "Call" and p.action == old_action and p.bet == old_bet):
            if (not pio.callWarn):
                print ("Call has not changed")
            pio.callWarn = True
            flag = False
            
        if (p.action != old_action and (p.action == "Bet" or p.action =="All In")):
            i = 0
            work = False
            time.sleep(0.75)
            img = BI.getImage()
            p.setBet(img)
            while (i<5 and work == False):
                try:
                    p.bet = float(p.bet)
                    work = True
                except:
                    print ("Bet not read as number - trying again")
                    time.sleep(0.1)
                    img = BI.getImage()
                    p.setBet(img)
                    i+=1
            if (i >= 5):
                print ("Bet read timed out - action estimation capabilities diminished")
        
        if (pio.street != 0 and p.action == "Bet" and p.bet == 0.1):
            print ("Min bet treated as check")
            p.action = "Check"
            p.money_committed = 0.1
        
        if ((p.action != old_action or p.bet != old_bet) and flag):
        
            if (p.action == "Bet" or p.action == "Raise" or p.action == "All In"): 
                p.setEndState(True)
                resetEndStates(players, p.seat)
                try:
                    pio.current_bet = p.bet
                    p.money_committed = float(p.bet)
                except:
                    print ("Bet read failure - action estimation capabilities diminished")
                if (p.action == "Bet"):
                    print (p.position + " Bet " + str(p.bet))
                    pio.updateAction(p.position, "B", p.bet)
                elif (p.action == "Raise"):
                    print (p.position + " Raise")
                    pio.updateAction(p.position, "R", p.bet)
                else:
                    print (p.position + " All In")
                    pio.updateAction(p.position, "B", p.bet)
            elif (p.action == "Call"):
                pio.callWarn = False
                p.setEndState(True)
                try:
                    p.money_committed = float(pio.current_bet)
                    p.bet = pio.current_bet
                except:
                    print ("Current bet read failure when setting call amount - action estimation capabilities diminished")
                print (p.position + " Call " + str(pio.current_bet))
                pio.updateAction(p.position, "C", 0)
            elif (p.action == "Check"):
                if (pio.street != 0):
                    p.setEndState(True)
                    print (p.position + " Check")
                    pio.updateAction(p.position, "X", 0)
            
            if (p.action == "Fold"):
                print (p.position + " Fold")
                if (pio.street != 0):
                    pio.updateAction(p.position, "F", -1)
                if (p.seat == 6):
                    pio.we_in = False
                    print ("Homie folded tracking stopping")
            else:
                new_players.append(p)
                
            counter+=1
        else:
            #print ("Action on " + p.name)
            output_players = new_players + players[counter:]
            output_players = orderWithNextPlayer(output_players, p.seat)
            return output_players, pio
    
    return new_players, pio

def main():
            
    bu = None
    players = None
    pio = None
    
    BI.resizeBros()
     
    while(True):
        t = time.time()
        img = BI.getImage()
        
        new_bu = IT.findButton(img)
        we_raising = IT.weRaising(img)
        if (we_raising):
            print ("We Raising")
        if (bu != new_bu):
            print ("Button Moved: {a} -> {b}".format(a = bu, b = new_bu))
         
        if ((bu == new_bu and pio.we_in and not we_raising) and new_bu != 0):
            players, pio = updateAction(players, pio, img)
        elif (((bu != new_bu and not we_raising) or pio.go_again) and new_bu != 0):
            time.sleep(2.6)
            if (pio is not None):
                if (len(pio.setup) != 0):
                    pio.closeAllPio()
            bu = new_bu
            players, pio = newHand(bu, img)
        else:
            time.sleep(1)
        
        print (time.time() - t)

if __name__ == '__main__':
    main()