from os import path

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QColor

from time import sleep

from parametros import (IMAGENES, UBICACION_FLECHAS, VELOCIDAD_FLECHA,
                        UBICACION_ZONA_CAPTURA, ALTO_FLECHA, ALTO_CAPTURA,
                        COLORES)
import random


class Flecha(QThread):
    actualizar = pyqtSignal(QLabel, int)
    senal_flecha_en_zona_captura = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.flecha_fuera = False
        direcciones_posibles = ("izquerda", "derecha", "arriba", "abajo")
        self.direccion = random.choice(direcciones_posibles)
        self.__altura = (UBICACION_FLECHAS["y"])
        self.columna = random.randint(0, 3)
        """
        self.ruta_imagen_flechas = {
            "arriba": IMAGENES["imagen_flecha_arriba_5"],
            "abajo": IMAGENES["imagen_flecha_abajo_5"],
            "derecha": IMAGENES["imagen_flecha_derecha_5"],
            "izquerda": IMAGENES["imagen_flecha_izquerda_5"]
        }
        """
        self.init_gui(parent)

    def init_gui(self, parent):
        if self.direccion == "arriba":
            ruta_imagen_flecha = self.ruta_imagen_flechas["arriba"]
        elif self.direccion == "abajo":
            ruta_imagen_flecha = self.ruta_imagen_flechas["abajo"]
        elif self.direccion == "derecha":
            ruta_imagen_flecha = self.ruta_imagen_flechas["derecha"]
        elif self.direccion == "izquerda":
            ruta_imagen_flecha = self.ruta_imagen_flechas["izquerda"]
        ruta_imagen_flecha = path.join(*ruta_imagen_flecha)
        self.label = QLabel(parent)
        self.label.setGeometry(self.columna * 50, UBICACION_FLECHAS["y"], 50, 50)
        self.label.setPixmap(QPixmap(ruta_imagen_flecha))
        self.label.setScaledContents(True)
        self.label.setVisible(True)

        self.label.show()
        self.start()

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, valor):
        self.__altura = valor
        self.actualizar.emit(self.label, self.altura)

    def run(self):
        while True:
            sleep(0.01)
            nuevo_y = self.altura + 0.01 * VELOCIDAD_FLECHA
            self.altura = nuevo_y
            self.chequear_zona_captura()

    def chequear_zona_captura(self):
        y = UBICACION_ZONA_CAPTURA[1] + 100
        if y < self.label.y() + ALTO_FLECHA < y + ALTO_CAPTURA:
            self.senal_flecha_en_zona_captura.emit(True)
        elif (self.label.y() > y + ALTO_CAPTURA) and not(self.flecha_fuera):
            self.senal_flecha_en_zona_captura.emit(False)
            self.flecha_fuera = True

    def destruir_flecha(self):
        self.label.hide()
        self.terminate()
        print("Flecha destruida")


class FlechaNormal(Flecha):

    def __init__(self, parent):
        self.tipo = "normal"
        self.ruta_imagen_flechas = {
            "arriba": IMAGENES["imagen_flecha_arriba_1"],
            "abajo": IMAGENES["imagen_flecha_abajo_1"],
            "derecha": IMAGENES["imagen_flecha_derecha_1"],
            "izquerda": IMAGENES["imagen_flecha_izquerda_1"]
        }
        super().__init__(parent)


class Flecha2(Flecha):
    def __init__(self, parent):
        self.tipo = "flecha2"
        self.ruta_imagen_flechas = {
            "arriba": IMAGENES["imagen_flecha_arriba_2"],
            "abajo": IMAGENES["imagen_flecha_abajo_2"],
            "derecha": IMAGENES["imagen_flecha_derecha_2"],
            "izquerda": IMAGENES["imagen_flecha_izquerda_2"]
        }
        super().__init__(parent)