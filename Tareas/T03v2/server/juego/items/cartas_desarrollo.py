import json
from funciones import generar_dict_costos
from os import path
from networking import interfaz_network

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    COSTOS = PARAMETROS["costos"]
    COSTO_DESARROLLO = COSTOS["carta_desarrollo"]
    RUTAS_SPRITES = PARAMETROS["rutas_sprites"]
    RUTA_CARTA_DESARROLLO = RUTAS_SPRITES["carta_desarrollo"]


class CartaDesarrollo:
    costo = generar_dict_costos(COSTO_DESARROLLO)

    def __init__(self, tipo, ruta_label_relativa):
        self.tipo = None
        ruta_label = RUTA_CARTA_DESARROLLO.copy()
        ruta_label.append(ruta_label_relativa)
        self.ruta_label = ruta_label


class CartaPuntoVictoria(CartaDesarrollo):
    puntos = 1

    def __init__(self, ruta_label_relativa):
        super().__init__("punto_victoria", ruta_label_relativa)

    def activar(self, usuario):
        usuario.puntos_victoria += self.puntos
        usuario.puntos += self.puntos
        print("ACTIVANDO PUNTO VICTORIA")
        # Completar activar punto victoria ##
        interfaz_network.send_command(usuario.nombre, "open_victory_dialog", self.ruta_label)


class CartaMonopolio(CartaDesarrollo):

    def __init__(self, ruta_label_relativa):
        super().__init__("monopolio", ruta_label_relativa)

    def activar(self, usuario):
        print("ACTIVANDO MONOPOLIO")
        ## Completar activar carta monopolio ##
