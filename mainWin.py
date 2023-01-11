from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from widgets.canvas import canvas

"""
La classe MainWindow contiene una serie di metodi che inizializzano l'interfaccia utente, creano la barra di stato, 
inizializzano il menù e altre attività.

Il metodo init viene chiamato quando viene creata un'istanza della classe MainWindow e si occupa di inizializzare 
l'interfaccia utente chiamando il metodo initUI e di creare la barra di stato chiamando il metodo createStatusBar.

Il metodo initUI imposta il titolo e le dimensioni della finestra, imposta il widget canvas come widget centrale 
della finestra e imposta l'icona della finestra.

Il metodo createStatusBar crea la barra di stato e aggiunge un widget QLabel che mostra la posizione del mouse 
nella scena del canvas.

Il metodo initMenu crea il menù della finestra e aggiunge alcune azioni al menù File e al menù Modifica.
"""


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
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.2")
        self.setGeometry(100, 100, 800, 600)
        # Imposta il titolo della finestra
        self.setWindowTitle('BiggusPyV0.1.2')
        # Imposta l'icona della finestra
        self.setWindowIcon(QIcon('graphicElement/imgs/BiggusIcon.ico'))
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
        openAction = QAction('open', self)
        saveAction = QAction('save', self)
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')

        openAction.triggered.connect(self.open)
        saveAction.triggered.connect(self.save)
        exitAction.triggered.connect(qApp.quit)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Aggiungi un'azione al menù Modifica
        cutAction = QAction('Cut', self)
        cutAction.setShortcut('Ctrl+X')
        editMenu.addAction(cutAction)

    def save(self):
        data = self.canvas.saveScene()
        with open("testSave.txt", "w+") as f:
            f.write(data)

    def open(self):
        self.canvas.graphicScene.clear()
        data = ""
        with open("testSave.txt", "r") as f:
            data = f.read()

        self.canvas.deserialize(data)
