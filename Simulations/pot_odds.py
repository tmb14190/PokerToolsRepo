'''
Created on 1 May 2019

@author: Jack
'''
import sys, random
from PySide2.QtCore import SIGNAL, Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QWidget, QAction

app = QApplication(sys.argv)

def nextSim(muh):
    del app
    ok = QApplication(sys.argv)
    form = BasicMath()
    form.show()
    ok.exec_()
    
class BasicMath(QWidget):
    
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    pot = 0
    bet = 0
    PO = 0
    MDF = 0
    BT = 0
    BF = 0
    
    
    def __init__(self, parent=None):
        super(BasicMath, self).__init__(parent)
        
        self.setupVariables()
        
        # Setup Pot Size Label
        self.label = QLabel(self)
        self.label.setText("Pot: $%.2f" % self.pot)
        self.label.setStyleSheet("font: 22pt Calibri")
        self.label.move(170, 50)
    
        # Setup Bet Size Label
        self.label2 = QLabel(self)
        percent = (round(self.bet / self.pot, 3))*100
        betPercentage = " (" + str(percent) + "%)"
        self.label2.setText("Bet: $%.2f" % self.bet)
        self.label2.setStyleSheet("font: 22pt Calibri")
        self.label2.move(30, 50)
        
        # Setup Pot Odds Input
#         self.pola = QLabel(self)
#         self.pola.setText("Pot Odds:")
#         self.pola.setStyleSheet("font: 14pt Calibri")
#         self.pola.move(85, 148)
#         
#         self.input = QLineEdit(self)
#         self.input.setStyleSheet("font: 22pt Calibri")
#         self.input.move(185, 140)
#         self.input.resize(80,40)
#         self.input.setAlignment(Qt.AlignCenter)
        
        # Setup Bluffing Threshold Input
        self.bthrela = QLabel(self)
        self.bthrela.setText("Bluffing Threshold:")
        self.bthrela.setStyleSheet("font: 14pt Calibri")
        self.bthrela.move(18, 148)
        
        self.bthre = QLineEdit(self)
        self.bthre.setStyleSheet("font: 22pt Calibri")
        self.bthre.move(185, 140)
        self.bthre.resize(80,40)
        self.bthre.setAlignment(Qt.AlignCenter)
    
        # Setup MDF Input
        self.mdfla = QLabel(self)
        self.mdfla.setText("MDF:")
        self.mdfla.setStyleSheet("font: 14pt Calibri")
        self.mdfla.move(120, 208)
        
        self.mdfin = QLineEdit(self)
        self.mdfin.setStyleSheet("font: 22pt Calibri")
        self.mdfin.move(185, 200)
        self.mdfin.resize(80,40)
        self.mdfin.setAlignment(Qt.AlignCenter)
        
        # Setup Bluffing Frequency Input
        self.bfreqla = QLabel(self)
        self.bfreqla.setText("Bluffing Frequency:")
        self.bfreqla.setStyleSheet("font: 14pt Calibri")
        self.bfreqla.move(15, 268)
        
        self.bfreq = QLineEdit(self)
        self.bfreq.setStyleSheet("font: 22pt Calibri")
        self.bfreq.move(185, 260)
        self.bfreq.resize(80,40)
        self.bfreq.setAlignment(Qt.AlignCenter)

        #self.setLayout(layout)
        self.setWindowTitle("Pot Odds")
        self.setGeometry(800,300,325,360)
        
#         self.label3 = QLabel(self)
#         self.label3.setStyleSheet("font: 11pt Calibri")
#         self.label3.move(270, 148)
#         self.label3.hide()
        
        self.label4 = QLabel(self)
        self.label4.setStyleSheet("font: 11pt Calibri")
        self.label4.move(270, 148)
        self.label4.hide()
        
        self.label5 = QLabel(self)
        self.label5.setStyleSheet("font: 11pt Calibri")
        self.label5.move(270, 208)
        self.label5.hide()
        
        self.label6 = QLabel(self)
        self.label6.setStyleSheet("font: 11pt Calibri")
        self.label6.move(270, 268)
        self.label6.hide()
        
        
    def setupVariables(self):
        # Setup our simulation variables
        self.pot = round( random.uniform(0.35, 25) , 2 )
        
        # Make it a bit more likely to be within the range of 25-125%
        x = random.randint(1, 3)
        if (x == 1):
            self.bet = round( random.uniform(0.1, self.pot*2) , 2 )
            #print ("random")
        else:
            self.bet = round( random.uniform(self.pot*0.25, self.pot*1.25) , 2 )
           # print ("realistic")
        
        # Round
        self.PO = (round( self.bet / (self.pot + self.bet + self.bet), 4 )) * 100
        pPot = self.bet / self.pot
        self.BT = (round(pPot / (pPot + 1), 4)) * 100
        self.MDF = (100 - self.BT)
        self.BF = (round(pPot / ((2 * pPot) + 1), 4)) * 100
        
        #print (self.PO)
        #print (self.BT)
        #print (self.MDF)
        #print (self.BF)
    

    def button_click(self):
        
        if (self.flag2 + self.flag3 + self.flag4 == 3):
            self.setupVariables()
            self.reset()
        
        # shost is a QString object
