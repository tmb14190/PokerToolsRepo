'''
Created on 17 Feb 2022

@author: Jack
'''
from collections import Counter

def translate_card_strength(card):
    if (card == "A"):
        return 13
    if (card == "K"):
        return 12
    if (card == "Q"):
        return 11
    if (card == "J"):
        return 10
    if (card == "T"):
        return 9
    else:
        return int(card) - 1

def translate_back_card_strength(card):
    
    if (card == 13):
        return "A"
    if (card == 13):
        return "K"
    if (card == 11):
        return "Q"
    if (card == 10):
        return "J"
    if (card == 9):
        return "T"
    else:
        return str(int(card) + 1)
    
def getHighestSF(s1, s2):
    
    s1O = []
    for i in s1[0].split():
        s1O.append(translate_card_strength(i))
    
    s2O = []   
    for i in s2[0].split():    
        s2O.append(translate_card_strength(i))
    
    s1O.sort(reverse = True)
    s2O.sort(reverse = True)
    
    if (translate_card_strength(s1O[1]) > translate_card_strength(s2O[1])):
        return s1
    else:
        return s2

def getHighestQuads(q1, q2):
    
    if (translate_card_strength(q1) > translate_card_strength(q2)):
        return q1
    else:
        return q2

def getHighestHouse(h1, h2):
    
    c1 = Counter(h1)
    c2 = Counter(h2)
    
    trips1 = c1.most_common(1)[0][0]
    trips2 = c2.most_common(1)[0][0]
    pair1 = c1.most_common(2)[1][0]
    pair2 = c2.most_common(2)[1][0]
    
    if (translate_card_strength(trips1) > translate_card_strength(trips2)):
        return h1
    elif (translate_card_strength(trips2) > translate_card_strength(trips1)):
        return h2
    else:
        if (translate_card_strength(pair1) > translate_card_strength(pair2)):
            return h1
        elif (translate_card_strength(pair2) > translate_card_strength(pair1)):
            return h2
        else:
            return "CHOP"

def getHighestHouses(houses):
    
    best = []
    tripsB = ""
    pairB = ""
    for h in houses:
        c = Counter(h)
        
        tripsI = c.most_common(1)[0][0]
        pairI = c.most_common(2)[1][0]
    
        if (len(best) == 0):
            best = h
            tripsB = tripsI
            pairB = pairI
            continue
        
        if (translate_card_strength(tripsI) > translate_card_strength(tripsB)):
            best = h
            tripsB = tripsI
            pairB = pairI
        else:
            if (translate_card_strength(pairI) > translate_card_strength(pairB) and translate_card_strength(tripsI) == translate_card_strength(tripsB)):
                best = h
                tripsB = tripsI
                pairB = pairI
    
    return best

def getHighestFlush(flushes):
    
    highestFlush = [0, 0, 0, 0, 0] 
    print (flushes)
    for i in flushes:
        hNos = []
        FH = i.split()
        for j in FH:
            hNos.append(translate_card_strength(j))
        hNos.sort(reverse = True)
        
        if (hNos[0] > highestFlush[0]):
            highestFlush = hNos    
        elif (hNos[0] == highestFlush[0]):
            if (hNos[1] > highestFlush[1]):
                highestFlush = hNos    
            elif (hNos[1] == highestFlush[1]):
                if (hNos[2] > highestFlush[2]):
                    highestFlush = hNos    
                elif (hNos[2] == highestFlush[2]):
                    if (hNos[3] > highestFlush[3]):
                        highestFlush = hNos    
        
    output = ""
    for i in highestFlush:
        output = output + " " + translate_back_card_strength(i)
    
    return output[1:]

def getHighestStraight(straights):
    return 0

def getHighestTrip(t1, t2):
    
    c1 = Counter(t1)
    c2 = Counter(t2)
    
    trips1 = c1.most_common(1)[0][0]
    trips2 = c2.most_common(1)[0][0]
    h1A = c1.most_common(3)[1][0]
    h1B = c1.most_common(3)[2][0]
    h2A = c2.most_common(3)[1][0]
    h2B = c2.most_common(3)[2][0]
    
    if (translate_card_strength(h1B) > translate_card_strength(h1A)):
        temp = h1A
        h1A = h1B
        h1B = temp
    
    if (translate_card_strength(h2B) > translate_card_strength(h2A)):
        temp = h2A
        h2A = h2B
        h2B = temp
    
    if (translate_card_strength(trips1) > translate_card_strength(trips2)):
        return t1
    elif (translate_card_strength(trips2) > translate_card_strength(trips1)):
        return t2
    else:
        if (translate_card_strength(h1A) > translate_card_strength(h2A)):
            return t1
        elif (translate_card_strength(h2A) > translate_card_strength(h1A)):
            return t2
        else:
            if (translate_card_strength(h1B) > translate_card_strength(h2B)):
                return t1
            elif (translate_card_strength(h2B) > translate_card_strength(h1B)):
                return t2
            else:
                return "CHOP"

