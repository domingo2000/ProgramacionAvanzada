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
        self.tipo = tipo
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
        msg = f"{usuario.nombre} ha ganado un punto de victoria"
        interfaz_network.send_command_to_all("pop_up", msg)


class CartaMonopolio(CartaDesarrollo):

    def __init__(self, ruta_label_relativa):
        super().__init__("monopolio", ruta_label_relativa)

    def activar(self, usuario_monopolio, materia_prima, usuarios):
        msg = f"{usuario_monopolio.nombre} ha usado un monopolio robando {materia_prima}"
        interfaz_network.send_command_to_all("pop_up", msg)
        mazo_usuario_monopolio = usuario_monopolio.mazo
        for usuario in usuarios:
            if usuario == usuario_monopolio:
                pass
            else:
                mazo_usuario = usuario.mazo
                # Le quita las materias primas al contrincante
                cantidad_cartas_materia_prima = mazo_usuario[materia_prima]
                mazo_usuario[materia_prima] = 0
                # Se las agrega al jugador
                mazo_usuario_monopolio[materia_prima] += cantidad_cartas_materia_prima
