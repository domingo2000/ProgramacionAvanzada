from juego.items.cartas import CartaPuntoVictoria, CartaMonopolio
from juego.items.construcciones import Choza
import random


class Banco:

    def __init__(self, net):
        self.net = net
        self.cartas_desarrollo = [CartaPuntoVictoria(1), CartaMonopolio()]
        self.choza = Choza()

    def comprar_choza(self, mazo_jugador):
        if self.validar_compra(self.choza.costo, mazo_jugador):
            return self.choza
        else:
            return None

    def comprar_carretera(self):
        pass

    def comprar_desarrollo(self, mazo_jugador):
        carta_desarrollo = random.choice(self.cartas_desarrollo)
        if self.validar_compra(carta_desarrollo.costo, mazo_jugador):
            return carta_desarrollo
        else:
            return None

    def validar_compra(self, costo_compra, mazo_jugador):
        cartas = mazo_jugador.cartas
        for materia_prima in cartas:
            if cartas[materia_prima] < costo_compra[materia_prima]:
                return False
        return True