def getHighestTrips(trips):
    
    best = []
    tripsB = ""
    h1B = ""
    h2B = ""
    
    for t in trips:
        c = Counter(t)
    
        trips = c.most_common(1)[0][0]
        h1 = c.most_common(3)[1][0]
        h2 = c.most_common(3)[2][0]
        
        if (translate_card_strength(h2) > translate_card_strength(h1)):
            temp = h1
            h1 = h2
            h2 = temp
        
        if (len(best) == 0):
            tripsB = trips
            h1B = h1
            h2B = h2
            best = t
            continue

        if (translate_card_strength(trips) > translate_card_strength(tripsB)):
            tripsB = trips
            h1B = h1
            h2B = h2
            best = t
        else:
            if (translate_card_strength(h1) > translate_card_strength(h1B) and translate_card_strength(trips) == translate_card_strength(tripsB)):
                tripsB = trips
                h1B = h1
                h2B = h2
                best = t
            else:
                if (translate_card_strength(h2) > translate_card_strength(h2B) and translate_card_strength(trips) == translate_card_strength(tripsB) and translate_card_strength(h1) == translate_card_strength(h1B)):
                    tripsB = trips
                    h1B = h1
                    h2B = h2
                    best = t
    
    return best

def getHighestTwoPair(tp1, tp2):
    
    c1 = Counter(tp1)
    c2 = Counter(tp2)
    
    p1A = c1.most_common(1)[0][0]
    p2A = c2.most_common(1)[0][0]
    p1B = c1.most_common(2)[1][0]
    p2B = c2.most_common(2)[1][0]
    h1 = c1.most_common(3)[2][0]
    h2 = c2.most_common(3)[2][0]
    
    if (translate_card_strength(p1B) > translate_card_strength(p1A)):
        temp = p1A
        p1A = p1B
        p1B = temp
    
    if (translate_card_strength(p2B) > translate_card_strength(p2A)):
        temp = p2A
        p2A = p2B
        p2B = temp
    
    if (translate_card_strength(p1A) > translate_card_strength(p2A)):
        return tp1
    elif (translate_card_strength(p2A) > translate_card_strength(p1A)):
        return tp2
    else:
        if (translate_card_strength(p1B) > translate_card_strength(p2B)):
            return tp1
        elif (translate_card_strength(p2B) > translate_card_strength(p1B)):
            return tp2
        else:
            if (translate_card_strength(h1) > translate_card_strength(h2)):
                return tp1
            elif (translate_card_strength(h2) > translate_card_strength(h1)):
                return tp2
            else:
                return "CHOP"

def getHighestTwoPairs(two_pair):
    
    best = []
    tp1B = ""
    tp2B = ""
    hB = ""
    
    for tp in two_pair:
        c = Counter(tp)
    
        tp1 = c.most_common(1)[0][0]
        tp2 = c.most_common(2)[1][0]
        h = c.most_common(3)[2][0]
        
        if (translate_card_strength(tp2) > translate_card_strength(tp1)):
            temp = tp1
            tp1 = tp2
            tp2 = temp
        
        if (len(best) == 0):
            tp1B = tp1
            tp2B = tp2
            hB = h
            best = tp
            continue

        if (translate_card_strength(tp1) > translate_card_strength(tp1B)):
            tp1B = tp1
            tp2B = tp2
            hB = h
            best = tp
        else:
            if (translate_card_strength(tp2) > translate_card_strength(tp2B) and translate_card_strength(tp1) == translate_card_strength(tp1B)):
                tp1B = tp1
                tp2B = tp2
                hB = h
                best = tp
            else:
                if (translate_card_strength(h) > translate_card_strength(hB) and translate_card_strength(tp1) == translate_card_strength(tp1B) and translate_card_strength(tp2) == translate_card_strength(tp2B)):
                    tp1B = tp1
                    tp2B = tp2
                    hB = h
                    best = tp
    
    return best

