#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide import QtGui
from PySide.QtGui import *

from view import Ui_Wienwahl
from model import CSVManager, TableModel
from database import Database
from delegate import ItemDelegate
from commands import EditCommand

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
        self.db = Database()
        self.filename = None
        self.view.tableView.setSortingEnabled(True)
        self.undoStack = QUndoStack()
        self.view.tableView.setItemDelegate(ItemDelegate(self.undoStack))

    def createShortcuts(self):
        QShortcut(QKeySequence("CTRL+Q"), self, self.exit)
        QShortcut(QKeySequence("CTRL+C"), self, self.copy)
        QShortcut(QKeySequence("CTRL+V"), self, self.paste)
        QShortcut(QKeySequence("CTRL+Z"), self, self.undo)
        QShortcut(QKeySequence("CTRL+Y"), self, self.redo)
        QShortcut(QKeySequence("CTRL+X"), self, self.cut)

    def linkMenu(self):
        self.view.actionExit.triggered.connect(self.exit)
        self.view.actionOpen.triggered.connect(self.open)
        self.view.actionNew.triggered.connect(self.new)
        self.view.actionSave.triggered.connect(self.save)
        self.view.actionSaveAs.triggered.connect(self.saveAs)
        self.view.actionAddNewRow.triggered.connect(self.addNewRow)
        self.view.actionDuplicateRow.triggered.connect(self.duplicateRow)
        self.view.actionDeleteRow.triggered.connect(self.deleteRow)
        self.view.actionSaveToDB.triggered.connect(self.saveToDB)
        self.view.actionLoadFromDB.triggered.connect(self.loadFromDB)
        self.view.actionGenerateProjection.triggered.connect(self.generateProjection)
        self.view.actionUndo.triggered.connect(self.undo)
        self.view.actionRedo.triggered.connect(self.redo)
        self.view.actionCopy.triggered.connect(self.copy)
        self.view.actionPaste.triggered.connect(self.paste)
        self.view.actionCut.triggered.connect(self.cut)

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
        if len(self.view.tableView.selectionModel().selectedIndexes()) != 0:
            clipboard = QApplication.clipboard()
            selected_index = self.view.tableView.selectionModel().selectedIndexes()[0]
            selected_text = str(self.model.data(selected_index))
            clipboard.setText(selected_text)

    def paste(self):
        if len(self.view.tableView.selectionModel().selectedIndexes()) != 0:
            clipboard = QApplication.clipboard()
            index = self.view.tableView.selectionModel().selectedIndexes()[0]
            command = EditCommand(self.model, index)
            command.newValue(str(clipboard.text()))

            self.undoStack.beginMacro("Paste")
            self.undoStack.push(command)
            self.undoStack.endMacro()
            self.view.tableView.reset()

    def cut(self):
        self.copy()
        index = self.view.tableView.selectionModel().selectedIndexes()[0]
        command = EditCommand(self.model, index)
        command.newValue("")
        self.undoStack.beginMacro("Cut")
        self.undoStack.push(command)
        self.undoStack.endMacro()
        self.view.tableView.reset()

    def undo(self):
        print()
        self.undoStack.undo()
        self.view.tableView.reset()

    def redo(self):
         self.undoStack.redo()
         self.view.tableView.reset()

    def saveToDB(self):
        export = self.model.getDataForExport()
        export = [export[0]]+export[1]
        self.db.save_to_db(export, self.view.statusBar)

    def loadFromDB(self):
        data = self.db.read_from_db(self.view.statusBar)
        self.model.update(data[0], data[1:])
        self.view.tableView.reset()
        self.view.tableView.repaint()
        self.view.tableView.setModel(self.model)

    def generateProjection(self):
        pro = self.db.generateProjection(self.view.statusBar)
        if pro is not False:
            pro_header = [["Partei"],["Stimmen in %"]]
            self.model.update(pro_header, pro)
            self.view.tableView.reset()
            self.view.tableView.repaint()
            self.view.tableView.setModel(self.model)

class DevNull:
    def write(self, msg):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    sys.stderr = DevNull()
    c = Controller(app)
    c.show()
    sys.exit(app.exec_())