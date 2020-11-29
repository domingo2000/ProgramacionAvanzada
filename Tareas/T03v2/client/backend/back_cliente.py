from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from backend.networking import interfaz_network, revisar_comando
from os import path
import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)


class BackCliente(QObject):
    senal_cerrar_sala_espera = pyqtSignal()
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_abrir_sala_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()
    senal_anadir_usuario = pyqtSignal(str)
    senal_actualizar_usuarios = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.usuario_propio = str
        self.comandos = {
            "close_wait_window": self.senal_cerrar_sala_espera.emit,
            "close_game_window": self.senal_cerrar_ventana_juego.emit,
            "open_wait_window": self.senal_abrir_sala_espera.emit,
            "open_game_window": self.senal_abrir_ventana_juego.emit,
            "add_user": self.anadir_usuario,
            "update_users": self.actualizar_usuarios,
            "set_user": self.set_usuario
        }
        self.thread_comandos = QTimer()
        self.thread_comandos.setInterval(0)
        self.thread_comandos.timeout.connect(self.revisar_comandos)
        self.thread_comandos.start()

    def anadir_usuario(self, nombre_usuario):
        self.senal_anadir_usuario.emit(nombre_usuario)

    def actualizar_usuarios(self, nombres_usuarios):
        self.senal_actualizar_usuarios.emit(nombres_usuarios)

    def revisar_comandos(self):
        revisar_comando(self.comandos)

    def set_usuario(self, nombre_usuario):
        self.usuario_propio = nombre_usuario
