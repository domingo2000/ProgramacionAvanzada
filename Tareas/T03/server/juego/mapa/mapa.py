import json
from os import path
from juego.mapa.generador_grilla import GeneradorGrillaHexagonal
import random


class Nodo:

    def __init__(self, id, lista_adyacencia=[]):
        self.id = id
        self.estado = "libre"
        self.usuario_presente = None
        self.vecinos = lista_adyacencia
        self.posicion = None
        self.construccion = None

    def __repr__(self):
        return f"nodo_{self.id}: -> {self.vecinos}"


class Hexagono:

    def __init__(self, id, nodos={}):
        self.id = id

        self.nodos = {nodo.id: nodo for nodo in nodos}
        self.num_ficha = 0
        self.materia_prima = ""

    def añadir_nodo(self, nodo):
        self.nodos[nodo.id] = nodo

    def __repr__(self):
        return f"hex_{self.id}: num_{self.num_ficha}, {self.materia_prima}"


class Mapa:
    """
    Clase que representa al mapa, esta es un grafo no dirigido
    que contiene tanto los hexagonos como los nodos y esta implementado
    con lista de adyacencia. Este implementa funciones
    de grafos y recorrido
    """
    def __init__(self):
        self.dimensiones = [0, 0]
        self.nodos = {}
        self.hexagonos = {}
        self.cargar_mapa()

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

    def cargar_mapa(self):
        """
        Carga el mapa desde el archivo json
        """
        with open("parametros.json") as file:
            parametros = json.load(file)
            rutas = parametros["rutas"]
            ruta_grafo = path.join(*rutas["grafo"])
        with open(ruta_grafo) as file:
            data_grafo = json.load(file)

        # Setea las dimensiones
        self.dimensiones = data_grafo["dimensiones_mapa"]

        # Instancia y agrega todos los nodos
        data_nodos = data_grafo["nodos"]
        for id_nodo in data_nodos:
            lista_adyacencia = data_nodos[id_nodo]
            nodo = Nodo(id_nodo, lista_adyacencia)
            self.agregar_nodo(nodo)

        # Instancia y agrega todos los hexagonos
        data_hexagonos = data_grafo["hexagonos"]
        for id_hexagono in data_hexagonos:
            id_nodos = data_hexagonos[id_hexagono]
            hexagono = Hexagono(id_hexagono)

            # Agrega todos los nodos correspondientes al hexagono
            for id_nodo in id_nodos:
                nodo = self.nodos[id_nodo]
                hexagono.añadir_nodo(nodo)
            self.agregar_hexagono(hexagono)

        # Agrega los numeros a cada hexagono
        self.cargar_numeros()
        # Carga las materias primas
        self.cargar_materias_primas()
        # Carga las posiciones de cada nodo en la grilla
        generador_grilla = GeneradorGrillaHexagonal(56)
        posiciones = generador_grilla.generar_grilla(self.dimensiones, 70, 30)
        for id_nodo in posiciones:
            self.nodos[id_nodo].posicion = posiciones[id_nodo]
        print(self.nodos)

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

    def datos_mapa(self):
        numeros = []
        materias_primas = []
        for id_hexagono in self.hexagonos:
            hexagono = self.hexagonos[id_hexagono]
            num_ficha = hexagono.num_ficha
            materia_prima = hexagono.materia_prima
            numeros.append(num_ficha)
            materias_primas.append(materia_prima)
        return numeros, materias_primas


if __name__ == "__main__":
    mapa = Mapa()
    mapa.cargar_mapa()
    print(mapa)
