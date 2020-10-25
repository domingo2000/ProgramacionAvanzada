import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QSound
import parametros as p
from backend.funciones import sleep

# Cargamos la interfaz
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
        self.label_tecla_abajo.setText(p.FLECHA_ABAJO.upper())
        self.label_tecla_derecha.setText(p.FLECHA_DERECHA.upper())
        self.label_tecla_arriba.setText(p.FLECHA_ARRIBA.upper())
        self.label_tecla_izquierda.setText(p.FLECHA_izquierda.upper())

    def comenzar(self):
        cancion = self.opciones_cancion.currentText()
        dificultad = self.opciones_dificultad.currentText()
        self.senal_cargar_nivel.emit(cancion, dificultad)

    def keyPressEvent(self, event):
        tecla = event.text()
        if not event.isAutoRepeat():
            self.teclas_presionadas.add(tecla)
            self.actualizar_zona_captura(tecla)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if len(self.teclas_presionadas) > 0:
                print(f"Señal teclas presionadas: {self.teclas_presionadas}")
                self.senal_teclas_presionadas.emit(self.teclas_presionadas)
                self.despintar_zona_captura()
                self.teclas_presionadas = set()

    def actualizar_label(self, label, pos_x, pos_y):
        label.move(pos_x, pos_y)

    def destruir_label(self, label):
        label.parent = None

    def actualizar_label_combo(self, int):
        self.label_combo.setText(f"Combo: {int}")

    def actualizar_label_combo_maximo(self, int):
        self.label_combo_maximo.setText(f"Combo Máximo: {int}")

    def actualizar_progressbar_progreso(self, int):
        self.barra_progreso.setValue(int)

    def actualizar_progressbar_aprobacion(self, int):
        self.barra_aprobacion.setValue(int)

    def actualizar_zona_captura(self, tecla):
        if tecla == p.FLECHA_ABAJO:
            self.label_zona_captura_abajo.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_ARRIBA:
            self.label_zona_captura_arriba.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_DERECHA:
            self.label_zona_captura_derecha.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_izquierda:
            self.label_zona_captura_izquierda.setStyleSheet("background-color: blue;")
    
    def despintar_zona_captura(self):
        self.label_zona_captura_arriba.setStyleSheet("")
        self.label_zona_captura_abajo.setStyleSheet("")
        self.label_zona_captura_izquierda.setStyleSheet("")
        self.label_zona_captura_derecha.setStyleSheet("")
