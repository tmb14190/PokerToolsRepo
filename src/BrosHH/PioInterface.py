'''
Created on 27 Oct 2020

@author: jackm
'''
from pywinauto.application import Application
from pywinauto.keyboard import send_keys, KeySequenceError
from pywinauto.mouse import click
import time
from ImageHandHistory.save_as_bytes import save_as_bytes
import win32api
import win32gui
import win32con
import pyHook

class PioInterface:
    app = None
    dlg = None
    first = True
    donk = False # IMPLEMENT NO DONKING ONLY CHECK OR CLOSE PLEASE
    numActions = 0
    street = 1
    board = ""
    endbox = []
    
    def openBoard(self, action, pos1, pos2, board, hand):
        self.board = board
        def dis(event):
            return False
        
        def en(event):
            return True
        
        program_path = r"C:/PioSOLVER/PioViewer.exe"
        #file_path  = self.getPath(action, pos1, pos2, board)
        file_path    = r"D:/Jack Data/Poker/Pio Database/Pio/BU vs BB 50 Flops/TBD/C Bet Boards/AsTh5c.cfr" # gair uses no dash no space e.g. 2h2sKs
        #file_path = r"P:\PioSOLVER\TREES\3Bet\BB 3Bet vs UTG Call\2h2s8s.cfr"
        
        app = Application(backend="uia").start(r'{} "{}"'.format(program_path, file_path))
        
        version = "1.10.24.6"
        #version = "1.10.24.7"
        
        running_path = file_path
        running_path = running_path.replace("/", "\\\\")
        running_path = running_path + " - PioViewer {a}".format(a = version) 
        print (running_path)
        print (file_path)
        
        dlg = app[running_path]
        
        # the buggiest shit in existence - to get it to work i tried app.dlg with it, then ran, then opened cmd and it suddenly worked
        #main = app.dlg.wrapper_object()
        #main.iface_transform.Move(0, 0) # move the window to top-left corner
        #main.iface_transform.Resize(1920, 1080) # change width and height
        
        
        pre_position = win32api.GetCursorPos()
        dlg.click_input(button='left', coords=(34, 62))
        win32api.SetCursorPos(pre_position)
        
        #app.dlg.Browser.select()
        
        #app.dlg.Button6.click()
        pre_position = win32api.GetCursorPos()
        dlg.click_input(button='left', coords=(1860, 340))
        win32api.SetCursorPos(pre_position)
        pre_position = win32api.GetCursorPos()
        dlg.click_input(button='left', coords=self.getHoleCardsCoords(hand))
        win32api.SetCursorPos(pre_position)
        
        
        self.app = app
        self.dlg = dlg
    
    def getPath(self, action, pos1, pos2, board):
        
        # P:\PioSOLVER\TREES\3Bet\BB 3Bet vs BU Call (BU Using Call Range vs SB 3Bet)
        # P:\PioSOLVER\TREES\3Bet\SB 3Bet vs BU Call
        # P:\PioSOLVER\TREES\RFI\UTG RFI vs BB Call
        
        o1 = pos1
        o2 = pos2
        board = board.replace(" ", "")
        if (pos1 == "HJ"):
            pos1 = "UTG"
        if (pos2 == "HJ"):
            pos2 = "UTG"
        if (pos1 == "CO" and pos2 != "BU"):
            pos1 = "BU"
        if (pos2 == "CO"):
            pos2 = "BU"
        
        if (o1 != pos1 or o2 != pos2):
            print ("Nearest Board: {a} {b} vs {c}".format(a = action, b = pos1, c = pos2))
        
        if (action == "RFI"):
            path = r"P:/PioSOLVER/RFI/{a} RFI vs {b} Call/{c}.cfr".format(a = pos1, b = pos2, c = board)
        elif (action == "3Bet"):
            fkGair = ""
            if (pos1 == "BU" and pos2 == "BB"):
                fkGair = " (BU Using Call Range vs SB 3Bet)"
            path = r"P:/PioSOLVER/TREES/3Bet/{a} 3Bet vs {b} Call{c}/{d}.cfr".format(a = pos2, b = pos1, c = fkGair, d = board)
        
        return path
            
    
    '''
    size = 0 for passive actions
    size = 1 for large bet
    size = 2 for small bet 
    size = 3 for raise
    '''
    def addAction(self, action):
        
        pre_position = win32api.GetCursorPos()
        self.dlg.set_focus()
        win32api.SetCursorPos(pre_position)
        coords = 0
        
        if (action == 0):
            if (self.donk): # NEED TO SET THIS UP
                coords = (self.getXNextAction()[-2] + 25, 90)
                print ("Donk Checked")
            elif (self.first):
                coords = (self.getXNextAction()[-2] + 25, 132)
            else:
                coords=(self.getXNextAction()[-2] + 25, 111)
                
        elif (action == 1 or action == 3):
            self.first = False
            coords=(self.getXNextAction()[-2] + 25, 90)
            
        elif (action == 2):
            self.first = False
            coords=(self.getXNextAction()[-2] + 25, 111)
            
        if (coords != 0):
            self.numActions += 1
            pre_position = win32api.GetCursorPos()
            self.dlg.click_input(button='left', coords=coords)
            win32api.SetCursorPos(pre_position)
            
        else:
            print ("PioInterface addAction bad action given")  
            
        self.donk = False  
            
    def addBoardCard(self, card):
        
        print ("numActions: " + str(self.numActions))
        
        self.first = True
        if (self.numActions % 2 == 1): # MAYBE DONK WORKING???
            self.donk = True
        self.numActions = 0
        
        pre_position = win32api.GetCursorPos()
        self.dlg.set_focus()
        win32api.SetCursorPos(pre_position)
        pre_position = win32api.GetCursorPos()
        self.dlg.click_input(button='left', coords=self.getBoardCoord(card))
        win32api.SetCursorPos(pre_position)
            
    '''
    input string cards - holecards e.g. "AsAh"
    '''
    def getHoleCardsCoords(self, cards):
        
        column = 67
        row = 224
        
        column_step = 100
        row_step = 64
        
        dict = {"A":0, "K":1, "Q":2, "J":3, "T":4, "9":5, "8":6, "7":7, "6":8, "5":9, "4":10, "3":11, "2":12}
        
        x = dict[cards[0]]
        y = dict[cards[2]]
        
        if (y < x):
            x, y = y, x
        
        # If suited
        if (cards[1] == cards[3]):
            coords = (y*column_step+column, x*row_step+row)
        else:
            coords = (x*column_step+column, y*row_step+row)
        
        # So if suited we add 1st card * 64, and 2nd card * 100 reverse for offsuit
        
        return coords
    
    # Prolly need to make it more lenient than just finding 240
    # returns an entire array of the end x coords of bet tree, so using output[-2] will get the start of the box for next click
    def getXNextAction(self):
        img = self.dlg.capture_as_image()
        
        img = img.convert('L')
                
        data = list(img.getdata())
        
        WIDTH, HEIGHT = img.size
             
        data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
            
        counter = 0
        flag = 0
        inbox = 0
        endbox = []
        for i in data[83]:
            if (i < 235 or i > 245):
                inbox+=1
            if (inbox == 30):
                flag = 1
            if (flag == 1):
                if (i >= 235 and i <= 245):
                    if (counter < 1700):
                        endbox.append(counter)
                    flag = 0
                    inbox = 0
            counter+=1
        
        self.endbox = endbox
        
        return endbox
    
    '''
    string card - next turn or river card e.g. "5s"
    returns coords for click
    '''
    def getBoardCoord(self, card):
        
        pointer = len(self.endbox) - 1
        
        endbox = self.getXNextAction()
        
        #pict = {"A":-1, "K":-2, "Q":-3, "J":-4, "T":-5, "9":-6, "8":-7, "7":-8, "6":-9, "5":-10, "4":-11, "3":-12, "2":-13}
        pict = {"A":13, "K":12, "Q":11, "J":10, "T":9, "9":8, "8":7, "7":6, "6":5, "5":4, "4":3, "3":2, "2":1}
        cict = {"c":90, "d":111, "h":132, "s":153}
        
        #pointer = pict[card[0]]
        x = endbox[pointer] + (34 * pict[card[0]]) - 17
        y = cict[card[1]]
        
        coord = (x, y)
        
        return coord
    
    def closePio(self):
        self.dlg.type_keys("%{F4}")
    
    