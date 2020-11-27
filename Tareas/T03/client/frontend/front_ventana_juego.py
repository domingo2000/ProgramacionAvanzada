from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from os import path
import json

window_name, base_class = uic.loadUiType("ventana_juego.ui")
with open("parametros.json") as file:
    data = json.load(file)
    rutas_sprites = data["rutas_sprites"]


class VentanaJuego(window_name, base_class):
    senal_lanzar_dados = pyqtSignal()

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

        self.labels_usuarios = {
            "0": self.nombre_j0,
            "1": self.nombre_j1,
            "2": self.nombre_j2,
            "3": self.nombre_j3,
        }
        self.labels_materias_primas = {
            "arcilla": {"0": self.arcilla_j0,
                        "1": self.arcilla_j1,
                        "2": self.arcilla_j2,
                        "3": self.arcilla_j3},
            "madera": {"0": self.madera_j0,
                       "1": self.madera_j1,
                       "2": self.madera_j2,
                       "3": self.madera_j3},
            "trigo": {"0": self.trigo_j0,
                      "1": self.trigo_j1,
                      "2": self.trigo_j2,
                      "3": self.trigo_j3}
        }

        self.labels_dados = {
            "1": self.dado_1,
            "2": self.dado_2
        }
        self.labels_puntos = {
            "0": self.puntos_j0,
            "1": self.puntos_j1,
            "2": self.puntos_j2,
            "3": self.puntos_j3,
        }
        self.labels_nodos = {
            "0": self.label_nodo_0,
            "1": self.label_nodo_1,
            "2": self.label_nodo_2,
            "3": self.label_nodo_3,
            "4": self.label_nodo_4,
            "5": self.label_nodo_5,
            "6": self.label_nodo_6,
            "7": self.label_nodo_7,
            "8": self.label_nodo_8,
            "9": self.label_nodo_9,
            "10": self.label_nodo_10,
            "11": self.label_nodo_11,
            "12": self.label_nodo_12,
            "13": self.label_nodo_13,
            "14": self.label_nodo_14,
            "15": self.label_nodo_15,
            "16": self.label_nodo_16,
            "17": self.label_nodo_17,
            "18": self.label_nodo_18,
            "19": self.label_nodo_19,
            "20": self.label_nodo_20,
            "21": self.label_nodo_21,
            "22": self.label_nodo_22,
            "23": self.label_nodo_23,
            "24": self.label_nodo_24,
            "25": self.label_nodo_25,
            "26": self.label_nodo_26,
            "27": self.label_nodo_27,
            "28": self.label_nodo_28,
            "29": self.label_nodo_29,
            "30": self.label_nodo_30,
            "31": self.label_nodo_31,
            "32": self.label_nodo_32,
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

    def actualizar_materias_primas(self, dict_materias_primas):
        """
        Recibe un diccionario de la forma:
        {"id_jugador": {"madera": 0, "arcilla": 0, "trigo": 0},...}
        y actualiza los labels de las materias primas
        """
        for id_jugador in dict_materias_primas:
            for materia_prima in dict_materias_primas[id_jugador]:
                valor = dict_materias_primas[id_jugador][materia_prima]
                self.labels_materias_primas[materia_prima][id_jugador].setText(str(valor))

    def actualizar_construcciones(self, dict_nodos_pixmap):

        """
        Recibe un diccionario de la forma
        {"id_nodo": pixmap, "id_nodo_2": pixmap_2}
        y asigna los pixmaps a cada nodo.
        En caso de ser None el pixmap, esconde el label
        """
        for id_nodo in dict_nodos_pixmap:
            pixmap = dict_nodos_pixmap[id_nodo]
            label_nodo = self.labels_nodos[id_nodo]
            if pixmap:
                if label_nodo.isHidden():
                    label_nodo.show()
                label_nodo.setPixmap(pixmap)
            else:
                label_nodo.hide()

    def actualizar_label_usuario(self, id, usuario):
        if id == "0":
            self.labels_usuarios[id].setText(f"{usuario} (Tú)")    
        else:
            self.labels_usuarios[id].setText(usuario)

    def actualizar_labels_puntos(self, dict_id_puntos):
        """
        Recibe un diccionario de la forma
        {"id_usuario": puntos, "id_usuario2": puntos2}
        y actualiza los puntos en la interfaz
        """
        for id_usuario in dict_id_puntos:
            puntos = dict_id_puntos[id_usuario]
            self.labels_puntos[id_usuario].setText("Puntos: " + str(puntos))

    def actualizar_dados(self, pixmap_1, pixmap_2):
        self.labels_dados["1"].setPixmap(pixmap_1)
        self.labels_dados["2"].setPixmap(pixmap_2)

    def lanzar_dados(self):
        self.senal_lanzar_dados.emit()
        # self.boton_lanzar_dados.setEnabled(False)

    def activar_interfaz(self, bool):
        self.boton_lanzar_dados.setEnbled(bool)
        self.boton_carta_desarrollo.setEnabled(bool)

        # Completar codigo para construcciones
