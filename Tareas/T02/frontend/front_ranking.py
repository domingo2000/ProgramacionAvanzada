import sys
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from parametros import CANTIDAD_RANKING
import time


class VentanaRanking(QWidget):
    senal_abrir_ventana_inicio = pyqtSignal()
    senal_actualizar_puntajes = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        # Parametros de ventana
        self.setWindowTitle("Ventana de Ranking")
        self.setGeometry(50, 50, 470, 445)
        # Titulo
        hbox_titulo = QHBoxLayout()
        titulo = QLabel()
        titulo.setTextFormat(Qt.RichText)
        titulo.setText("<h1><b>Ranking de puntajes</b></h1>")
        hbox_titulo.addStretch(1)
        hbox_titulo.addWidget(titulo)
        hbox_titulo.addStretch(1)

        # Puntajes
        self.labels_puntajes = [QLabel() for _ in range(CANTIDAD_RANKING)]
        hbox_puntajes = []

        for i in range(CANTIDAD_RANKING):
            hbox_puntaje = QHBoxLayout()
            hbox_puntaje.addStretch(1)
            hbox_puntaje.addWidget(self.labels_puntajes[i])
            hbox_puntaje.addStretch(2)
            hbox_puntajes.append(hbox_puntaje)

        # Botones
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)

        # Layout
        vbox_principal = QVBoxLayout()
        vbox_principal.addLayout(hbox_titulo)
        for i in range(CANTIDAD_RANKING):
            vbox_principal.addLayout(hbox_puntajes[i])
        vbox_principal.addWidget(self.boton_volver)
        self.setLayout(vbox_principal)

    def actualizar_puntajes(self, puntajes):
        # Puntajes en formato [usuario, puntaje]
        for i in range(len(puntajes)):
            usuario = puntajes[i][0]
            puntos = puntajes[i][1]
            self.labels_puntajes[i].setText(f"{usuario}: {puntos} pts")

    def abrir(self):
        self.senal_actualizar_puntajes.emit()
        self.show()

    def volver(self):
        self.hide()
        self.senal_abrir_ventana_inicio.emit()
