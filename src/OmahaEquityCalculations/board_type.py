'''
Created on 15 Feb 2022

@author: Jack
'''
import OmahaEquityCalculations.hand_comparator as HC

def getBoardCombos(board):
    
    translated = []
    for i in board.split():
        translated.append(HC.translate_card_strength(i[0]))
    
    translated.sort(reverse = True)
    
    output = []
    output.append([translated[0], translated[1], translated[2]])
    output.append([translated[0], translated[1], translated[3]])
    output.append([translated[0], translated[1], translated[4]])
    output.append([translated[0], translated[2], translated[3]])
    output.append([translated[0], translated[2], translated[4]])
    output.append([translated[0], translated[3], translated[4]])
    output.append([translated[1], translated[2], translated[3]])
    output.append([translated[1], translated[2], translated[4]])
    output.append([translated[1], translated[3], translated[4]])
    output.append([translated[2], translated[3], translated[4]])
    
    return output

def getBoardCombosUnaltered(board):
    
    b = []
    for i in board.split():
        b.append(i[0])
    
    
    output = []
    output.append([b[0], b[1], b[2]])
    output.append([b[0], b[1], b[3]])
    output.append([b[0], b[1], b[4]])
    output.append([b[0], b[2], b[3]])
    output.append([b[0], b[2], b[4]])
    output.append([b[0], b[3], b[4]])
    output.append([b[1], b[2], b[3]])
    output.append([b[1], b[2], b[4]])
    output.append([b[1], b[3], b[4]])
    output.append([b[2], b[3], b[4]])
    
    return output

def getHandCombos(hand):
    
    hand = hand.split()
    
    h1 = hand[0] + " " + hand[1]
    h2 = hand[0] + " " + hand[2]
    h3 = hand[0] + " " + hand[3]
    h4 = hand[1] + " " + hand[2]
    h5 = hand[1] + " " + hand[3]
    h6 = hand[2] + " " + hand[3]
    
    return [h1, h2, h3, h4, h5, h6]

def flushPossible(board):
    suits = [board[1], board[4], board[7], board[10], board[13]]
    if (len(set(suits)) <= 3):
        for i in suits:
            if (suits.count(suits[0]) >= 3):
                return True
            if (suits.count(suits[1]) >= 3):
                return True
            if (suits.count(suits[2]) >= 3):
                return True
            
    return False

def pairedBoard(board):
    if (len(set([board[0], board[3], board[6], board[9], board[12]])) <= 4):
        return True
    else: 
        return False

''' Optimising this could be pretty useful, a lot could be done '''
def straightPossible(board):
    
    ordered = []
    for i in board.split():
        ordered.append(HC.translate_card_strength(i[0]))
    ordered.sort(reverse = True)
    
    # Utilising these could improve performance
#     if (abs(ordered[0] - ordered[1]) > 2):
#         print ("Highest card cant be part of the straight")
#     if (abs(ordered[3] - ordered[4]) > 2):
#         print ("Lowest card cant be part of the straight")

    if (((ordered[0] - ordered[1]) + (ordered[1] - ordered[2]) < 5) and ordered[0] != ordered[1] and ordered[0] != ordered[2] and ordered[1] != ordered[2]) :
        return True
    if (((ordered[0] - ordered[1]) + (ordered[1] - ordered[3]) < 5) and ordered[0] != ordered[1] and ordered[0] != ordered[3] and ordered[1] != ordered[3]):
        return True
    if (((ordered[0] - ordered[1]) + (ordered[1] - ordered[4]) < 5) and ordered[0] != ordered[1] and ordered[0] != ordered[4] and ordered[1] != ordered[4]):
        return True
    if (((ordered[0] - ordered[2]) + (ordered[2] - ordered[3]) < 5) and ordered[0] != ordered[2] and ordered[0] != ordered[3] and ordered[2] != ordered[3]):
        return True
    if (((ordered[0] - ordered[2]) + (ordered[2] - ordered[4]) < 5) and ordered[0] != ordered[2] and ordered[0] != ordered[4] and ordered[2] != ordered[4]):
        return True
    if (((ordered[0] - ordered[3]) + (ordered[3] - ordered[4]) < 5) and ordered[0] != ordered[3] and ordered[0] != ordered[4] and ordered[3] != ordered[4]):
        return True
    if (((ordered[1] - ordered[2]) + (ordered[2] - ordered[3]) < 5) and ordered[1] != ordered[2] and ordered[1] != ordered[3] and ordered[2] != ordered[3]):
        return True
    if (((ordered[1] - ordered[2]) + (ordered[2] - ordered[4]) < 5) and ordered[1] != ordered[2] and ordered[1] != ordered[4] and ordered[2] != ordered[4]):
        return True
    if (((ordered[1] - ordered[3]) + (ordered[3] - ordered[4]) < 5) and ordered[1] != ordered[3] and ordered[1] != ordered[4] and ordered[3] != ordered[4]):
        return True
    if (((ordered[2] - ordered[3]) + (ordered[3] - ordered[4]) < 5) and ordered[2] != ordered[3] and ordered[2] != ordered[4] and ordered[3] != ordered[4]):
        return True
    
    return False