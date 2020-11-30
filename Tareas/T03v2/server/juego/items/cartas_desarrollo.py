import json
from funciones import generar_dict_costos

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    COSTOS = PARAMETROS["costos"]
    COSTO_DESARROLLO = COSTOS["carta desarrollo"]
    RUTAS_SPRITES = PARAMETROS["rutas_sprites"]
    RUTA_CARTA_DESARROLLO = RUTAS_SPRITES["carta_desarrollo"]


class CartaDesarrollo:
    costo = generar_dict_costos(COSTO_DESARROLLO)

    def __init__(self, tipo, ruta_label_relativa):
        self.tipo = None
        lista_ruta = RUTA_CARTA_DESARROLLO.extend(ruta_label_relativa)
        self.ruta_label = path.join(*lista_ruta)


class CartaPuntoVictoria(CartaDesarrollo):
    puntos = 1

    def __init__(self, ruta_label_relativa):
        super().__init__("punto_victoria", ruta_label_relativa)

    def activar(self, usuario):
        self.usuario.puntos_victoria += self.puntos
        self.usuario.puntos += self.puntos
        print("ACTIVANDO PUNTO VICTORIA")
        # Completar activar punto victoria ##


class CartaMonopolio(CartaDesarrollo):

    def __init__(self, ruta_label_relativa):
        super().__init__("monopolio", ruta_label_relativa)

    def activar(self, usuario):
        print("ACTIVANDO MONOPOLIO")
        ## Completar activar carta monopolio ##
