import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,
    QInputDialog, QLabel, QVBoxLayout, QWidget, QShortcut, QFontDialog, QColorDialog
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtGui import QTextListFormat
from PyQt5.QtGui import QTextDocumentWriter
from PyQt5.QtGui import QTextDocument

class NoteTakingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = QSettings('NoteTakingApp', 'Settings')
        self.loadSettings()
        
    def initUI(self):
        self.setWindowTitle("NoteMaster")
        self.setGeometry(100, 100, 500, 500)
        
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        
        self.createActions()
        self.createMenus()
        self.createToolbars()
        self.createShortcuts()
        
        self.noteChanged = False
        
    def createActions(self):
        self.newAction = QAction("New", self)
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.triggered.connect(self.newNote)
        
        self.openAction = QAction("Open", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.triggered.connect(self.openNote)
        
        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.triggered.connect(self.saveNote)
        
        self.saveAsAction = QAction("Save As...", self)
        self.saveAsAction.setShortcut(QKeySequence.SaveAs)
        self.saveAsAction.triggered.connect(self.saveNoteAs)
        
        self.undoAction = QAction("Undo", self)
        self.undoAction.setShortcut(QKeySequence.Undo)
        self.undoAction.triggered.connect(self.textEdit.undo)
        
        self.redoAction = QAction("Redo", self)
        self.redoAction.setShortcut(QKeySequence.Redo)
        self.redoAction.triggered.connect(self.textEdit.redo)
        
        self.cutAction = QAction("Cut", self)
        self.cutAction.setShortcut(QKeySequence.Cut)
        self.cutAction.triggered.connect(self.textEdit.cut)
        
        self.copyAction = QAction("Copy", self)
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.copyAction.triggered.connect(self.textEdit.copy)
        
        self.pasteAction = QAction("Paste", self)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.pasteAction.triggered.connect(self.textEdit.paste)
        
        self.selectAllAction = QAction("Select All", self)
        self.selectAllAction.setShortcut(QKeySequence.SelectAll)
        self.selectAllAction.triggered.connect(self.textEdit.selectAll)
        
        self.searchAction = QAction("Search", self)
        self.searchAction.setShortcut(QKeySequence.Find)
        self.searchAction.triggered.connect(self.searchNote)
        
        self.formatBoldAction = QAction("Bold", self)
        self.formatBoldAction.setShortcut(QKeySequence.Bold)
        self.formatBoldAction.setCheckable(True)
        self.formatBoldAction.triggered.connect(self.toggleBold)
        
        self.formatItalicAction = QAction("Italic", self)
        self.formatItalicAction.setShortcut(QKeySequence.Italic)
        self.formatItalicAction.setCheckable(True)
        self.formatItalicAction.triggered.connect(self.toggleItalic)
        
        self.formatUnderlineAction = QAction("Underline", self)
        self.formatUnderlineAction.setShortcut(QKeySequence.Underline)
        self.formatUnderlineAction.setCheckable(True)
        self.formatUnderlineAction.triggered.connect(self.toggleUnderline)
        
        self.formatBulletAction = QAction("Bullet List", self)
        self.formatBulletAction.triggered.connect(self.toggleBulletList)
        
        self.formatNumberedAction = QAction("Numbered List", self)
        self.formatNumberedAction.triggered.connect(self.toggleNumberedList)

        ###
        self.formatSizeAction = QAction("Font Size", self)
        self.formatSizeAction.triggered.connect(self.setFontSize)

        self.formatFontAction = QAction("Font", self)
        self.formatFontAction.triggered.connect(self.setFont)

        self.formatColorAction = QAction("Text Color", self)
        self.formatColorAction.triggered.connect(self.setTextColor)

        
    def createMenus(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        
        editMenu = menubar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.selectAllAction)
        editMenu.addAction(self.searchAction)
        
        formatMenu = menubar.addMenu("Format")
        formatMenu.addAction(self.formatBoldAction)
        formatMenu.addAction(self.formatItalicAction)
        formatMenu.addAction(self.formatUnderlineAction)
        formatMenu.addAction(self.formatBulletAction)
        formatMenu.addAction(self.formatNumberedAction)
        
    def createToolbars(self):
        toolbar = self.addToolBar("Toolbar")
        toolbar.addAction(self.newAction)
        toolbar.addAction(self.openAction)
        toolbar.addAction(self.saveAction)
        toolbar.addSeparator()
        toolbar.addAction(self.undoAction)
        toolbar.addAction(self.redoAction)
        toolbar.addSeparator()
        toolbar.addAction(self.cutAction)
        toolbar.addAction(self.copyAction)
        toolbar.addAction(self.pasteAction)
        toolbar.addSeparator()
        toolbar.addAction(self.formatBoldAction)
        toolbar.addAction(self.formatItalicAction)
        toolbar.addAction(self.formatUnderlineAction)
        toolbar.addAction(self.formatBulletAction)
        toolbar.addAction(self.formatNumberedAction)
        toolbar.addSeparator()
        toolbar.addAction(self.formatSizeAction)
        toolbar.addAction(self.formatFontAction)
        toolbar.addAction(self.formatColorAction)

        
    def createShortcuts(self):
        newShortcut = QShortcut(QKeySequence.New, self)
        newShortcut.activated.connect(self.newNote)
        
        openShortcut = QShortcut(QKeySequence.Open, self)
        openShortcut.activated.connect(self.openNote)
        
        saveShortcut = QShortcut(QKeySequence.Save, self)
        saveShortcut.activated.connect(self.saveNote)
        
        saveAsShortcut = QShortcut(QKeySequence.SaveAs, self)
        saveAsShortcut.activated.connect(self.saveNoteAs)
        
        undoShortcut = QShortcut(QKeySequence.Undo, self)
        undoShortcut.activated.connect(self.textEdit.undo)
        
        redoShortcut = QShortcut(QKeySequence.Redo, self)
        redoShortcut.activated.connect(self.textEdit.redo)
        
        cutShortcut = QShortcut(QKeySequence.Cut, self)
        cutShortcut.activated.connect(self.textEdit.cut)
        
        copyShortcut = QShortcut(QKeySequence.Copy, self)
        copyShortcut.activated.connect(self.textEdit.copy)
        
        pasteShortcut = QShortcut(QKeySequence.Paste, self)
        pasteShortcut.activated.connect(self.textEdit.paste)
        
        selectAllShortcut = QShortcut(QKeySequence.SelectAll, self)
        selectAllShortcut.activated.connect(self.textEdit.selectAll)
        
        searchShortcut = QShortcut(QKeySequence.Find, self)
        searchShortcut.activated.connect(self.searchNote)
        
    def newNote(self):
        if self.noteChanged:
            response = self.promptSaveChanges()
            if response == QMessageBox.Save:
                self.saveNote()
            elif response == QMessageBox.Cancel:
                return
        self.textEdit.clear()
        self.setWindowTitle("Note Taking App")
        self.noteChanged = False
        
    def openNote(self):
        if self.noteChanged:
            response = self.promptSaveChanges()
            if response == QMessageBox.Save:
                self.saveNote()
            elif response == QMessageBox.Cancel:
                return
        filename, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "HTML Files (*.html *.htm)")
        if filename:
            with open(filename, 'r') as file:
                html_content = file.read()
                text_document = QTextDocument()
                text_document.setHtml(html_content)
                self.textEdit.setDocument(text_document)
                self.setWindowTitle(f"Note Taking App - {filename}")
                self.noteChanged = False

    def saveNoteAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "HTML Files (*.html *.htm)")
        if filename:
            with open(filename, 'w') as file:
                html_content = self.textEdit.document().toHtml()
                file.write(html_content)
            self.setWindowTitle(f"Note Taking App - {filename}")
            self.noteChanged = False
            QMessageBox.information(self, "Note Saved", "Note saved successfully.")

    def saveNote(self):
        if self.windowTitle() == "Note Taking App":
            self.saveNoteAs()
        else:
            filename = self.windowTitle().split(" - ")[-1]
            with open(filename, 'w') as file:
                html_content = self.textEdit.document().toHtml()
                file.write(html_content)
            self.setWindowTitle(f"Note Taking App - {filename}")
            self.noteChanged = False
            QMessageBox.information(self, "Note Saved", "Note saved successfully.")

        
    def promptSaveChanges(self):
        response = QMessageBox.question(self, "Save Changes", "Do you want to save the changes to the current note?",
                                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        return response
        
    def closeEvent(self, event):
        if self.noteChanged:
            response = self.promptSaveChanges()
            if response == QMessageBox.Save:
                self.saveNote()
            elif response == QMessageBox.Cancel:
                event.ignore()
                return
        self.saveSettings()
        event.accept()
        
    def searchNote(self):
        searchDialog = QInputDialog(self)
        searchDialog.setInputMode(QInputDialog.TextInput)
        searchDialog.setWindowTitle("Search")
        searchDialog.setLabelText("Search Text:")
        searchDialog.setOkButtonText("Search")
        searchDialog.setCancelButtonText("Cancel")
        if searchDialog.exec_() == QInputDialog.Accepted:
            searchText = searchDialog.textValue()
            flags = QTextDocument.FindFlags()
            flags |= QTextDocument.FindCaseSensitively
            if self.textEdit.find(searchText, flags):
                QMessageBox.information(self, "Search Result", "Text found.")
            else:
                QMessageBox.information(self, "Search Result", "Text not found.")
        
    def toggleBold(self):
        font = self.textEdit.currentFont()
        font.setBold(not font.bold())
        self.textEdit.setCurrentFont(font)
        
    def toggleItalic(self):
        font = self.textEdit.currentFont()
        font.setItalic(not font.italic())
        self.textEdit.setCurrentFont(font)
        
    def toggleUnderline(self):
        font = self.textEdit.currentFont()
        font.setUnderline(not font.underline())
        self.textEdit.setCurrentFont(font)
        
    def toggleBulletList(self):
        if self.textEdit.textCursor().currentList():
            self.textEdit.textCursor().createList()
        else:
            self.textEdit.textCursor().insertList(QTextListFormat.ListDisc)
        
    def toggleNumberedList(self):
        if self.textEdit.textCursor().currentList():
            self.textEdit.textCursor().createList()
        else:
            self.textEdit.textCursor().insertList(QTextListFormat.ListDecimal)
            
    def loadSettings(self):
        self.settings.beginGroup('MainWindow')
        self.resize(self.settings.value('size', QSize(500, 500)))
        self.move(self.settings.value('pos', QPoint(100, 100)))
        self.settings.endGroup()
        
    def saveSettings(self):
        self.settings.beginGroup('MainWindow')
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos', self.pos())
        self.settings.endGroup()

    def setFontSize(self):
        font, ok = QFontDialog.getFont(self)
        if ok:
            currentCursor = self.textEdit.textCursor()
            font.setPointSize(font.pointSize())  # Ensure explicit point size
            self.textEdit.setCurrentFont(font)

            # Reset the cursor to apply the font changes
            self.textEdit.setTextCursor(currentCursor)

    def setFont(self):
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.textEdit.setCurrentFont(font)


    def setTextColor(self):
        color = QColorDialog.getColor(self.textEdit.textColor(), self)
        if color.isValid():
            self.textEdit.setTextColor(color)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    noteApp = NoteTakingApp()
    noteApp.show()
    sys.exit(app.exec_())