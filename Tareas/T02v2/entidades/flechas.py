import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QTimer, QObject
from PyQt5.QtGui import QPixmap
import parametros as p
import random
import time


class Flecha(QObject):
    senal_actualizar = pyqtSignal(QLabel, int)

    def __init__(self, parent):
        super().__init__()
        # Atributos flecha abstracta
        self.velocidad = p.VELOCIDAD_FLECHA
        self.direccion = random.choice(p.DIRECCIONES)
        self.puntos = p.PUNTOS_FLECHA
        self.probabilidad = None  # float entre 0 y 1
        self.viva = True
        self.columna = 0
        self.__altura = p.ALTURA_INICIAL_FLECHA

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(p.TASA_DE_REFRESCO * 1000)
        self.timer.timeout.connect(self.actualizar_altura)

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, y):
        self.__altura = y
        self.label.move(self.columna * 50, y)
        self.senal_actualizar.emit(self.label, self.altura)

    def init_gui(self, ruta_imagen, parent):
        self.label = QLabel(parent)
        self.label.setGeometry(100, 100, 50, 50)
        imagen_flecha = QPixmap(path.join(*ruta_imagen))
        self.label.setPixmap(imagen_flecha)
        self.label.setScaledContents(True)
        self.label.setVisible(True)

        self.label.show()

    def actualizar_altura(self):
        self.altura += p.TASA_DE_REFRESCO * self.velocidad

    def capturar(self):
        pass

    def comenzar(self):
        print("COMENZANDO")
        self.timer.start()
        print(f" Esta activo: {self.timer.isActive()}")

    def cambiar_velocidad(self, ponderador):
        self.velocidad = self.velocidad * ponderador


class FlechaNormal(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_3"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_NORMAL
        self.columna = 0


class Flecha2(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_4"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_X2
        self.columna = 1


class FlechaDorada(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_2"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_DORADA
        self.columna = 2


class FlechaHielo(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_1"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_HIELO
        self.columna = 3


if __name__ == "__main__":
    app = QApplication([])

    ventana = QWidget()
    ventana.setGeometry(0, 0, 500, 500)
    flecha_normal = FlechaNormal(ventana)
    flecha_dorada = FlechaDorada(ventana)

    flecha_x2 = Flecha2(ventana)
    flecha_hielo = FlechaHielo(ventana)
    flecha_hielo.cambiar_velocidad(1 / 2)
    flecha_dorada.cambiar_velocidad(1.5)

    flecha_normal.comenzar()
    flecha_dorada.comenzar()
    flecha_hielo.comenzar()
    flecha_x2.comenzar()

    ventana.show()
    sys.exit(app.exec_())
