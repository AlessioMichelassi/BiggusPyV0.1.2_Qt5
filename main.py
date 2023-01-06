import os
import json
import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication
from mainWin import MainWindow


def save_data(data, file_path):
    if not os.path.exists(file_path):
        logging.error(f"Il file {file_path} non esiste")
        return
    with open(file_path, "w") as f:
        json.dump(data, f)


def load_data(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Il file {file_path} non esiste")
        return
    with open(file_path, "r") as f:
        return json.load(f)


def setPalette(app):
    app.setStyle("Fusion")
    darkPalette = app.palette()
    darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 127, 127), )
    darkPalette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    darkPalette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 127, 127), )
    darkPalette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
    darkPalette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(127, 127, 127),)
    darkPalette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    darkPalette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(80, 80, 80), )
    darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(127, 127, 127), )
    app.setPalette(darkPalette)


def main():
    app = QApplication(sys.argv)
    setPalette(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
