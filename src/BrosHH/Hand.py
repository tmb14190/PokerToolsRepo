'''
Created on 7 Oct 2020

@author: jackm
'''
import datetime
from pytz import timezone
import shutil
from io import StringIO

class HandHistory:
    
    hh = StringIO()
    pot = 0
    current_bet = 0
    street = 0
    action_on = 0
    bu = 0
    bb = 0
    board = ""
    
    '''
    bb - float of big blind amount
    players - list of players class
    '''
    def __init_(self):
        pass
    
    '''
    
    NEEDS DOING
    
    '''
    def getHandNumber(self):
        self.number = "0000000000001" # something like that idfk
        
    '''
    Writes up until Hole Cards
    float bb - big blind
    Player[] players - list of players
    '''
    def writeInit(self, bb, players):
        
        self.pot = float(bb)*1.5
        self.bb = bb
        
        number = self.getHandNumber()
        
        try:
            self.bu = players[-2].seat
        except:
            self.bu = players[-1].seat # THIS WORK?

        
        self.hh.write("\n")
        wet = datetime.datetime.now()
        et = datetime.datetime.now(timezone('EST'))
        self.hh.write("PokerBros Hand #{a}: Hold'em No Limit (${b:.2f}/${c:.2f}) - {d} WET [{e} ET]\n".format(a = number, b = bb/2, c = bb, d = str(wet)[:-7], e = str(et)[:-13]))
        self.hh.write("Table '09OctAria880305184943241' 6-max Seat #{a} is the button\n".format(a = self.bu))
        for i in players:
            self.hh.write("Seat {a}: {b} (${c} in chips)\n".format(a = i.seat, b = i.name, c = i.stack))
        self.hh.write("{a}: posts small blind ${b:.2f}\n".format(a = players[len(players)-2].name, b = bb/2))
        self.hh.write("{a}: posts big blind ${b:.2f}\n".format(a = players[len(players)-1].name, b = bb))
    
    def writePost(self, player):
        self.hh.write("{a}: posts big blind ${b:.2f}\n".format(a = player.name, b = self.bb))
        self.pot += self.bb
    
    '''
    string hand - 5 characters e.g. "As Ac"
    '''
    def writeHoleCards(self, hand):
        self.hh.write("*** HOLE CARDS ***\n")
        self.hh.write("Dealt to Homie [{a}]\n".format(a = hand))
    
    '''
    NEEDS DOING
    
    SHOULD MAYBE BE REFACTORED SO THIS CLASS CONTAINS ALL STRING MANIPULATION
    string name - name of player
    string action - action in full, e.g. "folds", "calls $1.78", "bets $0.21", "raises 0.10 to $0.20"
    action is full action in string
    '''
    def writeAction(self, name, action, bet):
        self.hh.write("{a}: {b}\n".format(a = name, b = action))
    
    '''
    string board - just the full current board string e.g. As Ac Ad, or 2d 2s 2h 2c, or As Ks Qs Js Ts
    '''
    def writeBoard(self, board):
        self.board = board
        if (len(board) == 8):
            self.hh.write("*** FLOP *** [{a}]\n".format(a = board))
        elif (len(board) == 11):
            self.hh.write("*** TURN *** [{a}] [{b}] \n".format(a = board[:-3], b = board[-2:] ))
        elif (len(board) == 14):
            self.hh.write("*** RIVER *** [{a}] [{b}] [{c}]\n".format(a = board[:-6], b = board[-5:-4], c = board[-2:]))
    
    '''
    Player player - player with uncalled bet
    float bet - amount being returned to player
    '''
    def writeUncalledBet(self, bet, player):
        self.hh.write("Uncalled bet (${a}) returned to {b}\n".format(a = bet, b = player.name))
    
    '''
    float pot - size of pot
    Player winner - position of player who won pot
    Player[] players - list of players who got to showdown
    '''
    def showdown(self, pot, winner, player):
        self.hh.write("*** SHOW DOWN ***\n")
        for p in player:
            if (p.hand == ""):
                self.hh.write("{a}: doesn't show hand\n".format( a = p.name)) 
            else: 
                self.hh.write("{a}: shows [{b}]".format( a = p.name, b = p.hand))  
        self.hh.write("{a} collected ${b:.2f} from pot\n".format( a = winner.name, b = pot)) 
        
    def summary(self, players):
        rake = self.pot*0.0845
        if (rake > self.bb*8.5):
            rake = self.bb*8.5
        self.hh.write("*** SUMMARY ***\n")
        self.hh.write("Total pot ${a:.2f} | Rake ${b:.2f}".format( a = self.pot, b = rake))
        self.hh.write("Board [{a}]".format( a = self.board))
        for p in players:
            self.hh.write(p.summary)
            
    def writeToFile(self):
        with open ("Dave's Hand Histories.txt", 'w') as f:
            self.hh.seek (0)
            shutil.copyfileobj (self.hh, f)

            
            
            