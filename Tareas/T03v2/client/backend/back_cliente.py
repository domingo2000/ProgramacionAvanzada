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
    senal_anadir_usuario = pyqtSignal(str)
    senal_actualizar_usuarios = pyqtSignal(list)
    senal_cargar_hexagono = pyqtSignal(str, str)
    senal_cargar_num_ficha = pyqtSignal(str, int)
    senal_cargar_nombre_usuario = pyqtSignal(str, str)
    senal_actualizar_materia_prima = pyqtSignal(str, str, int)
    senal_actualizar_puntos_usuario = pyqtSignal(str, int)
    senal_eliminar_construccion = pyqtSignal(str)
    senal_anadir_construccion = pyqtSignal(str, QPixmap)

    def __init__(self):
        super().__init__()
        self.usuario_propio = str
        self.usuarios = {}
        self.comandos = {
            "close_wait_window": self.senal_cerrar_sala_espera.emit,
            "close_game_window": self.senal_cerrar_ventana_juego.emit,
            "open_wait_window": self.senal_abrir_sala_espera.emit,
            "open_game_window": self.senal_abrir_ventana_juego.emit,
            "add_user": self.anadir_usuario,
            "update_users": self.actualizar_usuarios,
            "set_user": self.set_usuario,
            "load_hexagon_resource": self.senal_cargar_hexagono.emit,
            "load_num_ficha": self.senal_cargar_num_ficha.emit,
            "update_resource": self.actualizar_materia_prima,
            "update_points": self.actualizar_puntos_usuario,
            "load_user_name": self.cargar_nombre_usuario,
            "del_construccion": self.senal_eliminar_construccion.emit,
            "add_building": self.anadir_construccion
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

    def cargar_nombre_usuario(self, nombre_usuario):
        id_usuario = self.usuarios[nombre_usuario]
        self.senal_cargar_nombre_usuario.emit(id_usuario, nombre_usuario)

    def anadir_construccion(self, id_nodo, nombre_construccion, nombre_usuario):
        id_usuario = self.usuarios[nombre_usuario]
        ruta_pixmap = path.join(*RUTAS_SPRITES[f"{nombre_construccion}_j{id_usuario}"])
        pixmap = QPixmap(ruta_pixmap)
        self.senal_anadir_construccion.emit(id_nodo, pixmap)