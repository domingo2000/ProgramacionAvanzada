import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import parametros as p
from entidades.flechas import FlechaNormal, FlechaHielo, FlechaDorada, Flecha2, GeneradorFlecha
import random


class Nivel(QWidget):

    def __init__(self, duracion, tiempo_entre_pasos, aprobacion_necesaria):
        super().__init__()
        self.combo = 0
        self.combo_maximo = 0
        self.aprobacion_necesaria = aprobacion_necesaria
        self.tiempo_entre_pasos = tiempo_entre_pasos
        self.duracion = duracion

        # Generador
        self.generador_flechas = GeneradorFlecha(self.tiempo_entre_pasos, self)
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
        flechas = self.revisar_zona_captura()
        print(event.key())

    def revisar_zona_captura(self):  # Deberia ser backend
        flechas = self.generador_flechas.flechas
        tamaño_zona_captura = p.TAMANO_VENTANAS["zona_captura"]
        inicio_zona_captura = self.height() - tamaño_zona_captura
        final_zona_captura = self.height()
        for flecha in flechas:
            inicio_flecha = flecha.altura
            final_flecha = flecha.altura + flecha.label.height()
            if (inicio_zona_captura < inicio_flecha < final_zona_captura) or\
               (inicio_zona_captura < final_flecha < final_zona_captura):
                flecha.destruir()

            elif inicio_flecha > final_zona_captura:
                flecha.destruir()


class NivelPrincipiante(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_PRINCIPIANTE.values())


class NivelAficionado(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_AFICIONADO.values())


class NivelMaestroCumbia(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_MAESTRO_CUMBIA.values())
