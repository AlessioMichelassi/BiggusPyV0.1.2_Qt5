from graphicElement.nodes.AbstractNodeGraphics import *

CANVAS_SCALE = 0.9
CENTER_ON = (430, 340)


class graphicViewOverride(QGraphicsView):

    scenePosChanged = pyqtSignal(int, int)

    # MOUSE BUTTON OVERRIDES VARIABLE
    lastMousePosition: QPointF = QPointF(0, 0)
    lastRightClickMousePosition: QPointF = QPointF(0, 0)
    lastLeftMouseBtnClickScenePos: QPointF = QPointF(0, 0)
    _middleMousePressed = False

    # KEY PRESSED OVERRIDES VARIABLE
    ctrlPressed = False

    # GUI FUNCTION OVERRIDES VARIABLE
    _isPanning = False
    _dragPos = None

    # OBJECT VARIABLE
    isConnectingPlug = False

    arrowList = []
    nodeList = []
    tempArrow = None

    def __init__(self, _graphicScene, parent=None):
        super(graphicViewOverride, self).__init__(parent)

        self.lastCTRLCopyFont = None
        self.lastCTRLCopyColor = None
        self.selectedItem = None
        self.graphicScene = _graphicScene
        self.mousePosition = QPoint(0, 0)
        self.setScene(self.graphicScene)
        self.canvas = None
        self.setRenderProperties()
        self.centerOn(CENTER_ON[0], CENTER_ON[1])
        self.scaleScene(CANVAS_SCALE)

    ####################################################
    #
    #
    #                  GENERAL GRAPHIC viEW sET UP
    #
    #
    ####################################################

    def setRenderProperties(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing
                            | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def wheelEvent(self, event):
        self.scaleScene(math.pow(2.0, -event.angleDelta().y() / 240.0))

    def keyPressEvent(self, event):  # sourcery skip: merge-nested-ifs
        self.checkKeyPressed(event)
        super(graphicViewOverride, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.lastMousePosition = event.pos()
        self.mousePosition = self.mapToScene(event.pos())
        self.mouseMove(event)
        self.scenePosChanged.emit(int(self.mousePosition.x()), int(self.mousePosition.y()))
        if self.isConnectingPlug:
            self.tempArrow.updatePosition(self.mapToScene(event.pos()))

    ####################################################
    #
    #
    #                  MOUSE OVERRIDING
    #
    #
    ####################################################

    def leftMouseButtonPress(self, event):
        """
            Nel caso in cui si prema CTRL+ LeftMB si può fare il pan della scena
            :param event: default mouse event
            :return: noyhing
        """
        self.selectedItem = self.getItemAtClick(event)
        if isinstance(self.selectedItem, plugGraphic):
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                print(self.selectedItem)
            else:
                self.createArrow(event)

    # LEFT MOUSE OVERRIDES
    def createArrow(self, event):
        # Crea una nuova freccia quando si clicca su un plugs
        self.isConnectingPlug = True
        self.tempArrow = Arrow(self.selectedItem, self.mapToScene(event.pos()))
        self.tempArrow.currentNode = self.selectedItem.parentItem()
        self.tempArrow.setZValue(-1)
        self.scene().addItem(self.tempArrow)

    def middleMouseButtonPress(self, event):
        self._middleMousePressed = True
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self._dragPos = event.pos()
        event.accept()
        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        pass

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)
        if self.isConnectingPlug and type(item) == plugGraphic:
            connection = self.tempArrow.establishConnection(item)
            connection.connect()
            self.scene().removeItem(self.tempArrow)
            self.tempArrow = None
        elif self.tempArrow:
            self.scene().removeItem(self.tempArrow)
            self.tempArrow = None
        self.isConnectingPlug = False

    def middleMouseButtonRelease(self, event):
        self._middleMousePressed = False
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self._isPanning = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMove(self, event):
        """
        Il pan della scena può avvenire o tenendo premuta la rotella
        oppure premendo CTRL+click sinistro
        :param event:
        :return:
        """
        if self._middleMousePressed:
            self._isPanning = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        if self._middleMousePressed and self._isPanning:
            self.panTheSceneWithMiddleMouse(event)

    def scaleScene(self, scaleFactor):
        """
        Questa funzione scala la scena. 1,1 aumenta 0,8 rimpicciolisce
        :param scaleFactor:
        :return:
        """
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)

    def setPanTheScene(self, event, isPanTheScene: bool):
        modifier = QApplication.keyboardModifiers()
        # Nel caso in cui non si possa utilizzare la rotella come terzo tasto del mouse
        # si può usare CTRL+LMB
        # Questa routine setta i cursori del mouse e le variabili per
        # l'override di mouseMove
        if isPanTheScene:
            self._dragPos = event.pos()
            if modifier == Qt.KeyboardModifier.ControlModifier:
                self._middleMousePressed = True
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self.setCursor(Qt.CursorShape.OpenHandCursor)
        elif modifier == Qt.KeyboardModifier.ControlModifier:
            self._middleMousePressed = False
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self._isPanning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def panTheSceneWithMiddleMouse(self, event):
        """
        Rispetto a panScene questa funzione sposta la scena in base ai movimenti del mouse
        """
        newPos = event.pos()
        diff = newPos - self._dragPos
        self._dragPos = newPos
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
        event.accept()

    ####################################################
    #
    #
    #                  KEY OVERRIDES
    #
    #
    ####################################################

    def checkKeyPressed(self, event):
        """
        Ogni volta che viene premuto un tasto avvia una funzione...
        :param event:
        :return:
        """
        key = event.key()
        if key == Qt.Key.Key_Plus:
            self.scaleScene(1.2)
        elif key == Qt.Key.Key_Minus:
            self.scaleScene(1 / 1.2)
        elif key == Qt.Key.Key_A:
            print("A pressed")
        elif key == Qt.Key.Key_S:
            print("B pressed")
        elif key == Qt.Key.Key_Delete:
            self.deleteObject(self.selectedItem)

        elif event.modifiers() and Qt.KeyboardModifier.ControlModifier:

            self.checkForModifier(event)
            # Questa parte controlla le sequenze di tasti

    def checkForModifier(self, event):
        """
        Se viene usato il tasto CTRL +
        :param event:
        :return:
        """
        if event.key() == Qt.Key.Key_C:
            if self.selectedItem:
                print("This override copy function")

        elif event.key() == Qt.Key.Key_V:
            if self.selectedItem:
                print("this will override paste function")

    ####################################################
    #
    #
    #                  Object Function
    #
    #
    ####################################################
    def getItemAtClick(self, event):
        """ Ritorna l'oggetto selezionato cliccandoci sopra"""
        pos = event.pos()
        return self.itemAt(pos)

    def deleteObject(self, obj):
        if isinstance(obj, Connection):
            obj.startPlug.plugInterface.disconnect()
            obj.endPlug.plugInterface.disconnect()
            self.scene().removeItem(obj)
        elif isinstance(obj, AbstractNodeGraphic):
            self.checkForPlugConnection(obj)

            self.scene().removeItem(obj)
        else:
            return

    def checkForPlugConnection(self, node):
        plugs = node.nodeData.dataInPlugs
        print(plugs)
        for plug in plugs:
            if plug.plugData.connectedWith:
                plug.disconnect()
                self.scene().removeItem(plug.plugGraphic)
            else:
                print(f"{plug.plugData.connectedWith}")
        plugs = node.nodeData.dataOutPlugs
        for plug in plugs:
            if plug.plugData.connectedWith is not None:
                plug.disconnect()
                self.scene().removeItem(plug.plugGraphic)
            else:
                print("no out plug")