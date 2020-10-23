import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, QObject
import parametros as p
from entidades.flechas import FlechaNormal, FlechaHielo, FlechaDorada, Flecha2, GeneradorFlecha
import random


class VentanaNivel(QWidget):
    senal_tecla_presionada = pyqtSignal(object, str)

    def __init__(self, nivel):
        super().__init__()
        # Generador
        self.generador_flechas = GeneradorFlecha(nivel.tiempo_entre_pasos, self)
        self.nivel = nivel
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
        self.zonas_captura = []  # (label, colider)
        for i in range(4):
            tamaño = p.TAMANO_VENTANAS["zona_captura"]
            pos_x = i * tamaño
            pos_y = self.height() - tamaño
            zona_captura = ZonaCaptura(self, pos_x, pos_y)
            self.zonas_captura.append(zona_captura)

    def comenzar(self):
        self.generador_flechas.comenzar()
        # Completar empezar_cancion

    def terminar(self):
        self.generador_flechas.parar()
        # Esperar a que no hayan flechas
        # Completar parar_cancion
        # mostrar_ventana_resumen

    def actualizar_label(self, label, x, y):
        label.move(x, y)

    def actualizar_flecha(self, flecha, pos_x, pos_y):
        self.actualizar_label(flecha.label, pos_x, pos_y)
        flecha.colider.moveTopLeft(QPoint(pos_x, pos_y))
    
    def destruir_label(self, label):
        label.setParent(None)

    def keyPressEvent(self, event):
        tecla = event.text()
        self.senal_tecla_presionada.emit(self, tecla)


class ZonaCaptura(QObject):

    def __init__(self, parent, pos_x, pos_y):
        super().__init__()
        self.crear_label(parent, pos_x, pos_y)
        self.crear_colider(pos_x, pos_y)

    def crear_label(self, parent, pos_x, pos_y):
        tamaño = p.TAMANO_VENTANAS["zona_captura"]
        label = QLabel(parent)
        label.setGeometry(pos_x, pos_y, tamaño, tamaño)
        color = p.COLORES["zona_captura"]
        label.setStyleSheet(f"border: 1px solid black; background-color: {color};")
        label.show()

    def crear_colider(self, pos_x, pos_y):
        tamaño = p.TAMANO_VENTANAS["zona_captura"]
        self.colider = QRect(pos_x, pos_y, tamaño, tamaño)
