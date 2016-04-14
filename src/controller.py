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
    def __init__(self, app, parent=None):
        #GUI Initialisierien
        super(Controller, self).__init__(parent)
        self.view = Ui_Wienwahl()
        self.view.setupUi(self)
        self.app = app

        #Shortcuts erstellen
        self.createShortcuts()

        #Menue verlinken
        self.linkMenu()

        #Init
        self.model = TableModel()
        self.filename = None
        self.view.tableView.setSortingEnabled(True)
        self.view.tableView.resizeColumnsToContents()

    def createShortcuts(self):
        QShortcut(QKeySequence("CTRL+Q"), self, self.exit)

    def linkMenu(self):
        self.view.actionExit.triggered.connect(self.exit)
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionNew.triggered.connect(self.new)
        self.view.actionSave.triggered.connect(self.save)
        self.view.actionSaveAs.triggered.connect(self.saveAs)
        self.view.actionAddNewRow.triggered.connect(self.addNewRow)
        self.view.actionDuplicateRow.triggered.connect(self.duplicateRow)
        self.view.actionDeleteRow.triggered.connect(self.deleteRow)

    def open(self):
        self.view.statusBar.showMessage("Opening file...", 2000)
        self.fileName = QFileDialog.getOpenFileName(self,"Open CSV", QDir.homePath(), "CSV Files (*.csv)")
        csv = CSVManager.importCSV(self, self.fileName[0])
        self.model.update(csv[0],csv[1])
        self.view.tableView.reset()
        self.view.tableView.repaint()
        self.view.tableView.setModel(self.model)


    def new(self):
        self.view.statusBar.showMessage("Creating new file...", 750)
        csvheader = [["#"],["Col1"],["Col2"]]
        csvdata = [["1","Data1","Data2"]]
        self.model.update(csvheader, csvdata)
        self.view.tableView.reset()
        self.view.tableView.repaint()
        self.view.tableView.setModel(self.model)

    def save(self):
        self.view.statusBar.showMessage("Saving to file...", 2000)
        if self.fileName is None:
            self.fileName = QFileDialog.getSaveFileName(self,"Save CSV", QDir.homePath(), "CSV Files (*.csv)")
        CSVManager.exportCSV(self, self.fileName[0], self.model.getDataForExport())

    def saveAs(self):
        self.view.statusBar.showMessage("Saving to file...", 2000)
        self.fileName = QFileDialog.getSaveFileName(self,"Save CSV", QDir.homePath(), "CSV Files (*.csv)")
        CSVManager.exportCSV(self, self.fileName[0], self.model.getDataForExport())

    def exit(self):
        self.view.statusBar.showMessage("Exiting...", 2000)
        sys.exit()

    def addNewRow(self):
        self.view.statusBar.showMessage("Adding new row...", 1000)
        self.model.insertRow()

    def duplicateRow(self):
        self.view.statusBar.showMessage("Duplicating rows...", 1000)
        selected = self.view.tableView.selectedIndexes()
        self.model.duplicateRow(selected)

    def deleteRow(self):
        self.view.statusBar.showMessage("Deleting rows...", 1000)
        selected = self.view.tableView.selectedIndexes()
        self.model.deleteRow(selected)

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
        self.view.statusBar.showMessage("Saving to database...", 3000)
        pass

    def loadFromDB(self):
        self.view.statusBar.showMessage("Loading from database...", 3000)
        pass

    def generateProjection(self):
        self.view.statusBar.showMessage("Generating projection...", 3000)
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    c = Controller(app)
    c.show()
    sys.exit(app.exec_())