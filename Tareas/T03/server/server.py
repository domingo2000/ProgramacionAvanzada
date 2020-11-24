from PyQt5.QtCore import pyqtSignal, QObject
from networking import ServerNet
from banco import Banco
from mapa.mapa import Mapa


class Server():
    senal_enviar_comando = pyqtSignal(str, tuple, str)
    senal_enviar_log = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.net = ServerNet()
        self.banco = Banco()
        self.mapa = Mapa()

        self.comandos_servidor = {
            "comprar_choza": self.banco.comprar_choza,
            "comprar_carretera": self.banco.comprar_carretera,
            "comprar_desarrollo": self.banco.comprar_desarrollo
        }

    def iniciar_partida(self):
        self.mapa.cargar_mapa()
