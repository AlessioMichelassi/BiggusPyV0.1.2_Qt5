import os
import json
import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication
from mainWin import MainWindow

"""Il codice importa diverse librerie, come os, json, logging, e sys, che forniscono funzionalità di base come 
l'accesso al sistema operativo, la gestione dei file JSON, la registrazione di errori e la gestione della riga di 
comando.

Viene anche importato il modulo QApplication e alcuni altri moduli dalla libreria PyQt5, che fornisce un framework 
per creare interfacce utente per le applicazioni. In particolare, QApplication è necessario per avviare 
l'applicazione GUI (Graphical User Interface).

Il file include anche tre funzioni: save_data, load_data e setPalette. La prima funzione, save_data, salva i dati in 
un file JSON in un percorso specificato. La seconda funzione, load_data, carica i dati da un file JSON in un percorso 
specificato. La terza funzione, setPalette, imposta il colore del tema dell'applicazione su scuro.

Infine, viene definita la funzione main, che avvia l'applicazione GUI creando un'istanza di QApplication e un'istanza 
di MainWindow. Il MainWindow viene quindi visualizzato e l'applicazione entra in un ciclo di esecuzione, 
che viene interrotto quando l'utente chiude la finestra. Se il file viene eseguito direttamente, viene chiamata la 
funzione main."""


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
