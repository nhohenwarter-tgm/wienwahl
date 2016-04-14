from PySide.QtCore import *
from PySide import QtCore

import csv, operator


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__()
        self.csvdata = None
        self.csvheader = None

    def update(self, header, data):
        self.emit(SIGNAL("layoutToBeChanged()"))
        self.csvheader = header
        self.csvdata = data
        self.emit(SIGNAL("layoutChanged()"))

    def getDataForExport(self):
        return [self.csvheader,self.csvdata]

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

    def insertRow(self):
        self.emit(SIGNAL("layoutToBeChanged()"))
        col = self.columnCount()-1
        row = [[self.rowCount()+1] + [""] * col]
        self.csvdata= self.csvdata+row
        self.emit(SIGNAL("layoutChanged()"))

    def duplicateRow(self, selected):
        sorted = []
        for sel in selected:
            sorted.append(sel.row())
        sorted = list(set(sorted))
        duplicates = []
        rowcount = self.rowCount()
        for s in sorted:
            rowcount = rowcount+1
            row = self.csvdata[s].copy()
            row[0] = rowcount
            duplicates.append(row)

        newdata = self.csvdata
        newdata += duplicates

        self.update(self.csvheader,newdata)

    def deleteRow(self, selected):
        sorted = []
        for sel in selected:
            sorted.append(sel.row())
        sorted = list(set(sorted))

        newdata = self.csvdata.copy()

        for s in sorted:
            newdata.pop(s)

        for i in range(1,len(newdata)+1):
            newdata[i-1][0] = i

        self.update(self.csvheader,newdata)

    def sort(self, ncol, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.csvdata = sorted(self.csvdata, key=operator.itemgetter(ncol))
        if order == Qt.DescendingOrder:
            self.csvdata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled
        elif index.row == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.SortOrder
        else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable


class CSVManager():
    def importCSV(self, filepath):
        with open(filepath, newline='') as csvfile:
            self.dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, self.dialect)
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
                rownum = rownum + 1
        return [header, data]

    def exportCSV(self, filepath, data):
        with open(filepath, "w+") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            data[0].pop(0)
            writer.writerow(data[0])
            for row in data[1]:
                row.pop(0)
                writer.writerow(row)
