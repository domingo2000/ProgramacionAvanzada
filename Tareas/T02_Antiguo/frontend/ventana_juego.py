import sys
from os import path

from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QVBoxLayout, QWidget)

from parametros import (IMAGENES, UBICACION_VENTANAS, ALTO_CAPTURA, UBICACION_ZONA_CAPTURA,
                        TAMANO_VENTANAS, COLORES, FLECHA_ABAJO, FLECHA_ARRIBA, FLECHA_DERECHA,
                        FLECHA_IZQUERDA)
from frontend.entidades import Flecha, FlechaNormal, Flecha2
import time


class VentanaJuego(QWidget):
    senal_salir_juego = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.init_gui()
        self.flechas = []
        self.flecha_en_zona_captura = None

    def init_gui(self):
        # Parametros generales
        self.setFixedSize(*TAMANO_VENTANAS["ventana_juego"])
        self.setGeometry(*UBICACION_VENTANAS["ventana_juego"], self.width(), self.height())
        # Layout_principal
        self.vbox_principal = QVBoxLayout()
        self.crear_barra_superior()
        self.crear_parte_inferior()
        self.setLayout(self.vbox_principal)

    def crear_barra_superior(self):
        # BARRA SUPERIOR
        barra_superior = QLabel()
        # Layout Barra superior
        hbox_barra_superior = QHBoxLayout()
        hbox_barra_superior.addSpacing(100)
        # Imagen Logo
        label_imagen_logo = QLabel(self)
        label_imagen_logo.setGeometry(0, 0, 100, 100)
        imagen_logo = QPixmap(path.join(*IMAGENES["imagen_inicio"]))
        label_imagen_logo.setPixmap(imagen_logo)
        label_imagen_logo.setScaledContents(True)
        # Label Combo y Mayor Combo
        vbox_combos = QVBoxLayout()
        vbox_combos.addStretch(1)
        self.label_combo = QLabel("Combo: ")
        self.label_combo_mayor = QLabel("Mayor Combo: ")
        vbox_combos.addWidget(self.label_combo)
        vbox_combos.addWidget(self.label_combo_mayor)

        vbox_combos.addStretch(1)
        hbox_barra_superior.addLayout(vbox_combos)

        # Progreso Y aprobacion
        hbox_barra_superior.addStretch(1)
        # Layout Vertical
        vbox_progresos_aprobacion = QVBoxLayout()
        vbox_progresos_aprobacion.addStretch(1)
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

        vbox_progresos_aprobacion.addStretch(1)
        hbox_barra_superior.addLayout(vbox_progresos_aprobacion)
        hbox_barra_superior.addStretch(1)
        # Cancion Y dificultad y boton comenzar partida
        vbox_3 = QVBoxLayout()
        vbox_3.addStretch(1)
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
        # Boton Comenzar Ronda
        self.boton_comenzar_ronda = QPushButton("Comenzar Ronda")
        self.boton_comenzar_ronda.clicked.connect(self.comenzar_juego)  # TEMPORAL
        vbox_3.addWidget(self.boton_comenzar_ronda)

        vbox_3.addStretch(1)
        hbox_barra_superior.addLayout(vbox_3)

        # Botones pausar y salir
        vbox_4 = QVBoxLayout()
        vbox_4.addStretch(1)
        # Boton Pausar
        self.boton_pausar = QPushButton("Pausar")
        vbox_4.addWidget(self.boton_pausar)
        # Boton Salir
        self.boton_salir = QPushButton("salir")
        self.boton_salir.clicked.connect(self.salir)
        vbox_4.addWidget(self.boton_salir)

        vbox_4.addStretch(1)
        hbox_barra_superior.addLayout(vbox_4)
        # añadir a Layout Principal
        self.vbox_principal.addLayout(hbox_barra_superior)
        self.vbox_principal.addStretch(1)

    def crear_parte_inferior(self):
        # Barra flechas izquerda
        widget_izquerda = QWidget(self)
        widget_izquerda.setGeometry(0, 100, 200, 500)
        widget_izquerda.setStyleSheet("background-color: #D2B2F3;")
        # Zonas de captura
        self.zonas_captura = {}
        for i in range(4):
            label_zona_captura = QLabel(widget_izquerda)
            label_zona_captura.setStyleSheet("border: 1px solid black")
            label_zona_captura.setGeometry(UBICACION_ZONA_CAPTURA[0] + (i * ALTO_CAPTURA),
                                           UBICACION_ZONA_CAPTURA[1], ALTO_CAPTURA, ALTO_CAPTURA)
            pixmap_zona_captura = QPixmap(ALTO_CAPTURA, ALTO_CAPTURA)
            pixmap_zona_captura.fill(QColor(*COLORES["zona_captura"]))
            label_zona_captura.setPixmap(pixmap_zona_captura)
            self.zonas_captura[i] = label_zona_captura

        # Fondo Central
        label_fondo = QLabel(self)
        label_fondo.setGeometry(200, 100, 500, 500)
        imagen_fondo = QPixmap(path.join(*IMAGENES["imagen_fondo"]))
        label_fondo.setPixmap(imagen_fondo)
        label_fondo.setScaledContents(True)

        # Barra Tienda
        self.widget_tienda = QWidget(self)
        self.widget_tienda.setGeometry(700, 100, 200, 500)
        self.widget_tienda.setStyleSheet("background-color: #D2B2F3;")

    def comenzar_ronda(self):
        pass

    def pausar(self):
        pass

    def salir(self):
        print("Saliendo del juego")
        self.hide()
        self.senal_salir_juego.emit()

    def esconder_tienda(self):
        if self.widget_tienda.isHidden():
            self.widget_tienda.show()
        else:
            self.widget_tienda.hide()

    def crear_flecha(self):
        nueva_flecha = Flecha2(self)
        nueva_flecha.actualizar.connect(self.actualizar_label)
        nueva_flecha.senal_flecha_en_zona_captura.connect(self.manejar_flecha)
        self.flechas.append(nueva_flecha)

    def actualizar_label(self, label, y):
        flecha = self.sender()
        label.move(flecha.columna * 50, y)

    # Funcion para probar funcionalidad de las flechas por mientras TEMPORAL
    def comenzar_juego(self):
        print("Empezando Juego")
        self.crear_flecha()

    def manejar_flecha(self, flecha_dentro):
        flecha = self.sender()
        if flecha_dentro:
            self.flecha_en_zona_captura = flecha
            self.cambiar_color_captura(flecha, flecha_dentro)
        else:
            self.flecha_en_zona_captura = None
            self.cambiar_color_captura(flecha, flecha_dentro)

    def cambiar_color_captura(self, flecha, flecha_dentro):
        i = flecha.columna
        if flecha_dentro:
            self.zonas_captura[i].pixmap().fill(Qt.blue)
            self.zonas_captura[i].repaint()
        else:
            color = QColor(*COLORES["zona_captura"])
            self.zonas_captura[i].pixmap().fill(color)
            self.zonas_captura[i].repaint()

    def keyPressEvent(self, event):
        tecla = event.text()
        if self.flecha_en_zona_captura:
            flecha = self.flecha_en_zona_captura
            direccion = flecha.direccion
            direccion_a_tecla = {
                "arriba": FLECHA_ARRIBA,
                "abajo": FLECHA_ABAJO,
                "derecha": FLECHA_DERECHA,
                "izquerda": FLECHA_IZQUERDA,
            }
            if direccion_a_tecla[direccion] == tecla:
                print("Flecha capturada")
                flecha.destruir_flecha()
                self.flecha_en_zona_captura = None
                self.cambiar_color_captura(flecha, False)
            else:
                pass


if __name__ == "__main__":
    app = QApplication([])
    ventana_juego = VentanaJuego()
    ventana_juego.show()
    sys.exit(app.exec_())