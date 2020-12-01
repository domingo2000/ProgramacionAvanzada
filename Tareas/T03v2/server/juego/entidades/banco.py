from juego.items.construcciones import Choza, Ciudad
from juego.entidades.generador_de_cartas import sacar_cartas
from juego.items.cartas_desarrollo import CartaDesarrollo, CartaPuntoVictoria, CartaMonopolio
from networking import interfaz_network
import json
from os import path

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    COSTOS = PARAMETROS["costos"]


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
                    usuario.mazo[materia_prima] += cartas_entregadas

    def comprar_carta_desarrollo(self, usuario):
        costo_carta = CartaDesarrollo.costo
        if self.compra_valida(costo_carta, usuario):
            tupla_carta_desarrollo = sacar_cartas(1).pop()
            tipo_carta = tupla_carta_desarrollo[0]
            ruta_label = "_".join(tupla_carta_desarrollo)
            ruta_label += ".png"
            if tipo_carta == "victoria":
                carta_desarrollo = CartaPuntoVictoria(ruta_label)
            elif tipo_carta == "monopolio":
                carta_desarrollo = CartaMonopolio(ruta_label)
            return carta_desarrollo

    def compra_valida(self, dict_costo, usuario):
        mazo_jugador = usuario.mazo
        for materia_prima in dict_costo:
            cantidad_necesaria = dict_costo[materia_prima]
            cantidad_mazo = mazo_jugador[materia_prima]
            if cantidad_mazo < cantidad_necesaria:
                # Enviar comando compra invalida
                interfaz_network.send_command(usuario.nombre, "pop_up",
                                              "No tienes las materias primas suficientes")
                return False
        self.realizar_compra(dict_costo, usuario)
        return True

    def realizar_compra(self, dict_costo, usuario):
        mazo = usuario.mazo
        for materia_prima in dict_costo:
            cantidad_necesaria = dict_costo[materia_prima]
            mazo[materia_prima] -= cantidad_necesaria

    def comprar_choza(self, usuario):
        costo_choza = Choza.costo
        if self.compra_valida(costo_choza, usuario):
            choza = Choza(usuario)
            return choza
