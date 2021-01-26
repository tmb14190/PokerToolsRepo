'''
Created on 26 Oct 2020

@author: jackm
'''
from BrosHH.PioInterface import PioInterface

class Pio:
    
    ePot = 0
    pot = 0
    current_bet = 0
    street = 0
    action_on = 0
    bu = 0
    bb = 0
    board = ""
    hand = ""
    pre = []
    flop = []
    turn = []
    river = []
    we_in = False
    setup = []
    go_again = False
    open = False
    waiting_flag = False
    callWarn = False
    dgafWarn = False
    our_position = ""
    
    # get the flop up pre = (p.position, action, p.bet)
    def init(self):
        raisers = []
        from_rfi = []
        print ("initialising pio")
        print (self.pre)
        
        for i in range(0, len(self.pre)):
            if (self.pre[i][1] == "B"):
                from_rfi = self.pre[i:]
                if (len(from_rfi) > 1):
                    raisers.append(0)
                break
        for i in range(1, len(from_rfi)):
            if (from_rfi[i][1] == "B"):
                raisers.append(i)
        
        if (len(raisers) == 1): # for rfi sims
            
            if (len(from_rfi) < 4): # only pull up a rfi sim if 1 or 2 calls
                if (self.our_position == from_rfi[0][0] or self.our_position == from_rfi[1][0]): # only open sim if we're involved
                    self.setup.append([PioInterface(), "RFI", from_rfi[0][0], from_rfi[1][0]])
                if (len(from_rfi) == 3):
                    if (self.our_position == from_rfi[0][0] or self.our_position == from_rfi[2][0]):
                        self.setup.append([PioInterface(), "RFI", from_rfi[0][0], from_rfi[2][0]])
                        
        elif (len(raisers) == 2): # for 3bet sims
            
            for action in from_rfi[raisers[1]+1:]: # go through all actions after 3bet
                if (from_rfi[raisers[0]][0] == action[0]):
                    if (self.our_position == from_rfi[raisers[0]][0] or self.our_position == from_rfi[raisers[1]][0]):
                        self.setup.append([PioInterface(), "3Bet", from_rfi[raisers[0]][0], from_rfi[raisers[1]][0]])
        

        for s in self.setup:
            s[0].openBoard(s[1], s[2], s[3], self.board, self.hand)
            print ("Open {a} {b} vs {c}".format(a = s[1], b = s[2], c = s[3]))
    
    def addBoardCard(self, card):
        for s in self.setup:
            self.open = True
            s[0].addBoardCard(card)
            
    def getPioSize(self, size, first):
        pio_size = 0
        if (size != 0 and first):
            if (self.street == 1):
                # uses 33, 66
                a = (size / self.pot)*100 - 33
                b = (size / self.pot)*100 - 66
                
                if (abs(a) > abs(b)):
                    print ("Bet 66%")
                    pio_size = 1
                else:
                    print ("Bet 33%")
                    pio_size = 2
                
            if (self.street == 2):
                # uses 40, 80
                a = (size / self.pot)*100 - 40
                b = (size / self.pot)*100 - 80
                
                if (abs(a) > abs(b)):
                    print ("Bet 80%")
                    pio_size = 1
                else:
                    print ("Bet 40%")
                    pio_size = 2
            if (self.street == 3):
                # uses 50, 100
                a = (size / self.pot)*100 - 50
                b = (size / self.pot)*100 - 100
                
                if (abs(a) > abs(b)):
                    print ("Bet 100%")
                    pio_size = 1
                else:
                    print ("Bet 50%")
                    pio_size = 2
        elif (size != 0 and not first):
            print ("Raise")
            pio_size = 3
        return pio_size

    def updateAction(self, position, action, size):
        
        if (self.street == 0):
            self.pre.append([position, action, size])
        else:
            id = 0
            for s in self.setup:
                if (position == s[2] or position  == s[3]):
                    if (size == -1):
                        self.closePioID(id)
                        id = 0
                    else:
                        pio_size = self.getPioSize(size, s[0].first)
                        s[0].addAction(pio_size)
                    id += 1
    
    def closeAllPio(self):
        for i in range(0, len(self.setup)):
            self.setup[0][0].closePio()
            self.setup.pop(0)
        self.open = False
    
    def closePioID(self, id):
        self.setup[id][0].closePio()
        self.setup.pop(id)
        if (len(self.setup) == 0):
            self.open = False



