#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 23:03:47 2019

@author: harsh
"""

import csv

from PyQt5 import QtCore, QtGui, QtWidgets

class Viewer1(QtWidgets.QWidget):
    def __init__(self, fileName, parent=None):
        super(Viewer1, self).__init__(parent)
        

        self.fileName = fileName

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.loadCsv(self.fileName)


        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    
    sys.exit(app.exec_())