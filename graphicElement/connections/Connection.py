import json
import math
import sys
from collections import OrderedDict

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Arrow(QGraphicsItem):
    currentNode = None

    def __init__(self, startPlug: 'PlugGraphic', end_point, parent=None):
        super().__init__(parent)
        self.startPlug = startPlug
        self.endPlug = None
        self.start_point = startPlug.scenePos()
        self.end_point = end_point

    def setEndPoint(self, endPlug: 'PlugGraphic'):
        self.endPlug = endPlug
        self.end_point = self.endPlug.scenePos()
        self.update()  # Aggiorna la visualizzazione della freccia
        if self.currentNode is not None:
            self.currentNode.outputConnection.append(self)
            self.currentNode = None

    def establishConnection(self, endPlug: 'PlugGraphic'):
        # Crea una nuova freccia
        conn = Connection(self.startPlug, endPlug)
        # Aggiungi la freccia alla scena
        self.scene().addItem(conn)
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
    """
    startNode è sempre il nodo che da l'output
    end
    """
    def __init__(self, _outputPlug, _inputPlug, parent=None):
        super().__init__(parent)
        if "Out" in _outputPlug.plugData.name:
            self.outputPlug = _outputPlug
            self.outputNode = self.outputPlug.nodeGraphic.nodeData
            self.inputPlug = _inputPlug
            self.inputNode = self.inputPlug.nodeGraphic.nodeData
        elif "In" in _outputPlug.plugData.name:
            self.outputPlug = _inputPlug
            self.outputNode = self.outputPlug.nodeGraphic.nodeData
            self.inputPlug = _outputPlug
            self.inputNode = self.inputPlug.nodeGraphic.nodeData
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(-1)
        self.connect()

    def connect(self):
        outputNode = self.outputPlug.nodeGraphic
        inputNode = self.inputPlug.nodeGraphic
        outputNode.nodeInterface.connectPlug(inputNode.nodeData, self.inputPlug, self.outputPlug, self)

    def deleteConnection(self):
        self.outputPlug.nodeGraphic.disconnectPlug(self.outputPlug.nodeGraphic.nodeData, self.outputPlug,
                                                   self.inputPlug.nodeGraphic.nodeData, self.inputPlug)
        self.inputPlug.nodeGraphic.disconnectPlug(self.inputPlug.nodeGraphic.nodeData, self.inputPlug,
                                                  self.outputPlug.nodeGraphic.nodeData, self.outputPlug)
        self.scene().removeItem(self)

    def updateGeometry(self):
        # Aggiorna la posizione della connessione in base alla posizione dei plugs di origine e di destinazione
        self.setLine(QLineF(self.outputPlug.scenePos(), self.inputPlug.scenePos()))

    def boundingRect(self):
        return QRectF(self.outputPlug.scenePos(), self.inputPlug.scenePos()).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        if not self.isSelected():
            painter.setPen(QPen(QColor(0, 20, 20), 3))
        else:
            painter.setPen(QPen(QColor(250, 50, 50), 3))
        painter.drawLine(self.outputPlug.scenePos(), self.inputPlug.scenePos())

    def serialize(self):
        dicts = {
            'inputNodeName': self.inputNode.title,
            'inputPlug': self.inputPlug.index,
            'outputNodeName': self.outputNode.title,
            'outputPlug': self.outputPlug.index,
        }
        return json.dumps(dicts)