import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel,
                             QWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from os import path
from parametros import IMAGENES


class VentanaRanking(QWidget):
    senal_abrir_ventana_ranking = pyqtSignal()
    senal_abrir_ventana_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        print("DEBUG: Init ranking")
        self.senal_abrir_ventana_ranking.connect(self.abrir)

    def init_gui(self):
        # Titulo
        titulo = QLabel("Ranking Puntajes")

        # Puntajes
        self.labels_puntajes = []
        self.puntaje1 = QLabel("Pedro 1999: 5000 pts")
        self.labels_puntajes.append(self.puntaje1)

        # Botones
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)
        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(titulo)
        for label_puntaje in self.labels_puntajes:
            vbox.addWidget(label_puntaje)
        vbox.addWidget(self.boton_volver)
        self.setLayout(vbox)

    def abrir(self):
        # COMPLETAR actualizar ventana rankings
        self.show()

    def volver(self):
        self.hide()
        self.senal_abrir_ventana_inicio.emit()
