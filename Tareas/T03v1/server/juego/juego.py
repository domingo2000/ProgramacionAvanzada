from juego.items.cartas import Mazo
from juego.mapa.mapa import Mapa
from juego.banco import Banco
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
        self.puntos_victoria = {usuario: 0 for usuario in self.usuarios}
        self.mazos = {usuario: Mazo() for usuario in self.usuarios}
        self.mapa = Mapa()
        self.banco = Banco(self.net)
        self.fase_inicio()
        self.__dados = [0, 0]
        self.__jugador_actual = ""
        self.dados_lanzados = False
        self.accion_realizada = False
        self.ganador = None
        self.comandos = {
            "lanzar_dados": self.lanzar_dados,
            "realizar_accion": self.realizar_accion,
            "actualizar_materia_monopolio": self.realizar_monopolio,
            "casa_dropeada": self.revisar_casa_dropeada
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
        while not self.accion_realizada:
            pass
        self.accion_realizada = False
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

    def actualizar_puntos(self):
        self.net.send_command_to_all("actualizar_puntos", [self.puntos])

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
        self.actualizar_puntos()
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
        self.net.log("-", "Parametros", str(parametros))

    def realizar_accion(self, accion, id=None):
        mazo_jugador = self.mazos[self.jugador_actual]
        if accion == "carta_desarrollo":
            carta_desarrollo = self.banco.comprar_desarrollo(mazo_jugador)
            if carta_desarrollo:
                self.comprar(carta_desarrollo)
                accion_valida = True
                if carta_desarrollo.tipo == "victoria":
                    self.agregar_punto_victoria()
                elif carta_desarrollo.tipo == "monopolio":
                    self.net.send_command("realizar_monopolio", self.jugador_actual)
            else:
                mensaje = "No tienes materias primas para comprar esta carta de desarrollo"
                self.net.send_command("error_msg", self.jugador_actual, [mensaje])
                accion_valida = False
        elif accion == "choza":
            accion_valida = self.revisar_casa_dropeada(id)
        elif accion == "ciudad":
            pass
        elif accion == "camino":
            pass
        elif accion == "intercambio":
            pass
        elif accion == "pasar":
            self.accion_realizada = True
            accion_valida = True
        else:
            raise KeyError("La accion pedida no existe")

        if not accion_valida:
            self.net.send_command("activar_interfaz", self.jugador_actual, [True])
        else:
            pass

    def notificar_compra_invalida(self, mensaje):
        self.send_command("pop_up", [f"compra_inválida: {mensaje}"])

    def realizar_monopolio(self, materia_prima):
        self.net.send_command_to_all("error_msg", [f"{self.jugador_actual} ha usado un monopolio"
                                                f"robando {materia_prima}"])
        cantidad_total_materia_prima = 0
        for usuario in self.mazos:
            cantidad_materia_prima = self.mazos[usuario].cartas[materia_prima]
            self.mazos[usuario].cartas[materia_prima] = 0
            cantidad_total_materia_prima += cantidad_materia_prima
        self.mazos[self.jugador_actual].cartas[materia_prima]\
            = cantidad_total_materia_prima
        self.actualizar_materias_primas()
        materia_prima = None

        self.accion_realizada = True

    def agregar_punto_victoria(self):
        self.puntos[self.jugador_actual] += 1
        self.puntos_victoria[self.jugador_actual] += 1
        puntos_victoria = self.puntos_victoria[self.jugador_actual]
        self.actualizar_puntos()
        self.net.send_command("actualizar_punto_victoria", self.jugador_actual, [puntos_victoria])
        self.accion_realizada = True

    def comprar(self, objeto):
        for materia_prima in objeto.costo:
            costo = objeto.costo[materia_prima]
            self.mazos[self.jugador_actual].cartas[materia_prima] -= costo

        self.actualizar_materias_primas()

    def revisar_casa_dropeada(self, id_nodo):
        id_vecinos = self.mapa.vecinos(id_nodo)
        # Revisa el mismo nodo
        nodo = self.mapa.nodos[id_nodo]
        if nodo.estado == "ocupado":
            self.net.send_command("error_msg", self.jugador_actual, ["Posición invalida"])
            return False
        # Revisa los vecinos
        for id_vecino in id_vecinos:
            nodo = self.mapa.nodos[id_vecino]
            if nodo.estado == "ocupado":
                self.net.send_command("error_msg", self.jugador_actual, ["Posición invalida"])
                return False
        # Caso si se puede poner la casa
        choza = self.banco.comprar_choza(self.mazos[self.jugador_actual])
        if choza:
            self.comprar(choza)
            self.net.send_command("activar_interfaz", self.jugador_actual, [False])
            self.asignar_casa(id_nodo, self.jugador_actual)
            self.accion_realizada = True
            return True
        else:
            self.net.send_command("error_msg", self.jugador_actual, [
                "no tienes suficientes materias primas"])
            return False
