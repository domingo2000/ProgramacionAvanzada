from os import path
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
import parametros as p


class Flecha(QLabel):
    contador_clase = 1
    senal_cambiar_posicion = pyqtSignal(QLabel, tuple)

    def __init__(self, direccion, parent, velocidad=p.VELOCIDAD_FLECHA, posicion=(0, 0)):
        super().__init__(parent)
        self.numero = Flecha.contador_clase
        Flecha.contador_clase += 1

        self.direccion = direccion
        self.velocidad = velocidad
        self.tipo = ""
        self.__pos = posicion

        # Label_Flecha
        self.pixmap = QPixmap()
        self.setGeometry(self.pos[0], self.pos[1], p.ALTO_FLECHA, p.ALTO_FLECHA)
        self.setStyleSheet("background-color: transparent;")
        self.setScaledContents(True)
        self.show()

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, valor):
        self.__pos = valor
        self.senal_cambiar_posicion.emit(self, self.pos)

    def mover(self):
        x = self.pos[0]
        y = self.pos[1] + self.velocidad * p.TASA_REFRESCO
        self.pos = (x, y)

    def cambiar_velocidad(self, velocidad):
        self.velocidad = velocidad
        if tipo == "dorada":
            print(self.velocidad)

    def capturar(self):
        self.setParent(None)
        self.hide()


class FlechaNormal(Flecha):

    def __init__(self, direccion, parent, posicion=(0, 0)):
        super().__init__(direccion, parent=parent, posicion=posicion)
        self.direccion = direccion
        self.tipo = "normal"
        pixmap = QPixmap(path.join(*p.IMAGENES_FLECHA[f"{self.direccion}_normal"]))
        self.setPixmap(pixmap)


class FlechaDorada(Flecha):

    def __init__(self, direccion, parent, posicion=(0, 0)):
        super().__init__(direccion, parent=parent, posicion=posicion)
        self.direccion = direccion
        self.tipo = "dorada"
        self.velocidad = p.VELOCIDAD_FLECHA_DORADA
        pixmap = QPixmap(path.join(*p.IMAGENES_FLECHA[f"{self.direccion}_dorada"]))
        self.setPixmap(pixmap)


class FlechaX2(Flecha):

    def __init__(self, direccion, parent, posicion=(0, 0)):
        super().__init__(direccion, parent=parent, posicion=posicion)
        self.direccion = direccion
        self.tipo = "x2"
        pixmap = QPixmap(path.join(*p.IMAGENES_FLECHA[f"{self.direccion}_x2"]))
        self.setPixmap(pixmap)


class FlechaHielo(Flecha):
    senal_reducir_velocidad_flechas = pyqtSignal(float)
    senal_devolver_velocidad_flechas = pyqtSignal(float)

    def __init__(self, direccion, parent, posicion=(0, 0)):
        super().__init__(direccion, parent=parent, posicion=posicion)
        self.direccion = direccion
        self.tipo = "hielo"
        pixmap = QPixmap(path.join(*p.IMAGENES_FLECHA[f"{self.direccion}_hielo"]))
        self.setPixmap(pixmap)

    def poder(self, duracion_nivel):
        pass
        """
        tiempo_reduccion = p.DURACION_EFECTO_HIELO * duracion_nivel
        self.timer_reduccion = QTimer()
        self.timer_reduccion.setInterval(tiempo_reduccion * 1000)
        self.timer_reduccion.setSingleShot(True)
        self.timer_reduccion.connect(self.senal_devolver_velocidad_flechas.emit)
        self.senal_reducir_velocidad_flechas.emit(p.TASA_REDUCCION_VELOCIDAD_HIELO,
                                                  p.DURACION_EFECTO_HIELO)
        """
