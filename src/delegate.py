from PySide.QtGui import QStyledItemDelegate, QLineEdit

from commands import EditCommand


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, undoStack):
        super().__init__()
        self.undoStack = undoStack
        self.edit = None

    def setModelData(self, editor, model, index):
        newValue = editor.text()
        self.edit.newValue(newValue)
        self.undoStack.beginMacro("Edit Cell")
        self.undoStack.push(self.edit)
        self.undoStack.endMacro()

    def editorEvent(self, event, model, option, index):
        self.edit = EditCommand(model, index)

    def createEditor(self, parent, option, index):
        return QLineEdit(parent)