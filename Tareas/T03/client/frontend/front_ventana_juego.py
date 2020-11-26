from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from os import path
import json

window_name, base_class = uic.loadUiType("ventana_juego.ui")
with open("parametros.json") as file:
    data = json.load(file)
    rutas_sprites = data["rutas_sprites"]


class VentanaJuego(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.labels_num_fichas = {
            "0": self.label_ficha0,
            "1": self.label_ficha1,
            "2": self.label_ficha2,
            "3": self.label_ficha3,
            "4": self.label_ficha4,
            "5": self.label_ficha5,
            "6": self.label_ficha6,
            "7": self.label_ficha7,
            "8": self.label_ficha8,
            "9": self.label_ficha9
        }

        self.labels_hexagonos = {
            "0": self.label_h0,
            "1": self.label_h1,
            "2": self.label_h2,
            "3": self.label_h3,
            "4": self.label_h4,
            "5": self.label_h5,
            "6": self.label_h6,
            "7": self.label_h7,
            "8": self.label_h8,
            "9": self.label_h9
        }
        self.labels_cartas_arcilla = {
            "0": self.arcilla_j0,
            "1": self.arcilla_j1,
            "2": self.arcilla_j2,
            "3": self.arcilla_j3,
        }
        self.labels_cartas_madera = {
            "0": self.madera_j0,
            "1": self.madera_j1,
            "2": self.madera_j2,
            "3": self.madera_j3,
        }
        self.labels_cartas_trigo = {
            "0": self.trigo_j0,
            "1": self.trigo_j1,
            "2": self.trigo_j2,
            "3": self.trigo_j3,
        }
        self.labels_dados = {
            "dado_1": self.dado_1,
            "dado_2": self.dado_2
        }
        self.labels_puntos = {
            "0": self.puntos_j0,
            "1": self.puntos_j1,
            "2": self.puntos_j2,
            "3": self.puntos_j3,
        }

    def actualizar_num_ficha(self, id_ficha, numero_ficha):
        label_num_ficha = self.labels_num_fichas[id_ficha]
        label_num_ficha.setText(str(numero_ficha))

    def actualizar_materia_prima_hexagono(self, id_hexagono, materia_prima):
        datos_ruta_pixmap = rutas_sprites[f"hex_{materia_prima}"]
        ruta_materia_prima = path.join(*datos_ruta_pixmap)
        pixmap_materia_prima = QPixmap(ruta_materia_prima)
        label_hexagono = self.labels_hexagonos[id_hexagono]
        label_hexagono.setPixmap(pixmap_materia_prima)

    def actualizar_puntos(self, dict_puntos):
        """
        Recibe un diccionario de la forma:
        {"id_jugador": puntos, "id_jugador_2": puntos,...}
        y actualiza los labels de los puntos
        """
        for id_jugador in dict_puntos:
            self.labels_puntos[id_jugador].setText(dict_puntos[id_jugador])

    def actualizar_cartas(self, dict_cartas):
        """
        Recibe un diccionario de la forma:
        {"id_jugador": {}, "id_jugador_2": puntos,...}
        y actualiza los labels de los puntos
        """
        for id_jugador in dict_puntos:
            self.labels_puntos[id_jugador].setText(dict_puntos[id_jugador])
