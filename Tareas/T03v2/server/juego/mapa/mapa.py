from os import path
import json
import random
from networking import interfaz_network

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    RUTAS = PARAMETROS["rutas"]


class Conexion:

    def __init__(self, id_nodo_1, id_nodo_2):
        self.id_nodo_1 = id_nodo_1
        self.id_nodo_2 = id_nodo_2
        self.__camino = False
        self.usuario = None
        self.init_conexion()

    @property
    def camino(self):
        return self.__camino

    @camino.setter
    def camino(self, valor):
        self.__camino = valor
        self.usuario = valor.usuario
        print(f"Enviar Comando Camino: {[self.id_nodo_1, self.id_nodo_2]}, {self.usuario.nombre}")

    def init_conexion(self):
        print(f"Enviar comando eliminar camino id_1: {self.id_nodo_1}, id_2: {self.id_nodo_2}")

    def __repr__(self):
        return (f"Conexion: [{self.id_nodo_1}, {self.id_nodo_2}]")


class Nodo:

    def __init__(self, id, conexiones=[], lista_adyacencia=[]):
        self.id = id
        self.ocupado = False
        self.usuario = None
        self.__construccion = None
        self.vecinos = lista_adyacencia
        self.conexiones = conexiones
        self.init_nodo()

    @property
    def construccion(self):
        return self.__construccion

    @construccion.setter
    def construccion(self, valor):
        if valor is not None:
            self.__construccion = valor
            puntos = valor.puntos
            self.usuario.puntos += puntos
            interfaz_network.send_command_to_all("add_building",
                                                 self.id,
                                                 self.construccion.nombre,
                                                 self.usuario.nombre)
        else:
            self.usuario.puntos -= self.construccion.puntos
            print(f"Enviar comando eliminar construccion, id: {self.id}")
            self.__construccion = valor

    def anadir_construccion(self, construccion, usuario):
        self.usuario = usuario
        self.construccion = construccion

    def eliminar_construccion(self):
        self.construccion = None
        self.usuario = None

    def init_nodo(self):
        interfaz_network.send_command_to_all("del_construccion", self.id)

    def __repr__(self):
        nodos_conectados = set()
        for conexion in self.conexiones:
            if conexion.id_nodo_1 == self.id:
                nodos_conectados.add(conexion.id_nodo_2)
            else:
                nodos_conectados.add(conexion.id_nodo_1)
        return f"nodo_{self.id}: -> {nodos_conectados}"


class Hexagono:

    def __init__(self, id, nodos={}):
        self.id = id
        self.nodos = nodos
        self.__materia_prima = None
        self.__num_ficha = 0

    @property
    def materia_prima(self):
        return self.__materia_prima

    @materia_prima.setter
    def materia_prima(self, valor):
        self.__materia_prima = valor
        interfaz_network.send_command_to_all("load_hexagon_resource", self.id, self.materia_prima)

    @property
    def num_ficha(self):
        return self.__num_ficha

    @num_ficha.setter
    def num_ficha(self, valor):
        self.__num_ficha = valor
        interfaz_network.send_command_to_all("load_num_ficha", self.id, self.num_ficha)

    def anadir_nodo(self, nodo):
        self.nodos[nodo.id] = nodo

    def __repr__(self):
        return f"Hexagono: id-{self.id}, ficha-{self.num_ficha}: {self.materia_prima}"


