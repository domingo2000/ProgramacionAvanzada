import sys
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("qt-designer-ventana-resumen.ui")


class VentanaResumen(window_name, base_class):
    senal_volver = pyqtSignal()
    senal_abrir_ventana_inicio = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ventana_a_volver = None
        self.setupUi(self)
        self.init_senales()

    def init_senales(self):
        self.boton_volver.clicked.connect(self.volver)

    def actualizar(self, puntaje_obtenido, puntaje_acumulado, combo_maximo,
                   cantidad_pasos_fallados, porcentaje_aprobacion, mensaje, ventana_a_volver,
                   interrumpido=False):

        self.label_puntaje_obtenido.setText(str(puntaje_obtenido))
        self.label_puntaje_acumulado.setText(str(puntaje_acumulado))
        self.label_combo_maximo.setText(str(combo_maximo))
        self.label_cantidad_pasos_fallados.setText(str(cantidad_pasos_fallados))
        self.label_aprobacion.setText(str(porcentaje_aprobacion))
        self.label_mensaje_final.setText(mensaje)

        self.ventana_a_volver = ventana_a_volver
        if not interrumpido:
            self.show()

    def volver(self):
        if self.ventana_a_volver == "ventana_inicio":
            self.senal_abrir_ventana_inicio.emit()
        elif self.ventana_a_volver == "ventana_juego":
            self.senal_abrir_ventana_juego.emit()
        self.hide()
