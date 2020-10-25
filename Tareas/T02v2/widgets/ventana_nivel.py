from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, QObject, QTimer
from PyQt5.QtMultimedia import QSound
import parametros as p
from entidades.pasos import GeneradorPasos
from os import path
from backend.funciones import sleep
import random


class VentanaNivel(QWidget):
    senal_teclas_presionadas = pyqtSignal(object, set)  # Object es la misma ventana

    def __init__(self, nivel, duracion, parent, path_cancion=path.join(*p.CANCIONES["Cumbia"])):
        super().__init__(parent)
        self.teclas_presionadas = set()
        self.duracion = duracion
        # Generador
        self.generador_pasos = GeneradorPasos(nivel.tiempo_entre_pasos, self,
                                              nivel.pasos_dobles, nivel.pasos_triples)
        # Musica
        self.cancion = QSound(path_cancion)
        self.init_gui()

        # Timer nivel
        self.timer = QTimer()
        self.timer.setInterval(self.duracion * 1000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.terminar)

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
        self.timer.start()
        print("Comenzando Nivel :)")
        self.generador_pasos.comenzar()
        self.cancion.play()

    def terminar(self):
        print("Terminando Nivel")
        # Esperar a que no hayan flechas
        # Completar parar_cancion
        self.generador_pasos.parar()
        sleep(self.height() / p.VELOCIDAD_FLECHA)
        self.cancion.stop()
        # mostrar_ventana_resumen
        print("Nivel Terminado")

    def actualizar_label(self, label, x, y):
        label.move(x, y)

    def destruir_label(self, label):
        label.setParent(None)

    def keyPressEvent(self, event):
        tecla = event.text()
        if not event.isAutoRepeat():
            self.teclas_presionadas.add(tecla)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if len(self.teclas_presionadas) > 0:
                print(f"Señal teclas presionadas: {self.teclas_presionadas}")
                self.senal_teclas_presionadas.emit(self, self.teclas_presionadas)
                self.teclas_presionadas = set()


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
