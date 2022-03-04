'''
Created on 14 Feb 2022

@author: Jack
'''
import OmahaEquityCalculations.hand_comparator as HC
import OmahaEquityCalculations.board_type as BT
from collections import Counter

def straightFlush(hand, board):
    
    flushes = flush(hand, board, True)
    
    SF = []
    hard_straights = HC.getStraights()
    for i in flushes:
        
        toOrder = []
        for j in i.split():
            toOrder.append(HC.translate_card_strength(j))
        
        toOrder.sort(reverse = True)
        
        if (toOrder in hard_straights):
            SF.append(i)
    
    if (len(SF) > 1):
        SF = HC.getHighestSF(SF[0], SF[1])
    elif (len(SF) == 1):
        return SF
    else:
        return False

def quads(hand, board):
    
    cards = [board[0], board[3], board[6], board[9], board[12]]
    
    counter = Counter(cards)
    
    paired = []
    trips = "F"
    quad = []
    
    if (counter.most_common(1)[0][1] == 3):
        trips = counter.most_common(1)[0][0]
    
    if (trips in hand):
        quad.append(trips)
    
    for i in range(0, 2):
        if (counter.most_common(2)[i][1] == 2):
            paired.append(counter.most_common(2)[i][0])
    
    for i in paired:
        if (hand.count(i) > 1):
            quad.append(i)
    
    if (len(quad) > 1):
        return HC.getHighestQuads(quad[0], quad[1])
    elif (len(quad) == 1):
        return quad[0]
    
    return False

def houseOLD(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    cards = [board[0], board[3], board[6], board[9], board[12]]
    
    counterB = Counter(cards)
    counterH = Counter([hand[0], hand[3], hand[6], hand[9]])
    
    paired = []
    trips = ""
    house = []
    
    if (counterB.most_common(1)[0][1] == 3):
        trips = counterB.most_common(1)[0][0] + counterB.most_common(1)[0][0] + counterB.most_common(1)[0][0]
    
    if (trips != ""):
        if (len(set([hand[0], hand[3], hand[6], hand[9]])) <= 3):
            house.append(trips + counterH.most_common(1)[0][0] + counterH.most_common(1)[0][0])
            
            if (counterH.most_common(2)[1][1] == 2):
                house.append(trips + counterH.most_common(2)[1][0] + counterH.most_common(2)[1][0])
    
    # We're here
    
    for i in range(0, 2):
        if (counterB.most_common(2)[i][1] == 2):
            paired.append(counterB.most_common(2)[i][0])
    
    remainingB = cards
    remainingH = [hand[0], hand[3], hand[6], hand[9]]
    trip = []
    for i in paired:
        if (hand.count(i) > 0):
            trip.append(i)
            remainingB.remove(i)
            remainingB.remove(i)
            remainingH.remove(i)
    
    
    pair = []
    for i in remainingH:
        if (i in remainingB):
            pair.append(i)
    
    if (len(pair) > 0 and len(trip) > 0):
        for i in trip:
            for j in pair:
                house.append(i + i + i + j + j)
    
    if (len(house) > 1):
        return HC.getHighestHouses(house)
    elif (len(house) == 1):
        return house[0]
    
    return False

def house(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    board_combos = BT.getBoardCombosUnaltered(board)
    
    houses = []
    
    for i in hand_combos:
        h = [i[0], i[3]]
        
        for j in board_combos:
            
            c = Counter(j + h)
            
            if (c.most_common(2)[0][1] == 3 and c.most_common(2)[1][1] == 2):
                houses.append(c.most_common(2)[0][0] + c.most_common(2)[0][0] + c.most_common(2)[0][0] + c.most_common(2)[1][0] + c.most_common(2)[1][0])
    
    if (len(houses) > 1):
        return HC.getHighestHouses(houses)
    elif (len(houses) == 1):
        return houses[0]
    
    return False

def flush(hand, board, SF):
    
    suits = [board[1], board[4], board[7], board[10], board[13]]
    hand_combos = BT.getHandCombos(hand)
    
    flushHand = []
    for h in hand_combos:
        if (h[1] == h[4]):
            if (suits.count(h[1]) >= 3):
                indices = [i for i, x in enumerate(board) if x == h[1]]
                flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[1]-1] + " " + board[indices[2]-1])
                
                if (len(indices) >= 4):
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[1]-1] + " " + board[indices[3]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[2]-1] + " " + board[indices[3]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[1]-1] + " " + board[indices[2]-1] + " " + board[indices[3]-1])
                
                if (len(indices) == 5):
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[1]-1] + " " + board[indices[4]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[2]-1] + " " + board[indices[2]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[0]-1] + " " + board[indices[3]-1] + " " + board[indices[4]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[1]-1] + " " + board[indices[2]-1] + " " + board[indices[4]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[1]-1] + " " + board[indices[3]-1] + " " + board[indices[4]-1])
                    flushHand.append(h[0] + " " + h[3] + " " + board[indices[2]-1] + " " + board[indices[3]-1] + " " + board[indices[4]-1])
    
    if (SF == True):
        return flushHand
    
    if (len(flushHand) > 1):
        highestFlush = HC.getHighestFlush(flushHand)
        return highestFlush
    elif (len(flushHand) == 1):
        return flushHand[0]
    else:
        return False

