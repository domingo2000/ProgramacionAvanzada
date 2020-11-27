from juego.items.cartas import Mazo
from juego.mapa.mapa import Mapa
from threading import Thread
import random
import json
import time


with open("parametros.json") as file:
    data = json.load(file)


class Juego():

    def __init__(self, usuarios, net):
        self.net = net
        self.usuarios = usuarios
        self.puntos = {usuario: 0 for usuario in self.usuarios}
        self.mazos = {usuario: Mazo() for usuario in self.usuarios}
        self.mapa = Mapa()
        self.fase_inicio()
        self.__dados = [0, 0]
        self.__jugador_actual = ""
        self.dados_lanzados = False
        self.ganador = None
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

    @property
    def jugador_actual(self):
        return self.__jugador_actual

    @jugador_actual.setter
    def jugador_actual(self, valor):
        self.__jugador_actual = valor
        self.net.send_command_to_all("actualizar_jugador_actual", [valor])

    def fase_inicio(self):
        self.ganador = None
        numeros, materias_primas = self.mapa.datos_mapa()
        random.shuffle(self.usuarios)
        self.net.send_command_to_all("cargar_mapa", [numeros, materias_primas])
        self.net.send_command_to_all("cargar_usuarios")
        self.actualizar_materias_primas()
        self.actualizar_construcciones()
        self.asignar_casas_aleatorias()
        self.repartir_materias_primas_iniciales()

    def fase_juego(self):
        self.net.log("Server", "Iniciando Juego")
        while not self.ganador:
            usuario = self.usuarios.pop()
            self.usuarios.insert(0, usuario)
            self.comenzar_turno(usuario)

    def comenzar_turno(self, usuario):
        self.jugador_actual = usuario
        self.net.send_command("throw_dices", usuario)
        while not self.dados_lanzados:
            pass
        # Reparte las masterias primas
        suma_dados = self.dados[0] + self.dados[1]
        if suma_dados == 7:
            pass
        else:
            self.repartir_materias_primas(suma_dados)

        self.net.send_command("activar_interfaz", usuario, [True])
        self.net.send_command("activar_interfaz", usuario, [False])
        self.dados_lanzados = False

    def actualizar_materias_primas(self):
        dict_materias = {usuario: self.mazos[usuario].cartas for usuario in self.usuarios}
        self.net.send_command_to_all("actualizar_materias_primas", [dict_materias])

    def actualizar_construcciones(self):
        dict_nodo_construccion_usuario = {}
        for id_nodo in self.mapa.nodos:
            nodo = self.mapa.nodos[id_nodo]
            dict_nodo_construccion_usuario[id_nodo] = [nodo.construccion, nodo.usuario_presente]
        self.net.send_command_to_all("actualizar_construcciones", [dict_nodo_construccion_usuario])

    def asignar_casas_aleatorias(self):
        for usuario in self.usuarios:
            for _ in range(2):  # Pone dos casas por usuario
                while True:
                    id_nodo = random.choice(list(self.mapa.nodos))
                    if self.validar_posicion_casa(id_nodo):
                        self.asignar_casa(id_nodo, usuario)
                        break

    def asignar_caminos_aleatorios(self):
        pass

    def asignar_casa(self, id_nodo, usuario):
        nodo = self.mapa.nodos[id_nodo]
        nodo.estado = "ocupado"
        nodo.usuario_presente = usuario
        nodo.construccion = "choza"
        self.actualizar_construcciones()
        self.puntos[usuario] += 1
        self.net.send_command_to_all("actualizar_puntos", [self.puntos])
        return True

    def asignar_construccion(self, id_nodo, usuario):
        pass

    def validar_posicion_casa(self, id_nodo):
        # Revisa el nodo propio
        if self.mapa.nodos[id_nodo].estado == "ocupado":
            return False
        # Revisa los nodos vecinos
        vecinos = self.mapa.vecinos(id_nodo)
        for id_nodo in vecinos:
            if self.mapa.nodos[id_nodo].estado == "ocupado":
                return False
        return True

    def lanzar_dados(self):
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.dados = [dado_1, dado_2]
        self.dados_lanzados = True
        self.net.log("server", "lanzando dados", f"{dado_1}, {dado_2}")

    def repartir_materias_primas_iniciales(self):
        for id_hexagono in self.mapa.hexagonos:
            hexagono = self.mapa.hexagonos[id_hexagono]
            materia_prima = hexagono.materia_prima
            for id_nodo in hexagono.nodos:
                nodo = hexagono.nodos[id_nodo]
                if nodo.estado == "ocupado":
                    usuario = nodo.usuario_presente
                    mazo = self.mazos[usuario]
                    mazo.cartas[materia_prima] += 1
        self.actualizar_materias_primas()

    def repartir_materias_primas(self, suma_dados):
        for id_hexagono in self.mapa.hexagonos:
            hexagono = self.mapa.hexagonos[id_hexagono]
            if hexagono.num_ficha == suma_dados:
                materia_prima = hexagono.materia_prima
                for id_nodo in hexagono.nodos:
                    nodo = hexagono.nodos[id_nodo]
                    if nodo.estado == "ocupado":
                        usuario = nodo.usuario_presente
                        mazo = self.mazos[usuario]
                        mazo.cartas[materia_prima] += 1
        self.actualizar_materias_primas()

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
