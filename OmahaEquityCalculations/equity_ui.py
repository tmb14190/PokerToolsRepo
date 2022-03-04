'''
Created on 17 Feb 2022

@author: Jack
'''
import sys, random
import OmahaEquityCalculations.omaha_equity as OE
from PySide2.QtCore import SIGNAL, Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QLabel, QWidget, QAction


app = QApplication(sys.argv)

def nextSim(muh):
    del app
    ok = QApplication(sys.argv)
    form = EquityUI()
    form.show()
    ok.exec_()
    
class EquityUI(QWidget):
    
    hand1 = ""
    hand2 = ""
    board = ""
    equity1 = 0
    equity2 = 0
    
    flag1 = 0
    flag2 = 0
    
    
    def __init__(self, parent=None):
        super(EquityUI, self).__init__(parent)
        
        self.setupVariables()
        
        hand1_text = self.colourText(self.hand1)
        hand2_text = self.colourText(self.hand2)
        board_text = self.colourText(self.board)
        
        # Setup Hand1 Label
        self.hand1_label = QLabel(self)
        self.hand1_label.setText(hand1_text)
        self.hand1_label.setStyleSheet("font: 16pt Calibri")
        self.hand1_label.move(40, 80)
    
        # Setup Hand2 Label
        self.hand2_label = QLabel(self)
        self.hand2_label.setText(hand2_text)
        self.hand2_label.setStyleSheet("font: 16pt Calibri")
        self.hand2_label.move(190, 80)
        
        # Setup Board Label
        self.board_label = QLabel(self)
        self.board_label.setText(board_text)
        self.board_label.setStyleSheet("font: 20pt Calibri")
        self.board_label.move(105, 20)
        
        # Setup equity1 Input
        self.e1_label = QLabel(self)
        self.e1_label.setText("Equity Hand 1:")
        self.e1_label.setStyleSheet("font: 14pt Calibri")
        self.e1_label.move(40, 148)
        
        self.e1_input = QLineEdit(self)
        self.e1_input.setStyleSheet("font: 22pt Calibri")
        self.e1_input.move(185, 140)
        self.e1_input.resize(80,40)
        self.e1_input.setAlignment(Qt.AlignCenter)
    
        # Setup equity2 Input
        self.e2_label = QLabel(self)
        self.e2_label.setText("Equity Hand 2:")
        self.e2_label.setStyleSheet("font: 14pt Calibri")
        self.e2_label.move(40, 208)
        
        self.e2_input = QLineEdit(self)
        self.e2_input.setStyleSheet("font: 22pt Calibri")
        self.e2_input.move(185, 200)
        self.e2_input.resize(80,40)
        self.e2_input.setAlignment(Qt.AlignCenter)

        #self.setLayout(layout)
        self.setWindowTitle("Pot Odds")
        self.setGeometry(800,300,325,360)
        
#         self.label3 = QLabel(self)
#         self.label3.setStyleSheet("font: 11pt Calibri")
#         self.label3.move(270, 148)
#         self.label3.hide()
        
        # Equity1 Output
        self.label4 = QLabel(self)
        self.label4.setStyleSheet("font: 11pt Calibri")
        self.label4.move(270, 148)
        self.label4.hide()
        
        # Equity2 Output
        self.label5 = QLabel(self)
        self.label5.setStyleSheet("font: 11pt Calibri")
        self.label5.move(270, 208)
        self.label5.hide()
        
    def setupVariables(self):
        # Setup our simulation variables
        
        self.hand1, self.hand2, self.board, self.equity1, self.equity2 = OE.runRandom()
    
    def colourText(self, text):
        text_coloured = []
        for i in text.split():
            if (i[1] == "h"):
                text_coloured.append("<font color=\"red\">%s</font>" % i)
            if (i[1] == "c"):
                text_coloured.append("<font color=\"green\">%s</font>" % i)
            if (i[1] == "d"):
                text_coloured.append("<font color=\"blue\">%s</font>" % i)
            if (i[1] == "s"):
                text_coloured.append(i)
        
        output = ""
        for i in text_coloured:
            output = output + " " + i
        return output[1:]

    def button_click(self):
        
        if (self.flag1 + self.flag2 == 2):
            self.setupVariables()
            self.reset()
        
        guessE1 = self.e1_input.text()
        guessE2 = self.e2_input.text()
        
        if (guessE1 == ""):
            guessE1 = -1
        if (guessE2 == ""):
            guessE2 = -1
        
        print (guessE1)
        print (type(guessE1))
        print (self.equity1)
        
        diffE1 = float(guessE1) - self.equity1
        diffE2 = float(guessE2) - self.equity2
        
        print (diffE1)
        
        # Bluffing Threshold
        if (diffE1 >= -1 and diffE1 <= 1):
            
            self.label4.setText(str(self.equity1)[:5] + "%")
            self.label4.show()

            self.e1_input.setStyleSheet("background-color:green; font: 22pt Calibri;")
            if (guessE1 != -1 and guessE2 == -1):
                self.e2_input.setFocus()
            
            self.flag1 = 1
        else:
            
            self.e1_input.setText("")
            
            if (not(guessE1 == -1)):
                if (float(guessE1) > self.equity1):
                    self.e1_input.setStyleSheet("background-color:orange; font: 22pt Calibri;")
                else:
                    self.e1_input.setStyleSheet("background-color:yellow; font: 22pt Calibri;")
            
            
        # MDF
        if (diffE2 >= -1 and diffE2 <= 1):
            
            self.label5.setText(str(self.equity2)[:5] + "%")
            self.label5.show()
            
            self.e2_input.setStyleSheet("background-color:green; font: 22pt Calibri;")
            
            self.flag2 = 1
        else:
            
            self.e2_input.setText("")
            
            if (not(guessE2 == -1)):
                if (float(guessE2) > self.equity2):
                    self.e2_input.setStyleSheet("background-color:orange; font: 22pt Calibri;")
                else:
                    self.e2_input.setStyleSheet("background-color:yellow; font: 22pt Calibri;")    
    
    def reset(self):
        
        hand1_text = self.colourText(self.hand1)
        hand2_text = self.colourText(self.hand2)
        board_text = self.colourText(self.board)
        
        self.hand1_label.setText(hand1_text)
        self.hand2_label.setText(hand2_text)
        self.board_label.setText(board_text)
        self.label4.hide()
        self.label5.hide()
        
        self.flag1 = 0
        self.flag2 = 0
        
        self.e1_input.setStyleSheet("background-color:white; font: 22pt Calibri;")
        self.e2_input.setStyleSheet("background-color:white; font: 22pt Calibri;")
        
        self.e1_input.setText("")
        self.e2_input.setText("")
        
        self.e1_input.setFocus()
    
    def notifyObservers(self):
        self.close()
    
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            self.button_click()

form = EquityUI()
form.show()
app.exec_()