def straight(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    
    straightHands = []
    hard_straights = HC.getStraights()
    for h in hand_combos:
        if (h[0] != h[3]):
            
            board_combos = BT.getBoardCombos(board)
            
            for b in board_combos:
                x = (b + [HC.translate_card_strength(h[0]), HC.translate_card_strength(h[3])])
                x.sort(reverse = True)
                print (x)
                if (x in hard_straights):
                    straightHands.append(x)
    
    if (len(straightHands) > 0):                
        max = 13    
        bestStraight = []
        for i in straightHands:
            if hard_straights.index(i) < max:
                max = hard_straights.index(i)
                bestStraight = i
        return bestStraight
    
    return False

def trips(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    board_combos = BT.getBoardCombosUnaltered(board)
    
    trips = []
    
    for i in hand_combos:
        h = [i[0], i[3]]
        
        for j in board_combos:
            
            c = Counter(j + h)
            
            
            if (c.most_common(1)[0][1] == 3 and c.most_common(2)[1][1] == 1):
                trips.append(c.most_common(2)[0][0] + c.most_common(2)[0][0] + c.most_common(2)[0][0] + c.most_common(2)[1][0] + c.most_common(3)[2][0])
    
    if (len(trips) > 1):
        return HC.getHighestTrips(trips)
    elif (len(trips) == 1):
        return trips[0]
    
    return False

def twoPair(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    board_combos = BT.getBoardCombosUnaltered(board)
    
    twoPairs = []
    
    for i in hand_combos:
        h = [i[0], i[3]]
        
        for j in board_combos:
            
            c = Counter(j + h)
            
            if (c.most_common(1)[0][1] == 2 and c.most_common(2)[1][1] == 2):
                twoPairs.append(c.most_common(2)[0][0] + c.most_common(2)[0][0] + c.most_common(2)[1][0] + c.most_common(2)[1][0] + c.most_common(3)[2][0])
    
    if (len(twoPairs) > 1):
        return HC.getHighestTwoPairs(twoPairs)
    elif (len(twoPairs) == 1):
        return twoPairs[0]
    
    return False

def pair(hand, board):
    
    hand_combos = BT.getHandCombos(hand)
    board_combos = BT.getBoardCombosUnaltered(board)
    
    pairs = []
    
    for i in hand_combos:
        h = [i[0], i[3]]
        
        for j in board_combos:
            
            c = Counter(j + h)
            
            if (c.most_common(1)[0][1] == 2 and c.most_common(2)[1][1] == 1):
                pairs.append(c.most_common(1)[0][0] + c.most_common(1)[0][0] + c.most_common(2)[1][0] + c.most_common(3)[2][0] + c.most_common(4)[3][0])
    
    if (len(pairs) > 1):
        return HC.getHighestPairs(pairs)
    elif (len(pairs) == 1):
        return pairs[0]
    
    return False

def highCard(hand, board):
    
    orderH = []
    for i in hand.split():
        orderH.append(HC.translate_card_strength(i[0]))
    
    orderB = []
    for i in board.split():
        orderB.append(HC.translate_card_strength(i[0]))
    
    orderH.sort(reverse = True)
    orderB.sort(reverse = True)
    
    high = orderH[0:2] + orderB[0:3]
    
    high.sort(reverse = True)
    
    return high

def getWinner(hand1, hand2, board):
    # Compare speeds with and without checking if hands are possible
    
    if (BT.flushPossible(board)):
        s1 = straightFlush(hand1, board)
        s2 = straightFlush(hand2, board)
        
        if (s1 != False or s2 != False):
            if (s2 == False):
                return True
            elif (s1 == False):
                return False
            elif (s1 == HC.getHighestSF(s1, s2)):
                print (s1)
                return True
            else:
                print (s2)
                return False
        
    if (BT.pairedBoard(board)):
        q1 = quads(hand1, board)    
        q2 = quads(hand2, board)   
        if (q1 != False or q2 != False):
            if (q2 == False):
                return True
            elif (q1 == False):
                return False
            elif (q1 == HC.getHighestQuads(q1, q2)):
                print (q1)
                return True
            else:
                print (q2)
                return False
         
        h1 = house(hand1, board)    
        h2 = house(hand2, board)   
        if (h1 != False or h2 != False):
            if (h2 == False):
                return True
            elif (h1 == False):
                return False
            elif (h1 == HC.getHighestHouse(h1, h2)):
                print (h1)
                return True
            else:
                print (h2)
                return False
   
    if (BT.flushPossible(board)):
        f1 = flush(hand1, board, False)
        f2 = flush(hand2, board, False)
        if (f1 != False or f2 != False):
            if (f2 == False):
                return True
            elif (f1 == False):
                return False
            elif (f1 == HC.getHighestFlush([f1, f2])):
                return True
            else:
                return False
     
    if (BT.straightPossible(board)):
        s1 = straight(hand1, board)
        s2 = straight(hand2, board)
        hard_straights = HC.getStraights()
        if (s1 != False or s2 != False):
            if (s2 == False):
                return True
            elif (s1 == False):
                return False
            elif (hard_straights.index(s1) < hard_straights.index(s2)):
                return True
            elif (hard_straights.index(s2) < hard_straights.index(s1)):
                return False
            else:
                return ("CHOP")
    
    t1 = trips(hand1, board)
    t2 = trips(hand2, board)
    if (t1 != False or t2 != False):
        if (t2 == False):
            return True
        elif (t1 == False):
            return False
        elif (t1 == HC.getHighestTrip(t1, t2)):
            print (t1)
            return True
        elif (t2 == HC.getHighestTrip(t1, t2)):
            print (t2)
            return False
    
    tp1 = twoPair(hand1, board)
    tp2 = twoPair(hand2, board)
    if (tp1 != False or tp2 != False):
        if (tp2 == False):
            return True
        elif (tp1 == False):
            return False
        elif (tp1 == HC.getHighestTwoPair(tp1, tp2)):
            print (tp1)
            return True
        elif (tp2 == HC.getHighestTwoPair(tp1, tp2)):
            print (tp2)
            return False
    
    p1 = pair(hand1, board)
    p2 = pair(hand2, board)
    if (p1 != False or p2 != False):
        if (p2 == False):
            return True
        elif (p1 == False):
            return False
        elif (p1 == HC.getHighestPair(p1, p2)):
            print (p1)
            return True
        elif (p2 == HC.getHighestPair(p1, p2)):
            print (p2)
            return False
    
    h1 = highCard(hand1, board)
    h2 = highCard(hand2, board)
    if (h1 != False or h2 != False):
        if (h2 == False):
            return True
        elif (h1 == False):
            return False
        elif (h1 == HC.getHighestHighHand(h1, h2)):
            print (h1)
            return True
        elif (h2 == HC.getHighestHighHand(h1, h2)):
            print (h2)
            return False
        
    #print ("tie")
    return ("CHOP")