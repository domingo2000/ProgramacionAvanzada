from banco import Banco
from mapa.mapa import Mapa
from networking import ServerNet
from threading import Thread
import time


class Server():

    def __init__(self, host, port):
        print("Inicializando Servidor")
        super().__init__()
        self.net = ServerNet(host, port)
        # Atributos del juego
        self.usuarios = []
        self.banco = Banco()
        self.mapa = Mapa()

        self.comandos = {
            "comprar_choza": self.banco.comprar_choza,
            "comprar_carretera": self.banco.comprar_carretera,
            "comprar_desarrollo": self.banco.comprar_desarrollo,
            "test": self.test
        }
        thread_revisar_comandos = Thread(target=self.thread_revisar_comandos,
                                         daemon=True)
        thread_revisar_comandos.start()
        #self.start()

    def start(self):
        while not self.net.lleno():
            pass

    def thread_revisar_comandos(self):
        while True:
            if not self.net.comando_realizado:
                index_ultimo_comando = len(self.net.stack_comandos) - 1
                comando = self.net.stack_comandos[index_ultimo_comando]
                nombre_comando = comando[0]
                if nombre_comando in self.comandos:
                    comando = self.net.stack_comandos.pop(index_ultimo_comando)
                    self.realizar_comando(comando)

            else:
                pass

    def realizar_comando(self, comando):
        self.net.comando_realizado = True
        nombre_comando = comando[0]
        parametros = comando[1]
        metodo = self.comandos[nombre_comando]
        if parametros:
            metodo(*parametros)
        else:
            metodo()

        self.net.log("Server", "Realizado Comando", nombre_comando)
    #  METODOS DEL JUEGO ###

    def iniciar_partida(self):
        self.mapa.cargar_mapa()
        self.send_command_to_all("close_window_wait")
        self.send_command_to_all("open_window_game")
        self.send_command_to_all("cargar_mapa")

    def test(self):
        self.net.log("Server", "Test", "None")


if __name__ == "__main__":
    import json
    with open("parametros.json") as file:
        data = json.load(file)
    server = Server(data["host"], data["port"])
    while True:
        comando = input("Ingrese el nombre del comando: ")
        parametros = []
        entrada = input("Ingrese un string para parametro: ")
        parametros.append(entrada)
        server.net.send_command_to_all(comando)
