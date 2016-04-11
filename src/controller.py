#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide import QtGui
from PySide.QtGui import *

from view import Ui_Wienwahl

import sys
import os
import csv


class Controller(QMainWindow):
    def __init__(self, parent=None):
        #GUI Initialisierien
        super(Controller, self).__init__(parent)
        self.view = Ui_Wienwahl()
        self.view.setupUi(self)

        #Shortcuts erstellen
        self.createShortcuts()

        #Menue verlinken
        self.linkMenu()

    def createShortcuts(self):
        QShortcut(QKeySequence("CTRL+Q"), self, self.exit)

    def linkMenu(self):
        self.view.actionExit.triggered.connect(self.exit)

    def open(self):
        pass

    def new(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass

    def exit(self):
        sys.exit()

    def addNewRow(self):
        pass

    def duplicateRow(self):
        pass

    def deleteRow(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def cut(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def saveToDB(self):
        pass

    def loadFromDB(self):
        pass

    def generateProjection(self):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    c = Controller()
    c.show()
    sys.exit(app.exec_())