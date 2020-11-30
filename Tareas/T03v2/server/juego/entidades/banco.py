from juego.items.construcciones import Choza, Ciudad


class Banco:

    def __init__(self):
        pass

    def repartir_cartas_iniciales(self, mapa):
        for hexagono in mapa.hexagonos.values():
            materia_prima = hexagono.materia_prima
            nodos_ocupados = hexagono.nodos_ocupados()
            for nodo in nodos_ocupados:
                cartas_entregadas = nodo.construccion.cartas_entregadas
                usuario = nodo.usuario
                usuario.mazo[materia_prima] += cartas_entregadas

    def repartir_cartas(self, mapa, suma_dados):
        for hexagono in mapa.hexagonos.values():
            if hexagono.num_ficha == suma_dados:
                materia_prima = hexagono.materia_prima
                nodos_ocupados = hexagono.nodos_ocupados()
                for nodo in nodos_ocupados:
                    cartas_entregadas = nodo.construccion.cartas_entregadas
                    usuario = nodo.usuario
                    usuaro.mazo[materia_prima] += cartas_entregadas
