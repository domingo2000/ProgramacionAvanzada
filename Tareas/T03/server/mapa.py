
class Nodo:

    def __init__(self, id, lista_adyacencia=[]):
        self.id = id
        self.estado = "libre"
        self.usuario_presente = None
        self.vecinos = lista_adyacencia


class Hexagono:

    def __init__(self, id, nodos):
        self.id = id
        self.nodos = nodos
        self.num_ficha = 0
        self.materia_prima = ""


class Mapa:
    """
    Clase que representa al mapa, esta es un grafo no dirigido
    que contiene tanto los hexagonos como los nodos y esta implementado
    con lista de adyacencia. Este implementa funciones
    de grafos y recorrido
    """
    def __init__(self):
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
        self.hexagonos[id] = hexagono
