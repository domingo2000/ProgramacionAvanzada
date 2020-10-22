import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import parametros as p
from entidades.flechas import FlechaNormal, FlechaHielo, FlechaDorada, Flecha2, GeneradorFlecha
import random


class VentanaNivel(QWidget):
    senal_tecla_presionada = pyqtSignal(object, str)

    def __init__(self, nivel):
        super().__init__()
        # Generador
        self.generador_flechas = GeneradorFlecha(nivel.tiempo_entre_pasos, self)
        self.init_gui()
        # Timers Flechas

    def init_gui(self):
        # Parametros generales de ventana
        self.setGeometry(*p.UBICACION_VENTANAS["ventana_nivel"],
                         *p.TAMANO_VENTANAS["ventana_nivel"])
        color = p.COLORES["ventana_nivel"]
        self.setStyleSheet(f"background-color:  {color};")
        self.crear_zona_captura()

    def crear_zona_captura(self):
        self.zonas_captura = []
        for i in range(4):
            tamaño_label = p.TAMANO_VENTANAS["zona_captura"]
            label = QLabel(self)
            self.zonas_captura.append(label)
            label.setGeometry(i * tamaño_label, self.height() - tamaño_label,
                              tamaño_label, tamaño_label)
            color = p.COLORES["zona_captura"]
            label.setStyleSheet(f"border: 1px solid black; background-color: {color};")
            label.show()

    def comenzar(self):
        self.generador_flechas.comenzar()

    def actualizar_label(self, label, x, y):
        label.move(x, y)

    def destruir_label(self, label):
        label.setParent(None)

    def keyPressEvent(self, event):
        tecla = event.text()
        self.senal_tecla_presionada.emit(self, tecla)

