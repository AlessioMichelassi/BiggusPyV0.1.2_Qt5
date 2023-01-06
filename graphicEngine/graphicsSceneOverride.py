import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class graphicSceneOverride(QGraphicsScene):
    itemSelected = pyqtSignal()
    itemsDeselected = pyqtSignal()

    def __init__(self, _sceneInterface=None, parent=None):
        super().__init__(parent)

        self.sceneInterface = _sceneInterface

        # settings
        self.gridSize = 10
        self.gridSquares = 5

        self._colorBackground = QColor("#393939")
        self._colorLight = QColor("#2f2f2f")
        self._colorDark = QColor("#292929")

        self._penLight = QPen(self._colorLight)
        self._penLight.setWidth(1)
        self._penDark = QPen(self._colorDark)
        self._penDark.setWidth(2)

        self.setBackgroundBrush(self._colorBackground)

    def setGraphicScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        _left = int(math.floor(rect.left()))
        _right = int(math.ceil(rect.right()))
        _top = int(math.floor(rect.top()))
        _bottom = int(math.ceil(rect.bottom()))

        firstLeftLine = _left - (_left % self.gridSize)
        firstTopLine = _top - (_top % self.gridSize)

        # compute all lines to be drawn
        linesLight, linesDark = [], []
        for x in range(firstLeftLine, _right, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                linesLight.append(QLine(x, _top, x, _bottom))
            else:
                linesDark.append(QLine(x, _top, x, _bottom))

        for y in range(firstTopLine, _bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                linesLight.append(QLine(_left, y, _right, y))
            else:
                linesDark.append(QLine(_left, y, _right, y))

        try:
            # draw the lines
            painter.setPen(self._penLight)
            painter.drawLines(*linesLight)

            painter.setPen(self._penDark)
            painter.drawLines(*linesDark)
        except Exception as e:
            pass