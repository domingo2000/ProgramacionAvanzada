import sys
from os import path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QVBoxLayout, QWidget)

from parametros import IMAGENES


class VentanaJuego(QWidget):
    # Señales de clase

    def __init__(self):
        super().__init__()

        self.init_gui()
        self.show()

    def init_gui(self):

        # BARRA SUPERIOR
        barra_superior = QLabel()
        # Layout Barra superior
        hbox_barra_superior = QHBoxLayout()
        # Imagen Logo
        label_imagen_logo = QLabel()
        imagen_logo = QPixmap(path.join(*IMAGENES["imagen_inicio"]))
        label_imagen_logo.setPixmap(imagen_logo)
        hbox_barra_superior.addWidget(label_imagen_logo)
        # Label Combo y Mayor Combo
        vbox_combos = QVBoxLayout()
        self.label_combo = QLabel("Combo: ")
        self.label_combo_mayor = QLabel("Mayor Combo: ")
        vbox_combos.addWidget(self.label_combo)
        vbox_combos.addWidget(self.label_combo_mayor)
        hbox_barra_superior.addLayout(vbox_combos)
        # Progreso Y aprobacion
        # Layout Vertical
        vbox_progresos_aprobacion = QVBoxLayout()
        # Progreso
        hbox_progreso = QHBoxLayout()
        label_progreso = QLabel("Progreso: ")
        self.progressbar_progreso = QProgressBar()
        self.progressbar_progreso.setGeometry(50, 50, 40, 40)
        hbox_progreso.addWidget(label_progreso)
        hbox_progreso.addWidget(self.progressbar_progreso)
        vbox_progresos_aprobacion.addLayout(hbox_progreso)
        # Aprobacion
        hbox_aprobacion = QHBoxLayout()
        label_aprobacion = QLabel("Aprobación: ")
        self.progressbar_aprobacion = QProgressBar()
        self.progressbar_aprobacion.setGeometry(50, 50, 40, 40)
        hbox_aprobacion.addWidget(label_aprobacion)
        hbox_aprobacion.addWidget(self.progressbar_aprobacion)
        vbox_progresos_aprobacion.addLayout(hbox_aprobacion)

        hbox_barra_superior.addLayout(vbox_progresos_aprobacion)

        # Cancion Y dificultad y boton comenzar partida
        vbox_3 = QVBoxLayout()
        # Cancion
        hbox_cancion = QHBoxLayout()
        label_cancion = QLabel("Canción: ")
        self.cancion = QComboBox()
        hbox_cancion.addWidget(label_cancion)
        hbox_cancion.addWidget(self.cancion)
        vbox_3.addLayout(hbox_cancion)
        # Dificultad
        hbox_dificultad = QHBoxLayout()
        label_dificultad = QLabel("Dificultad: ")
        self.dificultad = QComboBox()
        hbox_dificultad.addWidget(label_dificultad)
        hbox_dificultad.addWidget(self.dificultad)
        vbox_3.addLayout(hbox_dificultad)
        # Dificultad
        hbox_barra_superior.addLayout(vbox_3)
        # Layout Principal
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_barra_superior)
        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication([])
    ventana_juego = VentanaJuego()
    sys.exit(app.exec_())
