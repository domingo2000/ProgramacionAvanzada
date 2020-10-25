import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QSound
from widgets.ventana_nivel import VentanaNivel
from widgets.niveles import NivelPrincipiante
import parametros as p
from backend.funciones import sleep

# Cargamos el formulario usando uic
window_name, base_class = uic.loadUiType("qt-designer-ventana_juego.ui")


class VentanaJuego(window_name, base_class):
    senal_teclas_presionadas = pyqtSignal(set)
    senal_cargar_nivel = pyqtSignal(str, str)  # Cancion, Dificultad

    def __init__(self):
        super().__init__()
        self.teclas_presionadas = set()
        self.setupUi(self)
        self.init_senales()
        self.init_gui()

    def init_senales(self):
        # Coneccion senales propias
        self.boton_comenzar.clicked.connect(self.comenzar)

        # Senales externas
        self.senal_nivel_cargado = pyqtSignal()

    def init_gui(self):
        pass

    def comenzar(self):
        cancion = self.opciones_cancion.currentText()
        dificultad = self.opciones_dificultad.currentText()
        self.senal_cargar_nivel.emit(cancion, dificultad)
        # Resetea los combos
        self.actualizar_label_combo(0)
        self.actualizar_label_combo_maximo(0)

    def keyPressEvent(self, event):
        tecla = event.text()
        if not event.isAutoRepeat():
            self.teclas_presionadas.add(tecla)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if len(self.teclas_presionadas) > 0:
                print(f"Señal teclas presionadas: {self.teclas_presionadas}")
                self.senal_teclas_presionadas.emit(self.teclas_presionadas)
                self.teclas_presionadas = set()

    def actualizar_label(self, label, pos_x, pos_y):
        label.move(pos_x, pos_y)

    def destruir_label(self, label):
        label.parent = None

    def actualizar_label_combo(self, int):
        self.label_combo.setText(f"Combo: {int}")

    def actualizar_label_combo_maximo(self, int):
        self.label_combo_maximo.setText(f"Combo: {int}")