def getHighestPair(pair1, pair2):
    
    c1 = Counter(pair1)
    c2 = Counter(pair2)
    
    p1 = c1.most_common(1)[0][0]
    h1A = c1.most_common(2)[1][0]
    h1B = c1.most_common(3)[2][0]
    h1C = c1.most_common(4)[3][0]
    p2 = c2.most_common(1)[0][0]
    h2A = c2.most_common(2)[1][0]
    h2B = c2.most_common(3)[2][0]
    h2C = c2.most_common(4)[3][0]
    
    for i in range(0, 2):
        if (translate_card_strength(h1C) > translate_card_strength(h1B)):
            temp = h1B
            h1B = h1C
            h1C = temp
        if (translate_card_strength(h2A) > translate_card_strength(h1A)):
            temp = h1A
            h1A = h1B
            h1B = temp
        if (translate_card_strength(h2C) > translate_card_strength(h2B)):
            temp = h2B
            h2B = h2C
            h2C = temp
        if (translate_card_strength(h2B) > translate_card_strength(h2A)):
            temp = h2A
            h2A = h2B
            h2B = temp

    
    if (translate_card_strength(p1) > translate_card_strength(p2)):
        return pair1
    elif (translate_card_strength(p2) > translate_card_strength(p1)):
        return pair2
    else:
        if (translate_card_strength(h1A) > translate_card_strength(h2A)):
            return pair1
        elif (translate_card_strength(h2A) > translate_card_strength(h1A)):
            return pair2
        else:
            if (translate_card_strength(h1B) > translate_card_strength(h2B)):
                return pair1
            elif (translate_card_strength(h2A) > translate_card_strength(h1B)):
                return pair2
            else:
                if (translate_card_strength(h1C) > translate_card_strength(h2C)):
                    return pair1
                elif (translate_card_strength(h2C) > translate_card_strength(h1C)):
                    return pair2
                else:
                    return "CHOP"

def getHighestPairs(pair):
    
    best = []
    pB = ""
    h1B = ""
    h2B = ""
    h3B = ""
    
    for p in pair:
        c = Counter(p)
    
        pa = c.most_common(1)[0][0]
        h1 = c.most_common(2)[1][0]
        h2 = c.most_common(3)[2][0]
        h3 = c.most_common(4)[3][0]
        
        for i in range(0, 2):
            if (translate_card_strength(h3) > translate_card_strength(h2)):
                temp = h2
                h2 = h3
                h3 = temp
            if (translate_card_strength(h2) > translate_card_strength(h1)):
                temp = h1
                h1 = h2
                h2 = temp
                
        
        if (len(best) == 0):
            best = p
            pB = pa
            h1B = h1
            h2B = h2
            h3B = h3
            continue

        if (translate_card_strength(pa) > translate_card_strength(pB)):
            best = p
            pB = pa
            h1B = h1
            h2B = h2
            h3B = h3
        else:
            if (translate_card_strength(h1) > translate_card_strength(h1B) and translate_card_strength(pa) == translate_card_strength(pB)):
                best = p
                pB = pa
                h1B = h1
                h2B = h2
                h3B = h3
            else:
                if (translate_card_strength(h2) > translate_card_strength(h2B) and translate_card_strength(h1) == translate_card_strength(h1B)and translate_card_strength(pa) == translate_card_strength(pB)):
                    best = p
                    pB = pa
                    h1B = h1
                    h2B = h2
                    h3B = h3
                else:
                    if (translate_card_strength(h3) > translate_card_strength(h3B) and translate_card_strength(h2) == translate_card_strength(h2B) and translate_card_strength(h1) == translate_card_strength(h1B) and translate_card_strength(pa) == translate_card_strength(pB)):
                        best = p
                        pB = pa
                        h1B = h1
                        h2B = h2
                        h3B = h3
    
    return best

def getHighestHighHand(h1, h2):
    
    #output1 = translate_card_strength(h1[0]) + translate_card_strength(h1[1]) + translate_card_strength(h1[2]) + translate_card_strength(h1[3]) + translate_card_strength(h1[4])
    #output2 = translate_card_strength(h2[0]) + translate_card_strength(h2[1]) + translate_card_strength(h2[2]) + translate_card_strength(h2[3]) + translate_card_strength(h2[4])
    
    if (h1[0] > h2[0]):
        return h1
    elif (h2[0] > h1[0]):
        return h2
    
    if (h1[1] > h2[1]):
        return h1
    elif (h2[1] > h1[1]):
        return h2

    if (h1[2] > h2[2]):
        return h1
    elif (h2[2] > h1[2]):
        return h2

    if (h1[3] > h2[3]):
        return h1
    elif (h2[3] > h1[3]):
        return h2

    if (h1[4] > h2[4]):
        return h1
    elif (h2[4] > h1[4]):
        return h2
    
    return "CHOP"
    

def getStraights():
    
    s = []
    s.append([13, 12, 11, 10, 9])
    s.append([12, 11, 10, 9, 8])
    s.append([11, 10, 9, 8, 7])
    s.append([10, 9, 8, 7, 6])
    s.append([9, 8, 7, 6, 5])
    s.append([8, 7, 6, 5, 4])
    s.append([7, 6, 5, 4, 3])
    s.append([6, 5, 4, 3, 2])
    s.append([5, 4, 3, 2, 1])
    s.append([13, 4, 3, 2, 1])
    
    return s
    
    
