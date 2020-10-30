import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QErrorMessage
from PyQt5 import uic

window_name, base_class = uic.loadUiType("ui-inicio.ui")


class VentanaInicio(window_name, base_class):
    senal_verificar_usuario = pyqtSignal(str)
    senal_abrir_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def comenzar(self):
        self.senal_verificar_usuario.emit(self.entrada_usuario.text())

    def ranking(self):
        self.senal_abrir_ranking.emit()

    def alerta_usuario_incorrecto(self):
        error = QErrorMessage(self)
        error.showMessage("El nombre de usuario debe ser alfanumerico")
