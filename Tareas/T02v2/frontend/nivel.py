import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import parametros as p
from entidades.flechas import FlechaNormal, FlechaHielo, FlechaDorada, Flecha2
import random

class Nivel(QWidget):

    def __init__(self, duracion, tiempo_entre_pasos, aprobacion_necesaria):
        super().__init__()
        self.combo = 0
        self.combo_maximo = 0
        self.aprobacion_necesaria = aprobacion_necesaria
        self.tiempo_entre_pasos = tiempo_entre_pasos
        self.duracion = duracion
        self.init_gui()

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

    def generador_flechas(self):
        n = random.uniform(0, 1)
        if n < p.PROB_NORMAL:
            pass
            # GENERA FLECHA NORMAL
        elif p.PROB_NORMAL < n < p.PROB_NORMAL + p.PROB_FLECHA_DORADA:
            # GENERA DORADA
            pass
        elif p.PROB_NORMAL + p.PROB_FLECHA_DORADA < n < p.PROB_NORMAL + p.PROB_FLECHA_DORADA + p.PROB_FLECHA_X2:
            # GENERA X2
            pass
        else:
            pass
            # Genera Hielo


class NivelPrincipiante(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_PRINCIPIANTE.values())


class NivelAficionado(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_AFICIONADO.values())


class NivelMaestroCumbia(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_MAESTRO_CUMBIA.values())
