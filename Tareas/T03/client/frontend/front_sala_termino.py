import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QApplication, QHBoxLayout
from os import path
import json


with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS_UIS = PARAMETROS["rutas_uis"]

window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["sala_termino"]))


class VentanaTermino(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lugar = 0

    def anadir_usuario(self, nombre_usuario, puntos):
        self.lugar += 1
        layout = QHBoxLayout()
        label_pos_nombre = QLabel(f"{self.lugar}:  {nombre_usuario}")
        label_puntos = QLabel(f"{puntos} Pts")
        layout.addWidget(label_pos_nombre)
        layout.addStretch(1)
        layout.addWidget(label_puntos)
        self.layout_usuarios.addLayout(layout)

    def actualizar_label_ganador(self, ganador, es_ganador):
        if es_ganador:
            msg = f"Has Ganado  :)"
        else:
            msg = f"Has Perdido :("
        self.label_ganador.setText(msg)


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaEspera()
    sys.exit(app.exec_())
