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
    senal_teclas_presionadas = pyqtSignal(object, set)
    senal_cargar_nivel = pyqtSignal(str, str)  # Cancion, Dificultad

    def __init__(self):
        super().__init__()
        self.teclas_presionadas = set()
        self.nivel_cargado = False
        self.setupUi(self)
        self.init_senales()
        self.init_gui()

    def init_senales(self):
        # Coneccion senales propias
        self.boton_comenzar.clicked.connect(self.comenzar)

        # Senales externas
        self.senal_nivel_cargado = pyqtSignal()

    def init_gui(self):
        nivel = NivelPrincipiante()  # Nivel temporal para inicializar la ventana
        # Crea el widget del Nivel
        self.crear_ventana_nivel(nivel)

    def crear_ventana_nivel(self, nivel):
        self.ventana_nivel = VentanaNivel(nivel, nivel.duracion, parent=self)
        self.ventana_nivel.setGeometry(*p.UBICACION_VENTANAS["ventana_nivel"],
                                       *p.TAMANO_VENTANAS["ventana_nivel"])

    def comenzar(self):
        cancion = self.opciones_cancion.currentText()
        dificultad = self.opciones_dificultad.currentText()
        print("DEBUG dificulad, cancion", dificultad, cancion)
        self.senal_cargar_nivel.emit(cancion, dificultad)

        print("Hola")
        while not(self.nivel_cargado):
            sleep(0.1)
            print("Cargando Nivel")
            print(f"Nivel cargado = {self.nivel_cargado}")
        self.ventana_nivel.comenzar()
        self.ventana_nivel.show()
        nivel_cargado = False

    def keyPressEvent(self, event):
        tecla = event.text()
        if not event.isAutoRepeat():
            self.teclas_presionadas.add(tecla)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if len(self.teclas_presionadas) > 0:
                print(f"Señal teclas presionadas: {self.teclas_presionadas}")
                self.senal_teclas_presionadas.emit(self.ventana_nivel, self.teclas_presionadas)
                self.teclas_presionadas = set()

    def cargar_nivel(self, nivel, cancion):
        print("Debug: Ventana_juego Cargando nivel")
        self.ventana_nivel = VentanaNivel(nivel, nivel.duracion, parent=self)
        self.ventana_nivel.setGeometry(*p.UBICACION_VENTANAS["ventana_nivel"],
                                       *p.TAMANO_VENTANAS["ventana_nivel"])
        self.ventana_nivel.cancion = cancion

        # Conecta las señales con el nivel nuevo creado
        self.senal_teclas_presionadas.connect(nivel.manejar_teclas)
        self.nivel_cargado = True
