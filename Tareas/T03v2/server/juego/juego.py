from juego.entidades.usuario import Usuario
from juego.entidades.banco import Banco
from juego.items.construcciones import Choza, Ciudad
from juego.mapa.mapa import Mapa
from collections import deque
import random
import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)


class Juego:

    def __init__(self, nombres_usuarios):
        self.usuarios = [Usuario(nombre_usuario) for nombre_usuario in nombres_usuarios]
        self.cola_turnos = deque()
        for usuario in self.usuarios:
            self.cola_turnos.append(usuario)
        self.dados = [int, int]
        self.banco = Banco()
        self.suma_dados = int
        self.mapa = Mapa()
        self.fase_inicio()

    def fase_inicio(self):
        random.shuffle(self.cola_turnos)
        self.mapa.cargar_mapa()
        self.construir_construcciones_iniciales()
        self.banco.repartir_cartas(self.mapa)

    def construir_construcciones_iniciales(self):
        lista_nodos = list(self.mapa.nodos.keys())
        for usuario in self.usuarios:
            for _ in range(PARAMETROS["CANTIDAD_CHOZAS_INICIALES"]):
                choza = Choza(usuario)
                while True:
                    id_nodo = random.choice(lista_nodos)
                    if self.mapa.anadir_construccion(choza, id_nodo, inicial=True):
                        break
        #  Construye las primeras casas
