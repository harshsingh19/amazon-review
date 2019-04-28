#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:10:18 2019

@author: harsh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:35:09 2019

@author: harsh
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Viewer2(QWidget):
    def __init__(self,_listimg):
        super().__init__()
        self.title = 'Document Analysis'
        self.left = 30
        self.top = 30
        self.width = 640
        self.height = 480
        self.imagenumber=0
        self._listimg = _listimg
        self.initUI()

    def keyPressEvent(self, event):
        key=event.key()
        if key==Qt.Key_Right:
            self.imagenumber=self.imagenumber+1
            self.showimage(self.imagenumber)
            # self.show()
        elif key==Qt.Key_Left:
            self.imagenumber=self.imagenumber-1
            self.showimage(self.imagenumber)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.showimage(0)
        self.show()

    def showimage(self,imagenumber):
        # label = QLabel(self)
        diroctray = 'image_data_store/'
        imagelist = self._listimg
        try:
            pixmap = QPixmap(diroctray+imagelist[imagenumber])
        # label.setPixmap(pixmap)
            self.label.setPixmap(pixmap)
            self.resize(pixmap.width() , pixmap.height())
            # self.show()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Viewer2()
    sys.exit(app.exec_())