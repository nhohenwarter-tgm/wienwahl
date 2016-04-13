from PySide.QtCore import *
from PySide import QtCore

import csv

class TableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__()
        self.csvdata = None
        self.csvheader = None

    def update(self, header, data):
        self.csvheader = header
        self.csvdata = data

    def rowCount(self, parent=QModelIndex()):
        return len(self.csvdata)

    def columnCount(self, parent=QModelIndex()):
        return len(self.csvdata[0])

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.csvdata[index.row()][index.column()]

    def setData(self, index, value, role=Qt.DisplayRole):
        if not index.isValid():
            return False
        else:
            self.csvdata[index.row()][index.column()] = value
            return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.csvheader[col]
        return None

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled

class CSVManager():
    def importCSV(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = []
            header = []
            rownum = 0

            for row in reader:
                if rownum == 0:
                    header.append("#")
                    for col in row:
                        header.append(col)
                else:
                    rowdata = []
                    rowdata.append(rownum)
                    for col in row:
                        rowdata.append(col)

                    data.append(rowdata)
                rownum = rownum +1
        return [header,data]




    def exportCSV(self, filepath, data):
        pass
