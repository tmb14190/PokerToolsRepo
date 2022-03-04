'''
Created on 17 Feb 2022

@author: Jack
'''
import random
import OmahaEquityCalculations.poker_rules as PR
import OmahaEquityCalculations.hand_comparator as HC

def getCardOptions():
    cardOps = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    suitOps = ["h", "c", "d", "s"]
    
    return cardOps, suitOps

def getAllCards():
    allCards= ["Ah", "Kh", "Qh", "Jh", "Th", "9h", "8h", "7h", "6h", "5h", "4h", "3h", "2h",
               "Ac", "Kc", "Qc", "Jc", "Tc", "9c", "8c", "7c", "6c", "5c", "4c", "3c", "2c",
               "Ad", "Kd", "Qd", "Jd", "Td", "9d", "8d", "7d", "6d", "5d", "4d", "3d", "2d",
               "As", "Ks", "Qs", "Js", "Ts", "9s", "8s", "7s", "6s", "5s", "4s", "3s", "2s"]
    
    return allCards
    

def getRandomHand(freeCards):
    cards = []
    while (len(cards) != 4):
        c = random.randint(0, len(freeCards)-1)
        
        cards.append(freeCards[c])
        
        del freeCards[c]
        
    
    return cards[0] + " " + cards[1] + " " + cards[2] + " " + cards[3], freeCards

def getRandomBoard(freeCards, override):
    street = random.randint(2, 4)
    
    if (street == 2 and override == False):
        return "", []
    
    cards = []
    
    while (len(cards) != street):
        c = random.randint(0, len(freeCards)-1)
        
        cards.append(freeCards[c])
        
        del freeCards[c]
        
    board = ""        
    for i in cards:
        board = board + " " + i
    
    return board[1:], freeCards

def runOutBoard(board, freeCards):
    cards = []
    b = board.split()
    
    tempCards = freeCards.copy()
    
    while (len(b) != 5):
        c = random.randint(0, len(tempCards)-1)
        
        b.append(tempCards[c])
        
        del tempCards[c]
        
    out = ""        
    for i in b:
        out = out + " " + i
    
    return out[1:]

def runOutTurnRiver(board, freeCards):
    cards = []
    b = board.split()
    
    while (len(b) != 5):
        c = random.randint(0, len(freeCards)-1)
        
        b.append(freeCards[c])
        
        del freeCards[c]
        
    out = ""        
    for i in b:
        out = out + " " + i
    
    return out[1:]

def runOutRiver(board, freeCards):
    cards = []
    b = board.split()
    
    while (len(b) != 5):
        c = random.randint(0, len(freeCards)-1)
        
        b.append(freeCards[c])
        
        del freeCards[c]
        
    out = ""        
    for i in b:
        out = out + " " + i
    
    return out[1:]

def runEquity(hand1, hand2, board):
    h1 = 0
    h2 = 0
    
    freeCards = getAllCards()
    
    hand1 = "As Ac Ks Kc"
    hand2 = "8h 9d 7h 6d"
    board = ""
    
    freeCards = [i for i in freeCards if i not in hand1.split()]
    freeCards = [i for i in freeCards if i not in hand2.split()]
    freeCards = [i for i in freeCards if i not in board.split()]
    
    freeCopy = freeCards.copy()
    
    ''' Define Accuracy '''
    simulations = 1000
    
    for i in range(0, simulations):
        if (len(board.split()) == 4):
            b = runOutRiver(board, freeCards)
        elif (len(board.split()) == 3):
            b = runOutBoard(board, freeCards)
        elif (len(board.split()) == 0):
            print ("LEN")
            print (len(freeCards))
            b, freeCards = getRandomBoard(freeCards, True)
            b = runOutBoard(board, freeCards)
            freeCards = freeCopy.copy()
        print (b)
        #print (board)
        result = PR.getWinner(hand1, hand2, b)
        if (result == True):
            print ("Hand 1 Wins!")
            h1 += 1
        elif (result == False):
            h2 += 1
            print ("Hand 2 Wins!")
        else:
            print (result)
        if (len(freeCards) == 0):
            break
    
    e1 = (h1 / (h1 + h2)) * 100
    e2 = (h2 / (h1 + h2)) * 100
    
    print (h1)
    print (h2)
    
    print (e1)
    print (e2)
    
    return e1, e2

def runEquity3ways(hand1, hand2, hand3, board):
    return 0

def runEquity4ways(hand1, hand2, hand3, hand4, board):
    return 0

def runRandom():
    
    freeCards = getAllCards()
    
    hand1, freeCards = getRandomHand(freeCards)
    hand2, freeCards = getRandomHand(freeCards)
    board, freeCards = getRandomBoard(freeCards, False)
    
    equity1, equity2 = runEquity(hand1, hand2, board)
    
    return hand1, hand2, board, equity1, equity2

