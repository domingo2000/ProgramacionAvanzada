import sys
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton, QLabel, 
                             QWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from os import path
from parametros import IMAGENES


class Ventana_inicio(QWidget):

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.show()

    def init_gui(self):
        # Imagen de inicio
        hbox_imagen_inicio = QHBoxLayout()
        label_imagen_inicio = QLabel()
        ruta_imagen_inicio = path.join(*IMAGENES["imagen_inicio"])
        print(f"DEBUG: {ruta_imagen_inicio}")
        imagen_inicio = QPixmap(ruta_imagen_inicio)
        label_imagen_inicio.setPixmap(imagen_inicio)
        label_imagen_inicio.setScaledContents(True)
        hbox_imagen_inicio.addWidget(label_imagen_inicio)

        # Entrada
        texto_entrada = QLabel("Ingresa el nombre de tú bailarín:")
        self.entrada = QLineEdit()

        # Botones
        hbox_botones = QHBoxLayout()
        self.boton_comenzar = QPushButton("Comenzar")
        self.boton_comenzar.clicked.connect(self.comenzar)
        self.boton_ranking = QPushButton("Ir a Ranking")
        self.boton_ranking.clicked.connect(self.ranking)
        hbox_botones.addWidget(self.boton_comenzar)
        hbox_botones.addWidget(self.boton_ranking)

        # Layout
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_imagen_inicio)
        vbox.addWidget(texto_entrada)
        vbox.addWidget(self.entrada)
        vbox.addLayout(hbox_botones)
        self.setLayout(vbox)

    def comenzar(self):
        print("Comenzando Partida...")
        pass

    def ranking(self):
        print("Yendo a Ranking...")
        pass


if __name__ == "__main__":
    app = QApplication([])
    ventana_inicio = Ventana_inicio()
    sys.exit(app.exec_())