import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from frontend.nivel2 import VentanaNivel
from backend.backend_nivel2 import NivelPrincipiante, NivelAficionado, NivelMaestroCumbia
import parametros as p

# Cargamos el formulario usando uic
window_name, base_class = uic.loadUiType("qt-designer-ventana_juego.ui")


class VentanaJuego(window_name, base_class):
    senal_teclas_presionadas = pyqtSignal(object, set)

    def __init__(self):
        super().__init__()
        self.teclas_presionadas = set()

        self.setupUi(self)
        self.init_senales()
        self.init_gui()

    def init_senales(self):
        self.boton_comenzar.clicked.connect(self.comenzar)

    def init_gui(self):
        self.nivel = NivelAficionado()
        # Crea el widget del Nivel
        self.ventana_nivel = VentanaNivel(self.nivel, self.nivel.duracion, parent=self)
        self.ventana_nivel.setGeometry(*p.UBICACION_VENTANAS["ventana_nivel"],
                                       *p.TAMANO_VENTANAS["ventana_nivel"])

    def comenzar(self):
        print("Comenzando Ronda")
        self.ventana_nivel.comenzar()

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