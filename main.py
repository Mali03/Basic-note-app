from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidget, QMessageBox, QMenu, QAction
from PyQt5 import QtGui
from src.MainWindow import Ui_MainWindow
from src.SecondWindow import Ui_SecondWindow
import sys
import json


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.loadNotes()

        self.ui.notesListWidget.model().rowsMoved.connect(self.itemMoved)

        self.ui.notesListWidget.setStyleSheet("background-color: rgb(150, 150, 150)")
        self.ui.notesListWidget.setDragDropMode(QListWidget.InternalMove)

        self.ui.newNoteButton.clicked.connect(self.addNote)

        self.ui.notesListWidget.itemDoubleClicked.connect(self.editNote)

    def contextMenuEvent(self, event):
        context = QMenu(self)
        
        action1 = QAction("Delete", self)

        context.setStyleSheet("background-color: rgb(255, 255, 255)")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        action1.setIcon(icon)
        
        action1.triggered.connect(self.deleteNote)
        
        context.addAction(action1)
        
        context.exec_(event.globalPos())

    def deleteNote(self):
        currentItem = self.ui.notesListWidget.currentItem()
        if currentItem:
            deletedIndex = self.ui.notesListWidget.row(currentItem)
        
        with open("data/database.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for i in range(deletedIndex, len(data) - 1):
            data[f"note_{i}"] = data[f"note_{i+1}"]

        del data[f"note_{len(data) - 1}"]

        with open("data/database.json", "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

        self.loadNotes()

    def itemMoved(self, parent, start, end, destination, row):
        itemCount = self.ui.notesListWidget.count()

        if ((row - start) == 2 or row == itemCount or ((row - start) != 2 and row == (itemCount - 1))):
            row -= 1

        with open("data/database.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            movedItemData = data[f"note_{start}"][0]

            if row > start:
                for i in range(start, row):
                    data[f"note_{i}"] = data[f"note_{i+1}"]
                data[f"note_{row}"] = [movedItemData]

            elif row < start:
                for i in range(start, row, -1):
                    data[f"note_{i}"] = data[f"note_{i-1}"]
                data[f"note_{row}"] = [movedItemData]

            with open("data/database.json", "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=4)

    def addNote(self):
        self.newWindow = QtWidgets.QMainWindow()
        self.uiSecond = Ui_SecondWindow()
        self.uiSecond.setupUi(self.newWindow)
        self.uiSecond.textBaslik.setStyleSheet("background-color: rgb(150, 150, 150)")
        self.uiSecond.textIcerik.setStyleSheet("background-color: rgb(150, 150, 150)")
        self.newWindow.show()

        self.uiSecond.buttonKaydet.clicked.connect(self.saveNote)

    def saveNote(self):
        if len(self.uiSecond.textBaslik.toPlainText()) == 0:
            QMessageBox.warning(None, "Warning", "Please enter a topic.")
        else:
            notDict = {
                "noteTopic": self.uiSecond.textBaslik.toPlainText(),
                "noteContent": self.uiSecond.textIcerik.toPlainText(),
            }

            with open("data/database.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                sayi = self.ui.notesListWidget.count()

                data[f"note_{sayi}"] = [
                    {
                        "noteTopic": notDict["noteTopic"],
                        "noteContent": notDict["noteContent"],
                    }
                ]

                with open("data/database.json", "w", encoding="utf-8") as outfile:
                    json.dump(data, outfile, indent=4)

                self.newWindow = QtWidgets.QMainWindow()
                self.uiSecond = Ui_SecondWindow()
                self.uiSecond.setupUi(self.newWindow)
                self.newWindow.close()

            self.loadNotes()

    def editNote(self):
        index = self.ui.notesListWidget.currentRow()
        item = self.ui.notesListWidget.item(index)

        with open("data/database.json", "r", encoding="utf-8") as file:
            datas = json.load(file)
            for data in datas:
                if not isinstance(datas[data], list):
                    continue
                if datas[data][0]["noteTopic"] == item.text():
                    self.newWindow = QtWidgets.QMainWindow()
                    self.uiSecond = Ui_SecondWindow()
                    self.uiSecond.setupUi(self.newWindow)
                    self.uiSecond.textBaslik.setStyleSheet(
                        "background-color: rgb(150, 150, 150)"
                    )
                    self.uiSecond.textBaslik.setText(datas[data][0]["noteTopic"])
                    self.uiSecond.textIcerik.setStyleSheet(
                        "background-color: rgb(150, 150, 150)"
                    )
                    self.uiSecond.textIcerik.setText(datas[data][0]["noteContent"])
                    self.newWindow.show()

                    self.uiSecond.buttonKaydet.clicked.connect(self.editTheNote)

    def editTheNote(self):

        notDict = {
            "noteTopic": self.uiSecond.textBaslik.toPlainText(),
            "noteContent": self.uiSecond.textIcerik.toPlainText(),
        }

        with open("data/database.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            sayi = self.ui.notesListWidget.currentRow()

            data[f"note_{sayi}"] = [
                {
                    "noteTopic": notDict["noteTopic"],
                    "noteContent": notDict["noteContent"],
                }
            ]

            with open("data/database.json", "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=4)

                self.newWindow = QtWidgets.QMainWindow()
                self.uiSecond = Ui_SecondWindow()
                self.uiSecond.setupUi(self.newWindow)
                self.newWindow.close()

        self.loadNotes()

    def loadNotes(self):
        self.ui.notesListWidget.clear()
        with open("data/database.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            notlar = [v for k, v in data.items() if k.startswith("note_")]

            for notDict in notlar:
                for notItem in notDict:
                    self.ui.notesListWidget.addItem(notItem["noteTopic"])


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


app()
