import sys
from os import path
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QShortcut
import parametros as p
from backend.funciones import sleep
from entidades.pinguino import Pinguino

# Cargamos la interfaz
window_name, base_class = uic.loadUiType("qt-designer-ventana_juego.ui")


class VentanaJuego(window_name, base_class):
    senal_teclas_presionadas = pyqtSignal(set)
    senal_cargar_nivel = pyqtSignal(str, str)  # Cancion, Dificultad
    senal_salir_juego = pyqtSignal()
    senal_guardar_puntaje = pyqtSignal()
    senal_fijar_usuario = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.teclas_presionadas = set()
        self.setupUi(self)
        self.init_senales()
        self.init_gui()
        # Colider pista baile
        punto = self.pista_baile.pos()
        tamaño = self.pista_baile.size()
        self.colider_pista_baile = QRect(punto, tamaño)

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

        # Pinguinos de la tienda
        pos_pinguino_amarillo = QPoint(0, 180)
        pos_pinguino_celeste = QPoint(90, 180)
        pos_pinguino_morado = QPoint(0, 280)
        pos_pinguino_verde = QPoint(90, 280)
        pos_pinguino_rojo = QPoint(45, 380)
        pinguino_morado = Pinguino(self.tienda,
                                   path.join(*p.IMAGENES["pinguino_morado_neutro"]),
                                   qpoint=pos_pinguino_morado)
        pinguino_verde = Pinguino(self.tienda,
                                  path.join(*p.IMAGENES["pinguino_verde_neutro"]),
                                  qpoint=pos_pinguino_verde)
        pinguino_rojo = Pinguino(self.tienda,
                                 path.join(*p.IMAGENES["pinguino_rojo_neutro"]),
                                 qpoint=pos_pinguino_rojo)
        pinguino_celeste = Pinguino(self.tienda,
                                    path.join(*p.IMAGENES["pinguino_celeste_neutro"]),
                                    qpoint=pos_pinguino_celeste)
        pinguino_amarillo = Pinguino(self.tienda,
                                     path.join(*p.IMAGENES["pinguino_amarillo_neutro"]),
                                     qpoint=pos_pinguino_amarillo)

    def init_shortcuts(self):
        pass
    
    def mousePressEvent(self, event):
        print(event.pos())
    # Drag And Drop
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        pinguino_original = event.source()
        pinguino = Pinguino(self, pinguino_original.ruta_imagen, pos, iscopy=True)
        if not(pinguino.colider.intersects(self.colider_pista_baile)):
            pinguino.setParent(None)
        event.acceptProposedAction()

    def pausar(self):
        print("Pausando")
        pass

    def salir(self):
        self.senal_salir_juego.emit()
        self.hide()

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

    def comenzar_nuevo_juego(self, nombre_usuario):
        self.show()
        self.senal_fijar_usuario.emit(nombre_usuario)

    def esconder_tienda(self):
        self.tienda.hide()
