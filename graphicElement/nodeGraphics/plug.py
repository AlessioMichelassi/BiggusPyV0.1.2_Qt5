import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Plug(QGraphicsItem):
    index = 0

    def __init__(self, name, diameter, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.name = name
        self.node = parent
        self.boundingRectangle = QRectF(-self.diameter // 2, -self.diameter // 2, self.diameter * 2, self.diameter * 2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setZValue(1)
        self.connection = None

    def __str__(self):
        self.node.nodeData.calculate()
        # sourcery skip: inline-immediately-returned-variable
        returnString = f"name: {self.name} not contains InPlugs or outPlugs"
        if "In" in self.name:
            returnString = f"name: {self.name}, index: {self.index}, " \
                           f"value: {self.node.nodeData.inPlugs[self.index]} " \
                           f"nodeParent {self.node.title}, connection: {self.connection}"
        elif "Out" in self.name:
            returnString = f"name: {self.name}, index: {self.index}, " \
                           f"value: {self.node.nodeData.outPlugs[self.index]} " \
                           f"nodeParent {self.node.title}, connection: {self.connection}"
        return returnString

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the plug
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
