import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QApplication
from os import path
import json


with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS_UIS = PARAMETROS["rutas_uis"]

window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["sala_espera"]))


class VentanaEspera(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.labels_usuarios = {}

    def anadir_usuario(self, nombre_usuario):
        label = QLabel(nombre_usuario)
        self.labels_usuarios[nombre_usuario] = label
        self.layout_usuarios.addWidget(label)

    def actualizar_usuarios(self, nombres_usuarios):
        for nombre_usuario in self.labels_usuarios.copy():
            label_usuario = self.labels_usuarios.pop(nombre_usuario)
            label_usuario.hide()
            label_usuario.setParent(None)
        for nombre_usuario in nombres_usuarios:
            self.anadir_usuario(nombre_usuario)

    def actualizar_label_sala_espera(self, string):
        self.label_sala_espera.setText(string)


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaEspera()
    sys.exit(app.exec_())
