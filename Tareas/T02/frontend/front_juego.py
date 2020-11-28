import sys
from PyQt5.QtCore import pyqtSignal, QRect, QEvent
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import parametros as p
from entidades.pinguinos import Pinguino
window_name, base_class = uic.loadUiType("ui-ventana-juego.ui")


class VentanaJuego(window_name, base_class):
    senal_abrir_ventana_inicio = pyqtSignal()
    senal_juego_terminado = pyqtSignal()
    senal_comenzar_juego = pyqtSignal()
    senal_comenzar_ronda = pyqtSignal(str, str)
    senal_teclas_presionadas = pyqtSignal(set)
    senal_pausar_juego = pyqtSignal()
    senal_reanudar_juego = pyqtSignal()
    senal_compra_realizada = pyqtSignal(Pinguino)
    senal_pinguino_dropeado = pyqtSignal(QEvent)
    senal_jugar_solo = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()
        self.teclas_presionadas = set()

    def init_gui(self):
        self.label_dinero_tienda.setText(f"Dinero: {p.DINERO_INCIAL}")
        self.label_valor_pinguino.setText(f"Valor Pinguino: {p.PRECIO_PINGUIRIN}")
        self.label_tecla_izquierda.setText(f"{p.FLECHA_IZQUIERDA}".upper())
        self.label_tecla_derecha.setText(f"{p.FLECHA_DERECHA}".upper())
        self.label_tecla_arriba.setText(f"{p.FLECHA_ARRIBA}".upper())
        self.label_tecla_abajo.setText(f"{p.FLECHA_ABAJO}".upper())

    def comenzar(self):
        self.show()
        self.senal_comenzar_juego.emit()

    def pausar(self):
        if self.boton_pausar.text() == "Pausar":
            self.senal_pausar_juego.emit()
            self.boton_pausar.setText("Reanudar")
        else:
            self.senal_reanudar_juego.emit()
            self.boton_pausar.setText("Pausar")

    def salir(self):
        self.hide()
        self.senal_juego_terminado.emit()
        self.senal_abrir_ventana_inicio.emit()

    def cambiar_pos_label(self, label, pos):
        label.move(*pos)

    def comenzar_ronda(self):
        print("BOTON COMENZAR RONDA")
        dificultad = self.opciones_dificultad.currentText()
        cancion = self.opciones_cancion.currentText()
        self.tienda.hide()
        self.senal_comenzar_ronda.emit(dificultad, cancion)

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            tecla = event.text()
            self.teclas_presionadas.add(tecla)
            self.actualizar_zona_captura(tecla)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if len(self.teclas_presionadas) > 0:
                print(f"Teclas presionadas {self.teclas_presionadas}")
                self.senal_teclas_presionadas.emit(self.teclas_presionadas)
                self.despintar_zona_captura()
                self.teclas_presionadas = set()

    def actualizar_zona_captura(self, tecla):
        print("Tecla pintandose")
        if tecla == p.FLECHA_ABAJO:
            self.label_zona_captura_abajo.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_ARRIBA:
            self.label_zona_captura_arriba.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_DERECHA:
            self.label_zona_captura_derecha.setStyleSheet("background-color: blue;")
        elif tecla == p.FLECHA_IZQUIERDA:
            self.label_zona_captura_izquierda.setStyleSheet("background-color: blue;")

    def despintar_zona_captura(self):
        self.label_zona_captura_arriba.setStyleSheet("")
        self.label_zona_captura_abajo.setStyleSheet("")
        self.label_zona_captura_izquierda.setStyleSheet("")
        self.label_zona_captura_derecha.setStyleSheet("")

    def actualizar_combo(self, int):
        self.label_combo.setText(f"Combo: {int}")

    def actualizar_combo_maximo(self, int):
        self.label_combo_maximo.setText(f"Combo Maximo: {int}")

    def actualizar_barra_progreso(self, int):
        self.barra_progreso.setValue(int)

    def actualizar_barra_aprobacion(self, int):
        self.barra_aprobacion.setValue(int)

    def actualizar_dinero_tienda(self, int):
        self.label_dinero_tienda.setText(f"Dinero: {int}")

    def actualizar_frame_label(self, label, pixmap):
        label.setPixmap(pixmap)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        pass

    def dropEvent(self, event):
        self.senal_pinguino_dropeado.emit(event)

    def reiniciar_botones(self):
        self.boton_comenzar.setEnabled(False)

    def activar_boton_comenzar(self):
        self.boton_comenzar.setEnabled(True)

    def desactivar_boton_comenzar(self):
        self.boton_comenzar.setEnabled(False)

    def activar_boton_jugar_solo(self, booleano):
        if booleano:
            self.boton_jugar_solo.setEnabled(True)
        else:
            self.boton_jugar_solo.setEnabled(False)

    def jugar_solo(self):
        self.activar_boton_jugar_solo(False)
        self.senal_jugar_solo.emit()

    def activar_opciones(self, booleano):
        self.opciones_dificultad.setEnabled(booleano)
        self.opciones_cancion.setEnabled(booleano)
