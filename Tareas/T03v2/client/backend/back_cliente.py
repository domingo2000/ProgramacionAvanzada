from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from backend.networking import interfaz_network, revisar_comando
from os import path
import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS_SPRITES = PARAMETROS["rutas_sprites"]


class BackCliente(QObject):
    senal_cerrar_sala_espera = pyqtSignal()
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_abrir_sala_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()
    senal_abrir_dialogo_punto_victoria = pyqtSignal(list)
    senal_abrir_dialogo_monopolio = pyqtSignal(list)
    senal_anadir_usuario = pyqtSignal(str)
    senal_actualizar_usuarios = pyqtSignal(list)
    senal_cargar_hexagono = pyqtSignal(str, str)
    senal_cargar_num_ficha = pyqtSignal(str, int)
    senal_cargar_nombre_usuario = pyqtSignal(str, str)
    senal_actualizar_materia_prima = pyqtSignal(str, str, int)
    senal_actualizar_puntos_usuario = pyqtSignal(str, int)
    senal_actualizar_puntos_victoria_usuario = pyqtSignal(int)
    senal_actualizar_jugador_actual = pyqtSignal(str)
    senal_eliminar_construccion = pyqtSignal(str)
    senal_anadir_construccion = pyqtSignal(str, QPixmap)
    senal_mensaje_sala_espera = pyqtSignal(str)
    senal_habilitar_dados = pyqtSignal()
    senal_habilitar_interfaz = pyqtSignal()
    senal_actualizar_dados = pyqtSignal(QPixmap, QPixmap)
    senal_alerta = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.usuario_propio = str
        self.usuarios = {}
        self.comandos = {
            "close_wait_window": self.senal_cerrar_sala_espera.emit,
            "close_game_window": self.senal_cerrar_ventana_juego.emit,
            "open_wait_window": self.senal_abrir_sala_espera.emit,
            "open_game_window": self.senal_abrir_ventana_juego.emit,
            "open_victory_dialog": self.senal_abrir_dialogo_punto_victoria.emit,
            "open_monopoly_dialog": self.senal_abrir_dialogo_monopolio.emit,
            "add_user": self.anadir_usuario,
            "update_users": self.actualizar_usuarios,
            "update_resource": self.actualizar_materia_prima,
            "update_points": self.actualizar_puntos_usuario,
            "update_current_player": self.senal_actualizar_jugador_actual.emit,
            "update_dices": self.actualizar_dados,
            "update_victory_points": self.actualizar_puntos_victoria_usuario,
            "set_user": self.set_usuario,
            "load_hexagon_resource": self.senal_cargar_hexagono.emit,
            "load_num_ficha": self.senal_cargar_num_ficha.emit,
            "load_user_name": self.cargar_nombre_usuario,
            "del_construccion": self.senal_eliminar_construccion.emit,
            "add_building": self.anadir_construccion,
            "msg_wait_room": self.senal_mensaje_sala_espera.emit,
            "enable_dice_throw": self.senal_habilitar_dados.emit,
            "enable_interface": self.senal_habilitar_interfaz.emit,

            "pop_up": self.senal_alerta.emit
        }

        self.thread_comandos = QTimer()
        self.thread_comandos.setInterval(0)
        self.thread_comandos.timeout.connect(self.revisar_comandos)
        self.thread_comandos.start()

    def anadir_usuario(self, nombre_usuario):
        self.senal_anadir_usuario.emit(nombre_usuario)

    def actualizar_usuarios(self, nombres_usuarios):
        id = 1
        for nombre_usuario in nombres_usuarios:
            if nombre_usuario == self.usuario_propio:
                self.usuarios[nombre_usuario] = "0"
            else:
                self.usuarios[nombre_usuario] = str(id)
                id += 1

        self.senal_actualizar_usuarios.emit(nombres_usuarios)

    def revisar_comandos(self):
        revisar_comando(self.comandos)

    def set_usuario(self, nombre_usuario):
        self.usuario_propio = nombre_usuario

    def do_none(self, *args):
        pass

    def actualizar_materia_prima(self, nombre_usuario, materia_prima, valor):
        id_usuario = self.usuarios[nombre_usuario]
        self.senal_actualizar_materia_prima.emit(id_usuario, materia_prima, valor)

    def actualizar_puntos_usuario(self, nombre_usuario, puntos):
        id_usuario = self.usuarios[nombre_usuario]
        self.senal_actualizar_puntos_usuario.emit(id_usuario, puntos)

    def actualizar_puntos_victoria_usuario(self, puntos):
        self.senal_actualizar_puntos_victoria_usuario.emit(puntos)

    def actualizar_dados(self, dado_1, dado_2):
        ruta_dado_1 = path.join(*RUTAS_SPRITES[f"dado_{dado_1}"])
        ruta_dado_2 = path.join(*RUTAS_SPRITES[f"dado_{dado_2}"])
        pixmap_1 = QPixmap(ruta_dado_1)
        pixmap_2 = QPixmap(ruta_dado_2)
        self.senal_actualizar_dados.emit(pixmap_1, pixmap_2)

    def cargar_nombre_usuario(self, nombre_usuario):
        id_usuario = self.usuarios[nombre_usuario]
        self.senal_cargar_nombre_usuario.emit(id_usuario, nombre_usuario)

    def lanzar_dados(self):
        interfaz_network.send_command("throw_dices")

    def comprar_carta_desarrollo(self):
        interfaz_network.send_command("buy_development_card")

    def activar_carta_desarrollo(self, materia_prima):
        interfaz_network.send_command("activate_development_card", materia_prima)

    def pasar_turno(self):
        interfaz_network.send_command("pass_turn")



    def anadir_construccion(self, id_nodo, nombre_construccion, nombre_usuario):
        id_usuario = self.usuarios[nombre_usuario]
        ruta_pixmap = path.join(*RUTAS_SPRITES[f"{nombre_construccion}_j{id_usuario}"])
        pixmap = QPixmap(ruta_pixmap)
        self.senal_anadir_construccion.emit(id_nodo, pixmap)