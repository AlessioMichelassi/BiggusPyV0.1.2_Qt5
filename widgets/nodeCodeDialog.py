from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class nodeCodeEditorDialog(QDialog):
    btnClose: QPushButton
    lblName: QLabel
    txtInputName: QLineEdit
    mainLayout: QVBoxLayout
    lines: list

    def __init__(self, _item, parent=None):
        super(nodeCodeEditorDialog, self).__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.setupInterface()
        self.parentItem = _item
        self.initUI()

    def setupInterface(self):
        # change name textLine
        self.layoutName = QHBoxLayout()
        self.lblName = QLabel("name:")
        self.txtInputName = QLineEdit("untitled")
        self.layoutName.addWidget(self.lblName)
        self.layoutName.addWidget(self.txtInputName)

        self.layoutTitle = QHBoxLayout()
        self.lblTitle = QLabel("title:")
        self.txtInputTitle = QLineEdit("untitled")
        self.layoutTitle.addWidget(self.lblTitle)
        self.layoutTitle.addWidget(self.txtInputTitle)

        self.layoutCode = QVBoxLayout()
        self.lblCode = QLabel("Code:")
        self.txtInputCode = QPlainTextEdit("")
        self.layoutCode.addWidget(self.lblCode)
        self.layoutCode.addWidget(self.txtInputCode)

        self.mainLayout.addLayout(self.layoutName)
        self.mainLayout.addLayout(self.layoutTitle)
        self.mainLayout.addLayout(self.layoutCode)
        self.btnClose = QPushButton('Ok', self)
        self.mainLayout.addWidget(self.btnClose)
        self.btnClose.clicked.connect(self.OK)

    def initUI(self):
        """
        this part is for override
        :return:
        """
        pass

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        print(self.lines)

    def OK(self):
        self.parentItem.nodeInterface.name = self.txtInputName.text()
        self.parentItem.nodeInterface.txtTitle = self.txtInputTitle.text()
        self.close()

    def loadSourceCode(self, _fileName):
        with open(_fileName, 'r', encoding="utf-8") as f:
            lines = f.read()
        self.txtInputCode.setPlainText(lines)