class Mapa:
    """
    Clase que representa al mapa, esta es un grafo no dirigido
    que contiene tanto los hexagonos como los nodos y esta implementado
    con lista de adyacencia. Este implementa funciones
    de grafos y recorrido
    """

    def __init__(self):
        self.dimensiones = []
        self.nodos = {}
        self.hexagonos = {}
        self.conexiones = {}

    def adyacentes(self, id_nodo_1, id_nodo_2):
        """
        Verifica si dos nodos son adyacentes y retorna un bool
        """
        nodo_1 = self.nodos[id_nodo_1]
        if id_nodo_2 in nodo_1.vecinos:
            return True
        else:
            return False

    def vecinos(self, id_nodo):
        """
        Retorna los id de los vecinos del nodo correspondiente a id_nodo
        ejemplo: vecinos(10) -> [5, 9, 15]
        """
        nodo = self.nodos[id_nodo]
        return nodo.vecinos

    def agregar_nodo(self, nodo):
        id_nodo = nodo.id
        self.nodos[id_nodo] = nodo

    def agregar_hexagono(self, hexagono):
        id_hexagono = hexagono.id
        self.hexagonos[id_hexagono] = hexagono

    def agregar_conexion(self, conexion):
        tupla = (conexion.id_nodo_1, conexion.id_nodo_2)
        self.conexiones[tupla] = conexion

    def cargar_mapa(self):
        """
        Carga el mapa desde el archivo json
        """
        ruta_grafo = path.join(*RUTAS["grafo"])
        with open(ruta_grafo) as file:
            data_grafo = json.load(file)

        # Setea las dimensiones
        self.dimensiones = data_grafo["dimensiones_mapa"]

        # Instancia y agrega todos los nodos
        data_nodos = data_grafo["nodos"]
        for id_nodo in data_nodos:
            lista_adyacencia = data_nodos[id_nodo]
            conexiones = []
            for id_nodo_conectado in lista_adyacencia:
                conexion = Conexion(id_nodo, id_nodo_conectado)
                self.agregar_conexion(conexion)
                conexiones.append(conexion)
            nodo = Nodo(id_nodo, conexiones=conexiones, lista_adyacencia=lista_adyacencia)
            self.agregar_nodo(nodo)

        # Instancia y agrega todos los hexagonos
        data_hexagonos = data_grafo["hexagonos"]
        for id_hexagono in data_hexagonos:
            id_nodos = data_hexagonos[id_hexagono]
            hexagono = Hexagono(id_hexagono)

            # Agrega todos los nodos correspondientes al hexagono
            for id_nodo in id_nodos:
                nodo = self.nodos[id_nodo]
                hexagono.anadir_nodo(nodo)
            self.agregar_hexagono(hexagono)

        # Agrega los numeros a cada hexagono
        self.cargar_numeros()
        # Carga las materias primas
        self.cargar_materias_primas()

    def cargar_numeros(self):
        numeros = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        random.shuffle(numeros)
        for id_hexagono in self.hexagonos:
            hexagono = self.hexagonos[id_hexagono]
            hexagono.num_ficha = numeros.pop()

    def cargar_materias_primas(self):
        materias_primas = ["madera", "trigo", "arcilla"]
        materias_escogidas = []
        for i in range(3):  # primeras 9 materias primas
            materias_escogidas.append("madera")
            materias_escogidas.append("trigo")
            materias_escogidas.append("arcilla")
        # Decima materia prima
        materias_escogidas.append(random.choice(materias_primas))
        # Se revuelven las materias primas
        random.shuffle(materias_escogidas)
        # Se asignan a cada hexagono
        for id_hexagono in self.hexagonos:
            hexagono = self.hexagonos[id_hexagono]
            hexagono.materia_prima = materias_escogidas.pop()

    def anadir_construccion(self, construccion, id_nodo, inicial=False):
        nodo = self.nodos[id_nodo]
        # Revisa que el mismo nodo no este construido
        if nodo.construccion is not None:
            if not inicial:
                print("Enviar comando posicion invalida")
            return False
        # Revisa que no hayan vecinos construidos
        for id_nodo_vecino in nodo.vecinos:
            nodo_vecino = self.nodos[id_nodo_vecino]
            if nodo_vecino.construccion is not None:
                if not inicial:
                    print("Enviar comando posicion invalida")
                return False
        nodo.anadir_construccion(construccion, construccion.usuario)
        return True


if __name__ == "__main__":
    mapa = Mapa()
    mapa.cargar_mapa()
    print(mapa)
