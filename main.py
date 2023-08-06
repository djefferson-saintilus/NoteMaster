import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.movie = QMovie("loading.gif")
        self.label = QLabel(self)
        self.label.setMovie(self.movie)

        self.movie.start()

        # Set the size of the label containing the image
        self.label.setFixedSize(500, 500)

        self.setWindowTitle("Loading...")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()


class NoteTakingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filePath=None

        self.initUI()
        self.noteChanged = False
        self.currentFont = self.textEdit.font()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        self.textEdit.setStyleSheet("QTextEdit { margin: 20px; padding: 20px; }")
        self.textEdit.textChanged.connect(self.onTextChanged)

        self.createActions()
        self.createMenus()
        self.createToolbars()
        self.createShortcuts()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Note Taking App")

        self.show()

    def closeEvent(self, event):
        if self.noteChanged:
            self.savePrompt()
        event.accept()

    # New method to handle KeyboardInterrupt (Ctrl+C)
    def handleKeyboardInterrupt(self):
        if self.noteChanged:
            self.savePrompt()
        sys.exit(0)  # Exit the application gracefully

    def onTextChanged(self):
        self.noteChanged = True

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def insertTimestamp(self):
        cursor = self.textEdit.textCursor()
        cursor.insertText(QDateTime.currentDateTime().toString())

    def countWords(self):
        text = self.textEdit.toPlainText()
        wordCount = len(text.split())
        QMessageBox.information(self, "Word Count", f"Number of words: {wordCount}")

    def highlightSelection(self):
        cursor = self.textEdit.textCursor()
        selectedText = cursor.selectedText()
        if selectedText:
            fmt = QTextCharFormat()
            color = QColorDialog.getColor(self.textEdit.textBackgroundColor(), self)
            if color.isValid():
                fmt.setBackground(color)
                cursor.mergeCharFormat(fmt)
                self.textEdit.mergeCurrentCharFormat(fmt)

    def removeHighlight(self):
        cursor = self.textEdit.textCursor()
        selectedText = cursor.selectedText()
        if selectedText:
            fmt = QTextCharFormat()
            transparentBrush = QBrush(Qt.NoBrush)
            fmt.setBackground(transparentBrush)
            cursor.mergeCharFormat(fmt)


    def formatBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.formatBoldAction.isChecked() else QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def formatItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.formatItalicAction.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def formatUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.formatUnderlineAction.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def formatBullet(self):
        cursor = self.textEdit.textCursor()
        if self.formatBulletAction.isChecked():
            cursor.insertList(QTextListFormat.ListDisc)
        else:
            cursor.insertList(QTextListFormat.ListDisc)
        self.textEdit.setFocus()

    def formatNumbered(self):
        cursor = self.textEdit.textCursor()
        if self.formatNumberedAction.isChecked():
            cursor.insertList(QTextListFormat.ListDecimal)
        else:
            cursor.insertList(QTextListFormat.ListDisc)
        self.textEdit.setFocus()

    def formatSize(self):
        font, ok = QFontDialog.getFont(self.currentFont, self)
        if ok and font.pointSizeF() > 0:
            self.currentFont = QFont(font.family(), font.pointSizeF(), self.currentFont.weight(), self.currentFont.italic())
            self.textEdit.setFont(self.currentFont)
        elif not ok:
            # Show an error message if the user cancels the font dialog
            QMessageBox.warning(self, "Error", "Font selection canceled.")

    def formatFont(self):
        font, ok = QFontDialog.getFont(self.currentFont, self)
        if ok:
            self.currentFont = font
            self.textEdit.setFont(self.currentFont)
        elif not ok:
            # Show an error message if the user cancels the font dialog
            QMessageBox.warning(self, "Error", "Font selection canceled.")


    def formatColor(self):
        color = QColorDialog.getColor(self.textEdit.textColor(), self)
        if color.isValid():
            self.textEdit.setTextColor(color)
        elif not color.isValid():
            # Show an error message if the user cancels the color dialog
            QMessageBox.warning(self, "Error", "Color selection canceled.")

    def insertImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file:
            imageFormat = QImage(file).format()
            if imageFormat != QImage.Format_Invalid:
                # Get the original image size
                originalImage = QImage(file)
                originalWidth = originalImage.width()
                originalHeight = originalImage.height()

                # Prompt the user for the desired width and height in percentage
                width, ok1 = QInputDialog.getInt(self, "Image Size", "Enter width (in pixels):", originalWidth, 1, 2000)
                height, ok2 = QInputDialog.getInt(self, "Image Size", "Enter height (in pixels):", originalHeight, 1, 2000)

                if ok1 and ok2:
                    # Generate the img tag with inline styling using pixel values
                    img_tag = f'<img src="{file}" width="{width}" height="{height}">'
                    cursor = self.textEdit.textCursor()
                    cursor.insertHtml(img_tag)
                    # Move the cursor after the inserted image
                    cursor.movePosition(QTextCursor.End)
                    self.textEdit.setTextCursor(cursor)
                    # Set focus back to the textEdit widget
                    self.textEdit.setFocus()
                    self.noteChanged = True  # Mark the note as changed after inserting the image
                else:
                    QMessageBox.warning(self, "Error", "Invalid width/height value. Image insertion canceled.")
            else:
                QMessageBox.warning(self, "Error", "Invalid image format. Image insertion canceled.")
        else:
            QMessageBox.warning(self, "Error", "Image insertion canceled.")

    def insertHyperlink(self):
        link, ok = QInputDialog.getText(self, "Insert Hyperlink", "Enter URL:")
        if ok and link:
            cursor = self.textEdit.textCursor()
            cursor.insertHtml(f'<a href="{link}">{link}</a>')
        elif not ok:
            # Show an error message if the user cancels the input dialog
            QMessageBox.warning(self, "Error", "Hyperlink insertion canceled.")


    def createActions(self):
        self.newAction = QAction(QIcon("icons/new.png"), "New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.newNote)

        self.openAction = QAction(QIcon("icons/open.png"), "Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.openNote)

        self.saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveNote)

        self.exitAction = QAction(QIcon("icons/exit.png"), "Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.close)

        self.undoAction = QAction(QIcon("icons/undo.png"), "Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction = QAction(QIcon("icons/redo.png"), "Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.cutAction = QAction(QIcon("icons/cut.png"), "Cut", self)
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.copyAction = QAction(QIcon("icons/copy.png"), "Copy", self)
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.pasteAction = QAction(QIcon("icons/paste.png"), "Paste", self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.formatBoldAction = QAction(QIcon("icons/bold.png"), "Bold", self)
        self.formatBoldAction.setShortcut("Ctrl+B")
        self.formatBoldAction.setCheckable(True)
        self.formatBoldAction.triggered.connect(self.formatBold)

        self.formatItalicAction = QAction(QIcon("icons/italic.png"), "Italic", self)
        self.formatItalicAction.setShortcut("Ctrl+I")
        self.formatItalicAction.setCheckable(True)
        self.formatItalicAction.triggered.connect(self.formatItalic)

        self.formatUnderlineAction = QAction(QIcon("icons/underline.png"), "Underline", self)
        self.formatUnderlineAction.setShortcut("Ctrl+U")
        self.formatUnderlineAction.setCheckable(True)
        self.formatUnderlineAction.triggered.connect(self.formatUnderline)

        self.formatBulletAction = QAction(QIcon("icons/bullet.png"), "Bullet List", self)
        self.formatBulletAction.setShortcut("Ctrl+Shift+B")
        self.formatBulletAction.setCheckable(True)
        self.formatBulletAction.triggered.connect(self.formatBullet)

        self.formatNumberedAction = QAction(QIcon("icons/numbered.png"), "Numbered List", self)
        self.formatNumberedAction.setShortcut("Ctrl+Shift+N")
        self.formatNumberedAction.setCheckable(True)
        self.formatNumberedAction.triggered.connect(self.formatNumbered)

        self.formatSizeAction = QAction(QIcon("icons/size.png"), "Font Size", self)
        self.formatSizeAction.triggered.connect(self.formatSize)

        self.formatFontAction = QAction(QIcon("icons/font.png"), "Font Family", self)
        self.formatFontAction.triggered.connect(self.formatFont)

        self.formatColorAction = QAction(QIcon("icons/color.png"), "Font Color", self)
        self.formatColorAction.triggered.connect(self.formatColor)

        self.insertTimestampAction = QAction(QIcon("icons/timestamp.png"), "Insert Timestamp", self)
        self.insertTimestampAction.triggered.connect(self.insertTimestamp)

        self.countWordsAction = QAction("Count Words", self)
        self.countWordsAction.triggered.connect(self.countWords)

        self.highlightSelectionAction = QAction("Highlight Selection", self)
        self.highlightSelectionAction.triggered.connect(self.highlightSelection)

        self.removeHighlightAction = QAction("Remove Highlight", self)
        self.removeHighlightAction.triggered.connect(self.removeHighlight)

        self.insertImageAction = QAction(QIcon("icons/image.png"), "Insert Image", self)
        self.insertImageAction.triggered.connect(self.insertImage)

        self.insertHyperlinkAction = QAction(QIcon("icons/hyperlink.png"), "Insert Hyperlink", self)
        self.insertHyperlinkAction.triggered.connect(self.insertHyperlink)

    def createMenus(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)

        formatMenu = menubar.addMenu("&Format")
        formatMenu.addAction(self.formatBoldAction)
        formatMenu.addAction(self.formatItalicAction)
        formatMenu.addAction(self.formatUnderlineAction)
        formatMenu.addSeparator()
        formatMenu.addAction(self.formatBulletAction)
        formatMenu.addAction(self.formatNumberedAction)
        formatMenu.addSeparator()
        formatMenu.addAction(self.formatSizeAction)
        formatMenu.addAction(self.formatFontAction)
        formatMenu.addAction(self.formatColorAction)

        insertMenu = menubar.addMenu("&Insert")
        insertMenu.addAction(self.insertTimestampAction)
        insertMenu.addSeparator()
        insertMenu.addAction(self.insertImageAction)
        insertMenu.addAction(self.insertHyperlinkAction)

        toolsMenu = menubar.addMenu("&Tools")
        toolsMenu.addAction(self.countWordsAction)
        toolsMenu.addAction(self.highlightSelectionAction)
        toolsMenu.addAction(self.removeHighlightAction)

    def createToolbars(self):
        toolbar = self.addToolBar("Toolbar")

        toolbar.addAction(self.newAction)
        toolbar.addAction(self.openAction)
        toolbar.addAction(self.saveAction)
        toolbar.addSeparator()

        toolbar.addAction(self.cutAction)
        toolbar.addAction(self.copyAction)
        toolbar.addAction(self.pasteAction)
        toolbar.addSeparator()

        toolbar.addAction(self.undoAction)
        toolbar.addAction(self.redoAction)
        toolbar.addSeparator()

        toolbar.addAction(self.formatBoldAction)
        toolbar.addAction(self.formatItalicAction)
        toolbar.addAction(self.formatUnderlineAction)
        toolbar.addSeparator()

        toolbar.addAction(self.formatBulletAction)
        toolbar.addAction(self.formatNumberedAction)
        toolbar.addSeparator()

        toolbar.addAction(self.formatSizeAction)
        toolbar.addAction(self.formatFontAction)
        toolbar.addAction(self.formatColorAction)
        toolbar.addSeparator()

        toolbar.addAction(self.insertTimestampAction)
        toolbar.addSeparator()

        toolbar.addAction(self.insertImageAction)
        toolbar.addAction(self.insertHyperlinkAction)

    def createShortcuts(self):
        QShortcut("Ctrl+Z", self, self.textEdit.undo)
        QShortcut("Ctrl+Y", self, self.textEdit.redo)
        QShortcut("Ctrl+X", self, self.textEdit.cut)
        QShortcut("Ctrl+C", self, self.textEdit.copy)
        QShortcut("Ctrl+V", self, self.textEdit.paste)
        QShortcut("Ctrl+B", self, self.formatBold)
        QShortcut("Ctrl+I", self, self.formatItalic)
        QShortcut("Ctrl+U", self, self.formatUnderline)
        QShortcut("Ctrl+Shift+B", self, self.formatBullet)
        QShortcut("Ctrl+Shift+N", self, self.formatNumbered)
        QShortcut("Ctrl+S", self, self.saveNote)
        QShortcut("Ctrl+O", self, self.openNote)
        QShortcut("Ctrl+N", self, self.newNote)

    def newNote(self):
        if self.noteChanged:
            self.savePrompt()
        self.textEdit.clear()
        self.noteChanged = False

    def openNote(self):
        if self.noteChanged:
            self.savePrompt()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "HTML Files (*.html *.htm);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, "r") as file:
                    content = file.read()
                    self.textEdit.setHtml(content)
            except IOError:
                QMessageBox.critical(self, "Error", "Failed to open file.")
        self.noteChanged = False

    def saveNote(self):
        if self.filePath:
            fileName = self.filePath
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            filter = "HTML Files (*.html *.htm);;All Files (*)"
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Note", "", filter, options=options)

        if fileName:
            try:
                content = self.textEdit.toHtml()
                with open(fileName, "w") as file:
                    file.write(content)
                self.filePath = fileName
                self.noteChanged = False
                QMessageBox.information(self, "Saved", "Note saved successfully.")
            except IOError:
                QMessageBox.critical(self, "Error", "Failed to save file.")

    def savePrompt(self):
        reply = QMessageBox.question(self, "Save Changes", "Do you want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.saveNote()
        elif reply == QMessageBox.Cancel:
            return

    def closeEvent(self, event):
        if self.noteChanged:
            self.savePrompt()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Show the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()

    # Simulate some time-consuming operations here (e.g., loading data or initializing resources)
    # Instead of using time.sleep, we use QEventLoop to pause the execution
    delay_loop = QEventLoop()
    QTimer.singleShot(3000, delay_loop.quit)  # 3000 milliseconds (3 seconds) delay
    delay_loop.exec_()

    # Close the loading screen and start the main application
    loading_screen.close()
    window = NoteTakingApp()
    window.show()

    sys.exit(app.exec_())