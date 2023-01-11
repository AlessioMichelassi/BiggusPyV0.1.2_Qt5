import contextlib
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from graphicElement.plugs.PlugGraphic import PlugGraphic
from graphicElement.connections.Connection import *


class superText(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Imposta il flag di evento per consentire di filtrare gli eventi
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

    def setText(self, text):
        self.parent.setValueFromGraphics(int(text))
        self.parent.nodeInterface.nodeData.calculate()
        self.parent.nodeInterface.notifyToObserver()

    def eventFilter(self, obj, event):
        # Verifica se l'evento è una pressione del tasto Invio
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Esegue l'azione desiderata (ad esempio, imposta il nuovo valore del testo)
            self.setText(self.toPlainText().strip())
            return True
        return super().eventFilter(obj, event)


class AbstractNodeGraphic(QGraphicsItem):
    # NodeGraphic parameter
    width: int = 50
    height: int = 100
    proxyWidget: QGraphicsProxyWidget
    borderColorDefault = QColor(10, 120, 10)
    borderColorSelect = QColor(255, 70, 10)
    backGroundColor = QColor(10, 180, 40)

    # NodeGraphics variable
    outputConnection = []
    nodeCounter = 0
    txtTitle: QGraphicsTextItem
    txtValue: QGraphicsTextItem
    valueContent: int
    nodeData = None
    nodeInterface = None
    drawFigure = "rect"
    isThereAProxyWidget = False

    def __init__(self, view, nodeInterface, parent=None):
        super().__init__(parent)
        self.graphicView = view
        self.nodeInterface = nodeInterface
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.setZValue(1)

        # Create the input and output plugs list as emptyList
        self.graphicInputPlugs = []
        self.graphicOutputPlugs = []

        # Create the label
        self.createTitleText()
        self.createValueText()

        # Create the bounding rect
        self.boundingRect = QRectF(0, 0, self.width, self.height)
        self.transform = QTransform()

        # Set the default position
        self.setPos(QPointF(0, 0))
        self.pythonLogo = QLabel()
        pixmap = QPixmap()
        pixmap.load('graphicElement/imgs/pythonLogo.png')
        self.pythonLogo.setPixmap(pixmap)
        self.pythonLogo.setMaximumSize(25, 25)
        self.pythonLogo.setScaledContents(True)
        self.pythonLogo.setStyleSheet("background-color: transparent;")
        self.proxyLogo = QGraphicsProxyWidget(self)
        self.proxyLogo.setWidget(self.pythonLogo)
        self.proxyLogo.setPos(self.width - 28, 2)

    def createTitleText(self):
        self.txtTitle = QGraphicsTextItem(self)
        self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.nodeInterface.nodeData.title)
        x = (self.txtTitle.boundingRect().width() // 3)
        self.txtTitle.setPos(-x, -30)  # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.txtTitle.setZValue(2)

    def createValueText(self):
        self.txtValue = superText(self)
        self.txtValue.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtValue.installEventFilter(self.txtValue)
        x = (self.txtValue.boundingRect().width() / 2)
        y = self.height / 2
        self.txtValue.setPos(x, y)  # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtValue.setPlainText("")
        self.txtValue.setDefaultTextColor(Qt.GlobalColor.black)
        self.txtValue.setZValue(2)

    def setValueFromGraphics(self, value, index: int = 0):
        # sourcery skip: assign-if-exp, hoist-statement-from-if
        if type(self.nodeData) == "NumberNode":
            self.nodeData.dataInPlugs[index].value = int(value)
        else:
            self.nodeData.dataInPlugs[index].value = value
        self.txtValue.setPlainText(str(value))
        with contextlib.suppress(AttributeError):
            self.nodeInterface.notifyToObserver()

    def updateTextValue(self):
        value = self.nodeData.dataOutPlugs[0].value
        self.txtValue.setPlainText(str(value))
        if self.isThereAProxyWidget:
            self.nodeData.updateText(value)

    def setTitle(self, text):
        self.txtTitle.setPlainText(text)
        textItemWidth = self.txtTitle.boundingRect().width()
        textItemHeight = self.txtTitle.boundingRect().height()
        x = (self.width - textItemWidth) / 2
        y = (self.height - textItemHeight) / 2
        self.txtTitle.setPos(x, -30)

    def createPlugsIn(self, inNumber):
        """
        La parte grafica dei Plug viene definita qui perchè
        varia in base alle dimensioni del nodo.
        :param inNumber:
        :return:
        """
        # Create the input and output plugs
        x = -8
        if inNumber == 0:
            return
        elif inNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // inNumber)
        for i in range(inNumber):
            plug = self.nodeInterface.nodeData.dataInPlugs[i].createGraphicPlug("In", self)
            plug.index = i
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3
            self.graphicInputPlugs.append(plug)

    def createPlugsOut(self, outNumber):
        x = self.width - 2
        if outNumber == 0:
            return
        elif outNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // outNumber)
        for i in range(outNumber):
            plug = self.nodeInterface.nodeData.dataOutPlugs[i].createGraphicPlug("Out", self)
            plug.index = i
            plug.setPos(QPointF(x, y))
            self.graphicOutputPlugs.append(plug)
            y += plug.diameter * 3

    def setProxyWidget(self, _proxyWidget: QWidget):
        if _proxyWidget is None:
            self.isThereAProxyWidget = False
        else:
            self.isThereAProxyWidget = True
            self.proxyWidget = QGraphicsProxyWidget(self)
            self.proxyWidget.setWidget(_proxyWidget)
            self.txtValue.hide()

    def redesign(self, width, height, type="rect"):
        """
        Basandosi sulle nuove dimensioni del nodo ricalcola la posizione del
        titolo e dei plug.
        :param width:
        :param height:
        :return:
        """
        self.width = width
        self.height = height
        self.boundingRect = QRectF(0, 0, self.width, self.height)
        if type == "rect":
            self.designRectangleShape()
        elif type == "diamond":
            self.designDiamondShape()

    def designRectangleShape(self):
        self.proxyLogo.setPos(self.width - 30, 2)
        textItemWidth = self.txtTitle.boundingRect().width()
        textItemHeight = self.txtTitle.boundingRect().height()
        x = (self.width - textItemWidth) / 2
        self.txtTitle.setPos(x, -30)
        inNumber = len(self.nodeData.dataInPlugs)
        x = -8
        if inNumber == 0:
            return
        elif inNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // inNumber)
        for i in range(inNumber):
            plug = self.nodeInterface.nodeData.dataInPlugs[i].plugGraphic
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3
        outNumber = len(self.nodeData.dataOutPlugs)
        x = self.width - 2
        if outNumber == 0:
            return
        elif outNumber == 1:
            y = self.height // 2
        else:
            y = (self.height // inNumber)
        for i in range(outNumber):
            plug = self.nodeInterface.nodeData.dataOutPlugs[i].plugGraphic
            plug.setPos(QPointF(x, y))
            y += plug.diameter * 3

        if self.isThereAProxyWidget:
            x = 10
            y = self.height - self.proxyWidget.size().height() - 5
            self.proxyWidget.setMaximumWidth(self.width - 20)
            self.proxyWidget.setPos(x, y)

    def designDiamondShape(self):
        self.height = self.width
        self.boundingRect = QRectF(0, 0, self.width, self.height)
        center_x = self.boundingRect.x() + self.boundingRect.width() / 2
        center_y = self.boundingRect.y() + self.boundingRect.height() / 2
        self.transform.translate(center_x, center_y)
        self.setBoundingRegionGranularity(0)
        self.transform.rotate(45)
        self.transform.scale(0.7, 0.7)
        self.transform.translate(-center_x, -center_y)

        self.boundingRect = self.boundingRect.united(self.shape().boundingRect())
        self.proxyLogo.setPos(self.width // 2 - 12, 10)
        textItemWidth = self.txtTitle.boundingRect().width()
        textItemHeight = self.txtTitle.boundingRect().height()
        x = (self.width - textItemWidth) // 2
        y = (self.height - textItemHeight) // 2
        self.txtTitle.setPos(x, -30)

        plug = self.nodeInterface.nodeData.dataInPlugs[0].plugGraphic
        self.nodeInterface.nodeData.dataInPlugs[0].changeName("signal")
        plug.setPos(10, 20)

        plug = self.nodeInterface.nodeData.dataInPlugs[1].plugGraphic
        plug.setPos(-10, self.height//2)

        plug = self.nodeInterface.nodeData.dataOutPlugs[0].plugGraphic
        plug.setPos(100, 20)

        plug = self.nodeInterface.nodeData.dataOutPlugs[1].plugGraphic
        plug.setPos(self.width//2, self.height)

        if self.isThereAProxyWidget:
            x = (self.width - textItemWidth) // 2
            y = self.height - 50
            self.proxyWidget.setMaximumWidth(self.width // 3)
            self.proxyWidget.setPos(x, y)
        self.drawFigure = "diamond"

    def boundingRect(self):
        return self.boundingRect.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the node
        if not self.isSelected():
            painter.setPen(self.borderColorDefault)
        else:
            painter.setPen(self.borderColorSelect)
        painter.setBrush(self.backGroundColor)
        if self.drawFigure == "rect":
            painter.drawRoundedRect(self.boundingRect, 5, 5)
        if self.drawFigure == "diamond":
            painter.setTransform(self.transform, True)
            painter.drawRoundedRect(self.boundingRect, 10, 10)

    def itemChange(self, change, value):
        # sourcery skip: merge-nested-ifs
        # Update the position of the plugs when the node is moved
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if len(self.outputConnection) > 0:
                for connection in self.outputConnection:
                    connection.updateGeometry()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Imposta il flag "selezionato" a True
            self.setSelected(True)
        # Chiamare la versione della superclasse del metodo mousePressEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Imposta il flag "selezionato" a False
            self.setSelected(False)
        # Chiamare la versione della superclasse del metodo mouseReleaseEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Sposta il nodo di una distanza pari alla differenza tra la posizione attuale del mouse
            # e la posizione del mouse al momento del click
            self.setPos(self.pos() + event.pos() - event.lastPos())
        # Chiamare la versione della superclasse del metodo mouseMoveEvent
        # per gestire gli altri tipi di pulsanti del mouse
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.nodeData.calculate()
