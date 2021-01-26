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

import BrosHH.BrosInterface as BI
import BrosHH.ImageToText as IT
from BrosHH.Player import Player
from BrosHH.Hand import HandHistory as HH
from BrosHH import Pio
 
def newHand(bu):
    
    img = BI.getImage()
    
    players = []
    we_in = False
    
    # set up list with only players who were dealt cards
    index = 0
    for i in range(1, 7):
        p = Player(i, img)
        if (p.playing):
            players.append(p)
            if (bu == i):
                index = len(players) - 1
            if (i == 6):
                we_in = True
    
    # TESTING IDEA - maybe check here to make sure index initialised for some form of testing
    
    # Set the order with bb at end of list
    if (len(players) > 2):
        bb = index + 2
    else:
        bb = index + 1
    players[:] = players[bb % (len(players)-1):] + players[:bb % (len(players)-1)]

    # going backwards in list (aka starting with bb) add the table position for each player
    sixmax = ["BB", "SB", "BU", "CO", "HJ", "UTG"]
    counter = 0
    for p in reversed(players):
        p.setPosition(sixmax(counter))
        counter+=1
    
    players[-1].bet(img)
    bb_size = players[-1].bet
    
    summary = HH()
    summary.writeInit(bb_size, players)
    
    # Deal with people posting big blinds
    for p in players:
        p.action()
        if (p.action == "New"):
            summary.writePost(p)
    
    if (we_in):
        hand = IT.getHoleCards()
        summary.writeHoleCards(" ".join(hand)) 
    
    return players, summary

def isNewStreet(players, summary):
    street = IT.getStreet()
    if (summary.street != street):
        summary.street = street
        board = IT.getBoard()
        summary.writeBoard(" ".join(board))
        resetEndStates(players, 0)
        players = orderWithButton(players, summary.bu)
        resetPlayerActions(players)
        if (street == 1):
            Pio.setupSimulation(players, summary)
    
    return players, summary

def isActionComplete(players):
    for p in players:
        if (not p.end_state):
            return False
    
    return True

def resetPlayerActions(players):
    
    for p in players:
        p.action = None
        p.bet = None
        p.total_money_committed += p.money_committed
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

# rake seems to be ~8.45% with 40nl capped at 3.36 no rake pre
def showdown(players, pot):
    pass
         
# FEELING SKETCH ABOUT THE POT AND STUFF THINK THERES SOMETHING I OVERLOOKED + STR / INTS / FLOATS
# WAY TO FIND OUT IF MISSING ACTION IS TO GET POT ON FLOP/TURN/RIVER AND COMPARE TO EXPECTED POT
def updateAction(players, summary):
    
    # THIS DOESNT DO FLOP/TURN/RIVER STUFF CAUSE WE GET THAT BY CHECKING THE BOARD
    # IT MAYBE SHOULD THO...
    if (isActionComplete(players)):
        if (len(players) == 1):
            if (summary.street != 2):
                summary.writeUncalledBet(players[0].bet, players[0])
            else:
                showdown(players, summary)
    
    players, summary = isNewStreet(players, summary)
    
    new_players = []
    counter = 1
    for p in players:
        if (not p.end_state): # DONT THINK THIS DOES ANYTHIGN AFTER LIST REARRANGING
            
            old_action = p.action
            old_bet = p.bet
            p.action()
            p.bet()
            # THIS IS GETTING VERY SCRAPPY ADDING IN THE NEW
            if (p.action != old_action or p.bet != old_bet or p.action == "New"):
            
                if (p.action == "Fold"): 
                    action = "folds"
                else:
                    
                    if (p.action == "Bet" or p.action == "Raise" or p.action == "All In"): 
                        p.setEndState(True)
                        resetEndStates(players, p.seat)
                        p.money_committed = p.bet
                        summary.current_bet = p.bet
                        summary.pot += float(p.bet)
                        if (p.action == "Bet"):
                            action = "bets " + str(p.bet)
                        elif (p.action == "Raise"):
                            action = "raises ${a} to ${b}".format(a = p.bet, b = float(p.bet) + float(summary.current_bet))
                        else:
                            action = "raises ${a} to ${b} and is all-in".format(a = p.bet, b = float(p.bet) + float(summary.current_bet))
                            
                    if (p.action == "Call"):
                        if (p.bet == summary.current_bet):
                            p.setEndState(True)
                            action = "calls" # Needs bet he's calling
                            p.money_committed = summary.current_bet
                            summary.pot += float(p.money_committed)
                            
                    if (p.action == "Check"):
                        p.setEndState(True)
                        action = "checks"
                    
                    if ((p.action) == "SB" or (p.action) == "BB" or (p.action) == "New"): 
                        p.money_committed = p.bet
                    
                    new_players.append(p)
                    
                # WHAT TO HAPPEN WHEN NOTHING HAS CHANGED????
                counter+=1
                summary.writeAction(p.name, action)
            else:
                next = p.seat
                output_players = new_players + players[counter:]
                output_players = orderWithNextPlayer(output_players, next)
                return output_players, summary
        else:
            new_players.append(p)
    
    return new_players, summary

def main():
            
    bu = None
    players = None
    summary = None
     
    while(True):
        new_bu = IT.findButton()
         
        if (bu == new_bu):
            players, summary = updateAction(players, summary)
        elif (bu is not None):
            time.sleep(1) # maybe not necessary 
            bu = new_bu
            players, summary = newHand(new_bu)

if __name__ == '__main__':
    main()
