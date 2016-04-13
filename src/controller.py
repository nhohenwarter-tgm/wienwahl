#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide import QtGui
from PySide.QtGui import *

from view import Ui_Wienwahl
from model import CSVManager, TableModel

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

        #Init
        self.model = TableModel()
        self.filename = None

    def createShortcuts(self):
        QShortcut(QKeySequence("CTRL+Q"), self, self.exit)

    def linkMenu(self):
        self.view.actionExit.triggered.connect(self.exit)
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionNew.triggered.connect(self.new)

    def open(self):
        self.fileName = QFileDialog.getOpenFileName(self,"Open Image", QDir.homePath(), "CSV Files (*.csv)")
        csv = CSVManager.importCSV(self, self.fileName[0])
        self.model.update(csv[0],csv[1])
        self.view.tableView.setModel(self.model)


    def new(self):
        csvheader = [["Col1"],["Col2"]]
        csvdata = [["Data1","Data2"]]
        self.model.update(csvheader, csvdata)
        self.view.tableView.setModel(self.model)

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