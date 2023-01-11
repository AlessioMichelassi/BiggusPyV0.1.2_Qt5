import contextlib
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from graphicElement.plugs.PlugGraphic import PlugGraphic
from graphicElement.connections.Connection import *



class MyGraphicItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.height = 50
        self.width = 100

        # Create a QPainterPath to define the diamond shape
        self.diamondPath = QPainterPath()
        self.diamondPath.moveTo(QPointF(0, -self.height / 2))
        self.diamondPath.lineTo(QPointF(self.width / 2, 0))
        self.diamondPath.lineTo(QPointF(0, self.height / 2))
        self.diamondPath.lineTo(QPointF(-self.width / 2, 0))
        self.diamondPath.closeSubpath()

        # Create a QTransform to rotate the diamond by 45 degrees
        self.diamond_transform = QTransform()
        self.diamond_transform.rotate(45)
        self.diamondPath = self.diamond_transform.map(self.diamondPath)

        # Calculate the offset between the original bounding rect and the transformed bounding rect
        self.offset = QPointF((self.width - self.diamondPath.boundingRect().width()) / 2,
                              (self.height - self.diamondPath.boundingRect().height()) / 2)

    def paint(self, painter, option, widget=None):
        # Draw the node
        if not self.isSelected():
            painter.setPen(self.borderColorDefault)
        else:
            painter.setPen(self.borderColorSelect)
        painter.setBrush(self.backGroundColor)
        painter.translate(self.offset)
        painter.drawRoundedRect(self.diamondPath.boundingRect(), 10, 10)

    def boundingRect(self):
        return QRectF(QPointF(0,0), self.height, self.width).normalized()
