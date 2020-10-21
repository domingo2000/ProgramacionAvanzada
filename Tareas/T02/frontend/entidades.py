from os import path

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

from time import sleep

from parametros import IMAGENES, UBICACION_FLECHAS, VELOCIDAD_FLECHA


class Flecha(QThread):
    actualizar = pyqtSignal(QLabel, int)

    def __init__(self, parent):
        super().__init__()
        self.init_gui(parent)

        self.__altura = (UBICACION_FLECHAS["flecha_1"][1])

    def init_gui(self, parent):
        ruta_imagen_flecha = path.join(*IMAGENES["imagen_flecha"])
        self.label = QLabel(parent)
        self.label.setGeometry(*UBICACION_FLECHAS["flecha_1"], 50, 50)
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
            print("Corriendo flecha")
            sleep(0.1)
            nuevo_y = self.altura + 0.1 * VELOCIDAD_FLECHA
            self.altura = nuevo_y
