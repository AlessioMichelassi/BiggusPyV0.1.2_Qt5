from PyQt5.QtWidgets import *

from widgets.canvas import canvas


class MainWindow(QMainWindow):

    canvas: canvas
    statusMousePosition: QLabel
    filename = "untitled"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.createStatusBar()
        self.initMenu()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        # Imposta il titolo della finestra
        self.setWindowTitle('BiggusPyV0.1.2')
        # Imposta l'icona della finestra
        # self.setWindowIcon(QIcon('path/to/icon.png'))
        self.canvas = canvas()
        self.setCentralWidget(self.canvas)

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")

    def initMenu(self):
        # Crea il menù
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        # Aggiungi un'azione al menù File
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        # Aggiungi un'azione al menù Modifica
        cutAction = QAction('Cut', self)
        cutAction.setShortcut('Ctrl+X')
        editMenu.addAction(cutAction)