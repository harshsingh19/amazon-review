#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 06:18:47 2019

@author: harsh
"""

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QToolTip,QMessageBox,QInputDialog, QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication,QSize
import sys
from PyQt5.QtWidgets import  QWidget, QAction,QComboBox,QHBoxLayout, QFrame, QSplitter,QStyleFactory,QTabWidget,QVBoxLayout,QListWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap,QImage,QPalette,QBrush
from amazon import main
class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Web Analizer"
        self.top = 20
        self.left = 20
        self.width = 400
        self.height = 300
        self.setWindowIcon(QtGui.QIcon("result.jpeg"))
            
        self.InitWindow()


    
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height);
        self.backgroudimage()
        self.statusBar().showMessage("Ready")
        self.button()
        self.getText()
        self.llabel()
        self.show()
    def backgroudimage(self):
        oImage = QImage("result1.jpeg")
        sImage = oImage.scaled(QSize(400,300))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.label = QLabel('', self)
        self.label.setGeometry(20,20,400,300)
        
    def button(self):
        #search Button
        button1 = QPushButton("Submit",self)
        button1.move(80,230)
        button1.setToolTip("<p>Button for Search Product Details</p>")
        button1.clicked.connect(self.on_click)
        #close button
        button2 = QPushButton("Exit",self)
        button2.move(220,230)
        button2.setToolTip("<p>Button for Close </p>")
        button2.clicked.connect(self.CloseApp)
    def CloseApp(self):
        reply = QMessageBox.question(self,"Close Message","Are you Sure You want to close it", QMessageBox.Yes | QMessageBox.No , QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def getText(self):
        self.Textbox1 = QLineEdit(self)
        self.Textbox1.resize(240,55)
        self.Textbox1.move(80,120)
        self.Textbox1.setPlaceholderText("Product URL")
    
    def llabel(self):
        Label1 = QLabel('Enter the Product URL :-',self)
        Label1.move(80,50)
        Label1.resize(300,35)

    @pyqtSlot()
    def on_click(self):
        self.textboxValue1 = self.Textbox1.text()
        self.datasender()
        #self.textbox.setText("")
        #tabs.addTab(tab3,'WordCloud')
        #tabs.addTab(tab4,'Bar Chart')
    def datasender(self):
        self.statusBar().showMessage("Running")
        self.findresult = main(self.textboxValue1)
        self.statusBar().showMessage(self.findresult)
        label2 = QLabel(self.findresult,self)
        label2.move(80,50)
        label2.resize(300,35)                 
 
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())