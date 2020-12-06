from PyQt5.QtWidgets import QLabel, QWidget, QErrorMessage
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QDropEvent
from PyQt5.QtCore import pyqtSignal, QEvent, QRect, QPoint
from os import path
from frontend.dialogs import (DialogoMonopolio, DialogPuntoVictoria,
                              DialogIntercambio1, DialogIntercambio2)
from frontend.construcciones import Choza
from frontend.ladron import Ladron
import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS_UIS = PARAMETROS["rutas_uis"]
    RUTAS_SPRITES = PARAMETROS["rutas_sprites"]

window_name, base_class = uic.loadUiType(path.join(*RUTAS_UIS["ventana_juego"]))


class VentanaJuego(window_name, base_class):
    senal_lanzar_dados = pyqtSignal()
    senal_activar_carta_desarrollo = pyqtSignal(str)
    senal_comprar_carta_desarrollo = pyqtSignal()
    senal_pasar_turno = pyqtSignal()
    senal_casa_dropeada = pyqtSignal(str)
    senal_label_dropeado = pyqtSignal(QLabel, QDropEvent)
    senal_ladron_dropeado = pyqtSignal(str)
    senal_proponer_intercambio = pyqtSignal(str, str, int, int, str)
    senal_realizar_intercambio = pyqtSignal(bool)
    senal_pedir_usuarios_intercambio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_dialogs()
        self.init_gui()

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

    def init_dialogs(self):
        self.dialogo_monopolio = DialogoMonopolio(self)
        self.dialogo_punto_victoria = DialogPuntoVictoria(self)
        self.dialogo_intercambio_1 = DialogIntercambio1(self)
        self.dialogo_intercambio_2 = DialogIntercambio2(self)

    def init_gui(self):
        self.casa_interfaz = Choza(0, 0, self)
        self.barra_usuario.layout().addWidget(self.casa_interfaz, 1, 3)
        self.ladron = Ladron(0, 0, self)
        self.barra_usuario.layout().addWidget(self.ladron, 0, 0)

    def actualizar_num_ficha(self, id_ficha, numero_ficha):
        label_num_ficha = self.labels_num_fichas[id_ficha]
        label_num_ficha.setText(str(numero_ficha))

    def actualizar_materia_prima_hexagono(self, id_hexagono, materia_prima):
        datos_ruta_pixmap = RUTAS_SPRITES[f"hex_{materia_prima}"]
        ruta_materia_prima = path.join(*datos_ruta_pixmap)
        pixmap_materia_prima = QPixmap(ruta_materia_prima)
        label_hexagono = self.labels_hexagonos[id_hexagono]
        label_hexagono.setPixmap(pixmap_materia_prima)

    def actualizar_puntos_usuario(self, id_usuario, puntos):
        self.labels_puntos[id_usuario].setText("Puntos: " + str(puntos))

    def actualizar_puntos_victoria_usuario(self, puntos_victoria):
        self.puntos_victoria.setText(f": {str(puntos_victoria)}")

    def activar_dialogo_puntos_victoria(self, ruta_label_punto_victoria):
        ruta_pixmap = path.join(*ruta_label_punto_victoria)
        self.dialogo_punto_victoria.label_carta.setPixmap(QPixmap(ruta_pixmap))
        self.dialogo_punto_victoria.exec()
        self.senal_activar_carta_desarrollo.emit("")

    def activar_dialogo_monopolio(self, ruta_label_monopolio):
        ruta_pixmap = path.join(*ruta_label_monopolio)
        self.dialogo_monopolio.label_carta.setPixmap(QPixmap(ruta_pixmap))
        self.dialogo_monopolio.exec()
        materia_prima = self.dialogo_monopolio.materia_prima.currentText()
        self.senal_activar_carta_desarrollo.emit(materia_prima)

    def pedir_usuarios_intercambio(self):
        self.senal_pedir_usuarios_intercambio.emit()
        self.deshabilitar_interfaz()

    def abrir_ventana_intercambio_1(self, lista_nombres):
        for nombre in lista_nombres:
            self.dialogo_intercambio_1.jugador_elegido.addItem(nombre)
        self.dialogo_intercambio_1.exec()
        materia_ofrecida = self.dialogo_intercambio_1.materia_ofrecida.currentText()
        materia_pedida = self.dialogo_intercambio_1.materia_pedida.currentText()
        cantidad_materia_ofrecida = self.dialogo_intercambio_1.cantidad_materia_ofrecida.value()
        cantidad_materia_pedida = self.dialogo_intercambio_1.cantidad_materia_pedida.value()
        jugador_elegido = self.dialogo_intercambio_1.jugador_elegido.currentText()
        self.senal_proponer_intercambio.emit(materia_ofrecida, materia_pedida,
                                             cantidad_materia_ofrecida, cantidad_materia_pedida,
                                             jugador_elegido)
        self.dialogo_intercambio_1.jugador_elegido.clear()

    def abrir_ventana_intercambio_2(self, materia_recibida, materia_pedida,
                                    cant_materia_recibida, cant_materia_pedida, nombre_oferente):
        self.dialogo_intercambio_2.materia_recibida.setText(materia_recibida)
        self.dialogo_intercambio_2.materia_pedida.setText(materia_pedida)
        self.dialogo_intercambio_2.cantidad_materia_recibida.setText(str(cant_materia_recibida))
        self.dialogo_intercambio_2.cantidad_materia_pedida.setText(str(cant_materia_pedida))
        self.dialogo_intercambio_2.nombre_oferente.setText(nombre_oferente)
        aceptado = self.dialogo_intercambio_2.exec()
        aceptado = bool(aceptado)
        self.senal_realizar_intercambio.emit(aceptado)

    def actualizar_materia_prima(self, id_jugador, materia_prima, valor):
        """
        """
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

    def eliminar_construccion(self, id_nodo):
        self.labels_nodos[id_nodo].hide()

    def anadir_construccion(self, id_nodo, pixmap):
        label = self.labels_nodos[id_nodo]
        label.setPixmap(pixmap)
        label.show()

    def actualizar_label_usuario(self, id, usuario):
        if id == "0":
            self.labels_usuarios[id].setText(f"{usuario} (Tú)")
        else:
            self.labels_usuarios[id].setText(usuario)

    def actualizar_label_jugador_actual(self, nombre_jugador):
        self.jugador_actual.setText(nombre_jugador)

    def actualizar_dados(self, pixmap_1, pixmap_2):
        self.labels_dados["1"].setPixmap(pixmap_1)
        self.labels_dados["2"].setPixmap(pixmap_2)

    def lanzar_dados(self):
        self.senal_lanzar_dados.emit()
        self.boton_lanzar_dados.setEnabled(False)

    def pasar_turno(self):
        self.senal_pasar_turno.emit()
        self.deshabilitar_interfaz()

    def comprar_carta_desarrollo(self):
        self.senal_comprar_carta_desarrollo.emit()
        self.deshabilitar_interfaz()

    def activar_interfaz_dados(self, bool):
        self.boton_lanzar_dados.setEnabled(bool)

    def habilitar_interfaz(self):
        self.casa_interfaz.movible = True
        self.boton_carta_desarrollo.setEnabled(True)
        self.boton_pasar_turno.setEnabled(True)
        self.boton_intercambio.setEnabled(True)

    def deshabilitar_interfaz(self):
        self.casa_interfaz.movible = False
        self.ladron.movible = False
        self.boton_carta_desarrollo.setEnabled(False)
        self.boton_pasar_turno.setEnabled(False)
        self.boton_intercambio.setEnabled(False)

    def habilitar_ladron(self):
        self.ladron.movible = True

    def alerta(self, mensaje):
        self.q_error_message = QErrorMessage(self)
        self.q_error_message.showMessage(mensaje)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        label_dropeado = event.source()
        pos_global = label_dropeado.mapToGlobal(QPoint(0, 0))
        pos_global_drop = self.mapToGlobal(event.pos())
        colider_drop = QRect(pos_global_drop, label_dropeado.size())
        if label_dropeado.tipo == "choza":
            for id_nodo in self.labels_nodos:
                label_nodo = self.labels_nodos[id_nodo]
                pos_global_nodo = label_nodo.mapToGlobal(QPoint(0, 0))
                colider_nodo = QRect(pos_global_nodo, label_nodo.size())
                if colider_drop.intersects(colider_nodo):
                    self.senal_casa_dropeada.emit(id_nodo)
                    self.deshabilitar_interfaz()
                    return
            self.alerta("Posicion invalida")
        elif label_dropeado.tipo == "ladron":
            for id_hexagono in self.labels_hexagonos:
                label_hexagono = self.labels_hexagonos[id_hexagono]
                pos_global_hexagono = label_hexagono.mapToGlobal(QPoint(0, 0))
                colider_hexagono = QRect(pos_global_hexagono, label_hexagono.size())
                if colider_drop.intersects(colider_hexagono):
                    self.senal_ladron_dropeado.emit(id_hexagono)
                    self.ladron.movible = False
                    return
            self.alerta("Posicion invalida")

    def habilitar_boton_dados(self):
        self.boton_lanzar_dados.setEnabled(True)

    def poner_ladron(self, id_hexagono):
        label_hexagono = self.labels_hexagonos[id_hexagono]
        self.ladron.setParent(label_hexagono)
        self.ladron.move(20, 20)
        self.ladron.show()
