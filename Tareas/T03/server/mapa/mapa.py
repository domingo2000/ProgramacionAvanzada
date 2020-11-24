import json
from os import path


class Nodo:

    def __init__(self, id, lista_adyacencia=[]):
        self.id = id
        self.estado = "libre"
        self.usuario_presente = None
        self.vecinos = lista_adyacencia

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


if __name__ == "__main__":
    mapa = Mapa()
    mapa.cargar_mapa()
    print(mapa)
    """
    nodo_0 = Nodo("0", ["1", "4"])
    nodo_1 = Nodo("1", ["5", "0"])
    nodo_5 = Nodo("5", ["1", "10", "6"])
    nodo_10 = Nodo("10", ["9", "5", "15"])
    nodo_9 = Nodo("9", ["10", "14", "4"])
    nodo_4 = Nodo("4", ["0", "9"])

    hex_1 = Hexagono("1", [nodo_0,
                         nodo_1,
                         nodo_10,
                         nodo_4,
                         nodo_5,
                         nodo_9])
    print(hex_1)
    for id_nodo in hex_1.nodos:
        nodo = hex_1.nodos[id_nodo]
        print(nodo)
    """
