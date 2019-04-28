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
from PyQt5.QtGui import QImage,QPalette,QBrush
from CorpusSentimentViewer import Viewer1
from wordimageshower import Viewer2
from amazon import main
import os

def filechecker(_list,_list2):
    val = []
    for i in _list2:
        if i not in _list:
            val.append(i)
    return val

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Web Analizer"
        self.top = 120
        self.left = 120
        self.width = 405
        self.height = 400
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
        self.label.setGeometry(120,120,400,300)
    
    def button(self):
        #search Button
        self.button1 = QPushButton("Submit",self)
        self.button1.move(20,230)
        self.button1.setToolTip("<p>Button for Search Product Details</p>")
        self.button1.clicked.connect(self.on_click)
        #close button
        self.button2 = QPushButton("Exit",self)
        self.button2.move(160,230)
        self.button2.setToolTip("<p>Button for Close </p>")
        self.button2.clicked.connect(self.CloseApp)

        self.button3 = QPushButton("Attributes",self)
        self.button3.move(290,50)
        self.button3.setToolTip("<p>Button for Showing Attributes </p>")
        self.button3.clicked.connect(lambda: self.dataview('Attribute/'+self.attributefiles[0]))
        self.button3.setEnabled(False)
        
        self.button4 = QPushButton("Cluster",self)
        self.button4.move(290,90)
        self.button4.setToolTip("<p>Button for Showing Cluster </p>")
        self.button4.clicked.connect((lambda: self.dataview('Cluster/'+self.clusterfiles[0])))
        self.button4.setEnabled(False)
        
        self.button5 = QPushButton("Sentence",self)
        self.button5.move(290,130)
        self.button5.setToolTip("<p>Button for Sentence Sentiment Viewer </p>")
        self.button5.clicked.connect(lambda: self.dataview('Data_Output/'+self.val1))
        self.button5.setEnabled(False)
        
        self.button7 = QPushButton("Corpus",self)
        self.button7.move(290,170)
        self.button7.setToolTip("<p>Button for Corpus Sentiment Viewer </p>")
        self.button7.clicked.connect(lambda: self.dataview('Data_Output/'+self.val))
        self.button7.setEnabled(False)
        
        self.button6 = QPushButton("WordCloud",self)
        self.button6.move(290,210)
        self.button6.setToolTip("<p>Button for WordCloud Viewer </p>")
        self.button6.clicked.connect(self.wordcloudviewer)
        self.button6.setEnabled(False)        
        
    def CloseApp(self):
        reply = QMessageBox.question(self,"Close Message","Are you Sure You want to close it", QMessageBox.Yes | QMessageBox.No , QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
    def locationCorpusSentimet(self):
        for i in self.outputfiles:
            if 'CorpusSentimet' in i:
                self.val = i
    def locationSentenceSentiment(self):
        for i in self.outputfiles:
            if 'SentenceSentiment' in i:
                self.val1 = i
    def dataview(self,location):
        self.csvview = Viewer1(location)
        self.csvview.showMaximized()
    def wordcloudviewer(self):
        self.viewword = Viewer2(self.wordcloudfiles)  
        self.viewword.showMaximized()
    def getText(self):
        self.Textbox1 = QLineEdit(self)
        self.Textbox1.resize(240,55)
        self.Textbox1.move(20,120)
        self.Textbox1.setPlaceholderText("Product URL")
    
    def llabel(self):
        Label1 = QLabel('Enter the Product URL :-',self)
        Label1.move(20,50)
        Label1.resize(300,35)

    @pyqtSlot()
    def on_click(self):
        self.textboxValue1 = self.Textbox1.text()
        self.datasender()
        #self.textbox.setText("")
        #tabs.addTab(tab3,'WordCloud')
        #tabs.addTab(tab4,'Bar Chart')
    def datasender(self):
        self.clusterlist1 = os.listdir('Cluster') 
        self.attributelist1 = os.listdir('Attribute') 
        self.output1list1 = os.listdir('Data_Output') 
        self.wordcloud = os.listdir('image_data_store') 
        
        self.statusBar().showMessage("Running")
        self.findresult = main(self.textboxValue1)
        self.statusBar().showMessage(self.findresult)
        self.buttonactivator()
        if self.findresult == 'Sucess':
            self.clusterlist2 = [i for i in os.listdir('Cluster') if '.csv' in i] 
            self.attributelist2 =[i for i in  os.listdir('Attribute') if '.csv' in i] 
            self.output1list2 = [i for i in os.listdir('Data_Output') if '.csv' in i] 
            self.wordcloud2 = os.listdir('image_data_store') 
            self.fileval()

    def fileval(self):
        self.clusterfiles = filechecker(self.clusterlist1,self.clusterlist2)
        self.attributefiles = filechecker(self.attributelist1,self.attributelist2) 
        self.outputfiles = filechecker(self.output1list1,self.output1list2) 
        self.wordcloudfiles = filechecker(self.wordcloud,self.wordcloud2)
        self.locationCorpusSentimet()
        self.locationSentenceSentiment()
    def buttonactivator(self):
        if self.findresult == 'Sucess':
            self.button3.setEnabled(True)
            self.button4.setEnabled(True)
            self.button5.setEnabled(True)
            self.button7.setEnabled(True)
            self.button6.setEnabled(True)       
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
