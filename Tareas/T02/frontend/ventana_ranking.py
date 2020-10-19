import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel,
                             QWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from parametros import IMAGENES, TAMANO_VENTANAS, UBICACION_VENTANAS
import time

class VentanaRanking(QWidget):
    senal_abrir_ventana_ranking = pyqtSignal()
    senal_abrir_ventana_inicio = pyqtSignal()
    senal_actualizar_puntajes = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.init_gui()
        print("DEBUG: Init ranking")
        self.senal_abrir_ventana_ranking.connect(self.abrir)
        self.senal_actualizar_puntajes.connect(self.actualizar_puntajes)
        # Señales para enviar
        self.senal_procesar_puntajes = None

    def init_gui(self):
        # Parametros de ventana
        self.setWindowTitle("Ventana de Ranking")
        self.setGeometry(*UBICACION_VENTANAS["ventana_ranking"], *TAMANO_VENTANAS["ventana_ranking"])
        # Titulo
        hbox_titulo = QHBoxLayout()
        titulo = QLabel()
        titulo.setTextFormat(Qt.RichText)
        titulo.setText("<h1><b>Ranking de puntajes</b></h1>")
        hbox_titulo.addStretch(1)
        hbox_titulo.addWidget(titulo)
        hbox_titulo.addStretch(1)

        # Puntajes
        self.labels_puntajes = [QLabel() for _ in range(5)]
        hbox_puntajes = []

        for i in range(5):
            hbox_puntaje = QHBoxLayout()
            hbox_puntaje.addStretch(1)
            hbox_puntaje.addWidget(self.labels_puntajes[i])
            hbox_puntaje.addStretch(2)
            hbox_puntajes.append(hbox_puntaje)

        # Botones
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)

        # Layout
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox_titulo)
        for i in range(5):
            self.vbox.addLayout(hbox_puntajes[i])
        self.vbox.addWidget(self.boton_volver)
        self.setLayout(self.vbox)

    def abrir(self):
        if self.senal_procesar_puntajes:
            self.senal_procesar_puntajes.emit()
        self.show()

    def actualizar_puntajes(self, puntajes):
        # Puntajes en formato [usuario, puntaje]
        print(puntajes)
        for i in range(len(puntajes)):
            usuario = puntajes[i][0]
            puntos = puntajes[i][1]
            self.labels_puntajes[i].setText(f"{usuario}: {puntos} pts")

    def volver(self):
        self.hide()
        self.senal_abrir_ventana_inicio.emit()
