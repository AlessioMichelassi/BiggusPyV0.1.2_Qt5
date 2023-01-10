import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Arrow(QGraphicsItem):
    currentNode = None

    def __init__(self, startPlug: 'plugGraphic', end_point, parent=None):
        super().__init__(parent)
        self.startPlug = startPlug
        self.endPlug = None
        self.start_point = startPlug.scenePos()
        self.end_point = end_point

    def setEndPoint(self, endPlug: 'plugGraphic'):
        self.endPlug = endPlug
        self.end_point = self.endPlug.scenePos()
        self.update()  # Aggiorna la visualizzazione della freccia
        if self.currentNode is not None:
            self.currentNode.outputConnection.append(self)
            self.currentNode = None

    def establishConnection(self, endPlug: 'plugGraphic'):
        # Crea una nuova freccia

        conn = Connection(self.startPlug, endPlug)
        # Aggiungi la freccia alla scena
        self.startPlug.plugInterface.connection = conn
        self.scene().addItem(conn)
        endPlug.plugInterface.connection = conn
        return conn

    def updatePosition(self, pos):
        self.end_point = pos
        self.update()  # Aggiorna la visualizzazione della freccia

    def updateArrow(self):
        self.start_point = self.startPlug.scenePos()

    def boundingRect(self):
        # Definiamo un bounding rectangle che include entrambe i punti della freccia
        return QRectF(self.start_point, self.end_point).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        # Disegniamo la freccia utilizzando un QPainter
        painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
        painter.drawLine(self.start_point, self.end_point)


class Connection(QGraphicsItem):
    def __init__(self, _startPlug, _endPlug, parent=None):
        super().__init__(parent)
        self.startPlug = _startPlug
        self.endPlug = _endPlug
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(-1)
        self.connect()

    def canConnect(self, endPlug):
        return True

    def connect(self):
        startNode = self.startPlug.nodeGraphic
        startNode.connection = startNode
        endNode = self.endPlug.nodeGraphic
        endNode.connection = endNode
        startNode.nodeInterface.connectPlug(startNode.nodeData, self.startPlug, endNode.nodeData, self.endPlug)

    def deleteConnection(self):
        self.startPlug.nodeGraphic.disconnectPlug(self.startPlug.nodeGraphic.nodeData, self.startPlug,
                                                  self.endPlug.nodeGraphic.nodeData, self.endPlug)
        self.endPlug.nodeGraphic.disconnectPlug(self.endPlug.nodeGraphic.nodeData, self.endPlug,
                                                self.startPlug.nodeGraphic.nodeData, self.startPlug)
        self.scene().removeItem(self)

    def updateGeometry(self):
        # Aggiorna la posizione della connessione in base alla posizione dei plugs di origine e di destinazione
        self.setLine(QLineF(self.startPlug.scenePos(), self.endPlug.scenePos()))

    def boundingRect(self):
        return QRectF(self.startPlug.scenePos(), self.endPlug.scenePos()).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        if not self.isSelected():
            painter.setPen(QPen(QColor(0, 20, 20), 3))
        else:
            painter.setPen(QPen(QColor(250, 50, 50), 3))
        painter.drawLine(self.startPlug.scenePos(), self.endPlug.scenePos())
