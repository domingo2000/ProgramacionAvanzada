from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QPushButton
from PyQt5 import uic
import json
from os import path
import sys

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS_UIS = PARAMETROS["rutas_uis"]

window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["monopolio"]))


class DialogoMonopolio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["punto_victoria"]))


class DialogPuntoVictoria(window_name, base_class):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["intercambio_1"]))


class DialogIntercambio1():
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["intercambio_2"]))


class DialogIntercambio2():
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication([])
    ventana = QWidget()
    ventana.setGeometry(50, 50, 500, 500)
    ventana.show()
    dialog = DialogPuntoVictoria(ventana)
    dialog.exec()
    sys.exit(app.exec_())