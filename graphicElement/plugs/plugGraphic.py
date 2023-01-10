import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class plugGraphic(QGraphicsItem):
    index = 0
    txtTitle: QGraphicsTextItem

    def __init__(self, plugInterface, diameter=8, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.plugInterface = plugInterface
        self.nodeGraphic = parent
        self.boundingRectangle = QRectF(-self.diameter // 2, -self.diameter // 2, self.diameter * 2, self.diameter * 2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(1)
        self.connection = None
        self.createTitleText()

    @property
    def name(self):
        return self.plugInterface.plugData.name

    def __str__(self):
        self.nodeGraphic.nodeData.calculate()
        # sourcery skip: inline-immediately-returned-variable
        returnString = f"name: {self.name}, index: {self.index}, " \
                       f"value: {self.nodeGraphic.nodeData.dataInPlugs[self.index].value} " \
                       f"nodeParent {self.nodeGraphic.nodeData.title}, connection: {self.plugInterface.connectedWith}"
        return returnString

    def createTitleText(self):
        font = QFont()
        font.setPointSize(10)
        self.txtTitle = QGraphicsTextItem(self)
        self.txtTitle.setFont(font)
        # self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.name)
        # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.defineTextPosition()
        self.txtTitle.setZValue(2)

    def defineTextPosition(self):
        x = self.txtTitle.boundingRect().width()
        if "In" in self.name:
            x = (x * -1) - 5
        elif "Out" in self.name:
            x = 10
        self.txtTitle.setPos(x, -10)

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the plugs
        painter.setBrush(Qt.GlobalColor.white)
        if not self.isSelected():
            painter.setPen(Qt.GlobalColor.black)
        else:
            painter.setPen(Qt.GlobalColor.red)
        _centerPoint = QPoint(self.diameter // 2, self.diameter // 2)
        painter.drawEllipse(_centerPoint, self.diameter, self.diameter)
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        _radius = self.diameter // 2

        painter.drawEllipse(_centerPoint, 3, 3)