#         guess = self.input.text()
        guessMDF = self.mdfin.text()
        guessBT = self.bthre.text()
        guessBF = self.bfreq.text()
        
#         if (guess == ""):
#             guess = 0
        if (guessMDF == ""):
            guessMDF = 0
        if (guessBT == ""):
            guessBT = 0
        if (guessBF == ""):
            guessBF = 0
        
#         diffPO = float(guess) - self.PO
        diffMDF = float(guessMDF) - self.MDF
        
        #print (guessBT)
        #print (type(guessBT))
        #print (self.BF)
        
        diffBT = float(guessBT) - self.BT
        diffBF = float(guessBF) - self.BF
        
#         # Pot Odds
#         if (diffPO >= -1 and diffPO <= 1):
#             
#             self.label3.setText(str(self.PO)[:5] + "%")
#             self.label3.show()
# 
#             self.input.setStyleSheet("background-color:green; font: 22pt Calibri;")
#             if (guess != 0 and guessMDF == 0):
#                 self.bthre.setFocus()
# 
#             self.flag1 = 1
#         else:
#             
#             self.input.setText("")
# 
#             if (not(guess == 0)):
#                 if (float(guess) > self.PO):
#                     self.mdfin.setStyleSheet("background-color:orange; font: 22pt Calibri;")
#                 else:
#                     self.mdfin.setStyleSheet("background-color:yellow; font: 22pt Calibri;")
        
        # Bluffing Threshold
        if (diffBT >= -1 and diffBT <= 1):
            
            self.label4.setText(str(self.BT)[:5] + "%")
            self.label4.show()

            self.bthre.setStyleSheet("background-color:green; font: 22pt Calibri;")
            if (guessBT != 0 and guessMDF == 0):
                self.mdfin.setFocus()
            
            self.flag3 = 1
        else:
            
            self.bthre.setText("")
            
            if (not(guessBT == 0)):
                if (float(guessBT) > self.BT):
                    self.bthre.setStyleSheet("background-color:orange; font: 22pt Calibri;")
                else:
                    self.bthre.setStyleSheet("background-color:yellow; font: 22pt Calibri;")
            
            
        # MDF
        if (diffMDF >= -1 and diffMDF <= 1):
            
            self.label5.setText(str(self.MDF)[:5] + "%")
            self.label5.show()
            
            self.mdfin.setStyleSheet("background-color:green; font: 22pt Calibri;")
            if (guessMDF != 0 and guessBT != 0 and guessBF == 0):
                self.bfreq.setFocus()
            
            self.flag2 = 1
        else:
            
            self.mdfin.setText("")
            
            if (not(guessMDF == 0)):
                if (float(guessMDF) > self.MDF):
                    self.mdfin.setStyleSheet("background-color:orange; font: 22pt Calibri;")
                else:
                    self.mdfin.setStyleSheet("background-color:yellow; font: 22pt Calibri;")
            
        
        # Bluffing Frequency
        if (diffBF >= -1 and diffBF <= 1):
            
            self.label6.setText(str(self.BF)[:5] + "%")
            self.label6.show()

            self.bfreq.setStyleSheet("background-color:green; font: 22pt Calibri;")
            
            self.flag4 = 1
        else:
            
            self.bfreq.setText("")
            
            if (not(guessBF == 0)):
                if (float(guessBF) > self.BF):
                    self.bfreq.setStyleSheet("background-color:orange; font: 22pt Calibri;")
                else:
                    self.bfreq.setStyleSheet("background-color:yellow; font: 22pt Calibri;")
                    
                    
    
    def reset(self):
        self.label.setText("Pot: $%.2f" % self.pot)
        self.label2.setText("Bet: $%.2f" % self.bet)
        self.label4.hide()
        self.label5.hide()
        self.label6.hide()
        self.label4.hide()
        
        self.flag2 = 0
        self.flag3 = 0
        self.flag4 = 0
        
        self.mdfin.setStyleSheet("background-color:white; font: 22pt Calibri;")
        self.bfreq.setStyleSheet("background-color:white; font: 22pt Calibri;")
        self.bthre.setStyleSheet("background-color:white; font: 22pt Calibri;")
        
        self.mdfin.setText("")
        self.bthre.setText("")
        self.bfreq.setText("")
        
        self.bthre.setFocus()
    
    def notifyObservers(self):
        #next = BasicMath()
        #next.show()
        self.close()
    
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            self.button_click()

form = BasicMath()
form.show()
app.exec_()