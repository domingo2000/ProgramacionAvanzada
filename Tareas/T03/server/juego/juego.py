from juego.items.cartas import Mazo
from juego.mapa.mapa import Mapa
from threading import Thread
import random


class Juego():

    def __init__(self, usuarios, net):
        self.net = net
        self.usuarios = usuarios
        self.puntos = {usuario: 0 for usuario in self.usuarios}
        self.mazos = {usuario: Mazo() for usuario in self.usuarios}
        self.mapa = Mapa()
        self.__dados = [0, 0]
        self.iniciar_juego()
        self.comandos = {
            "lanzar_dados": self.lanzar_dados
        }
        self.thread_revisar_comandos = Thread(target=self.thread_revisar_comandos,
                                              daemon=True)
        self.thread_revisar_comandos.start()

    @property
    def dados(self):
        return self.__dados

    @dados.setter
    def dados(self, valor):
        self.__dados = valor
        dado_1 = valor[0]
        dado_2 = valor[1]
        self.net.send_command_to_all("actualizar_dados", [dado_1, dado_2])

    def iniciar_juego(self):
        numeros, materias_primas = self.mapa.datos_mapa()
        self.net.send_command_to_all("cargar_mapa", [numeros, materias_primas])
        self.net.send_command_to_all("cargar_usuarios")
        self.actualizar_materias_primas()

    def actualizar_materias_primas(self):
        dict_materias = {usuario: self.mazos[usuario].cartas for usuario in self.usuarios}
        self.net.send_command_to_all("actualizar_materias_primas", [dict_materias])

    def actualizar_construcciones(self):
        self.net.send_command_to_all("actualizar_construcciones")

    def asignar_casas_aleatorias(self):
        pass

    def asignar_caminos_aleatorios(self):
        pass

    def asignar_casa(self, id_nodo, usuario):
        self.mapa.nodos[id_nodo].estado = "ocupado"
        self.mapa.nodos[id_nodo].usuario = usuario

        return True

    def validar_posicion_casa(self, id_nodo):
        vecinos = self.mapa.vecinos(id_nodo)
        for id_nodo in vecinos:
            if self.mapa.nodos[id_nodo].estado == "ocupado":
                return False
        return True

    def lanzar_dados(self):
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.dados = [dado_1, dado_2]
        self.net.log("server", "lanzando dados", f"{dado_1}, {dado_2}")

    def thread_revisar_comandos(self):
        while True:
            try:
                if not self.net.comando_realizado:
                    index_ultimo_comando = len(self.net.stack_comandos) - 1
                    comando = self.net.stack_comandos[index_ultimo_comando]
                    nombre_comando = comando[0]
                    if nombre_comando in self.comandos:
                        comando = self.net.stack_comandos.pop(index_ultimo_comando)
                        self.realizar_comando(comando)
            except IndexError:
                print("Solicitud acoplada")
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
