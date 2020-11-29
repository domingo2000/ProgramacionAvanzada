from juego.entidades.usuario import Usuario
from juego.mapa.mapa import Mapa
from collections import deque
import random


class Juego:

    def __init__(self, nombres_usuarios):
        self.usuarios = [Usuario(nombre_usuario) for nombre_usuario in nombres_usuarios]
        self.cola_turnos = deque()
        for usuario in self.usuarios:
            self.cola_turnos.append(usuario)
        self.dados = [int, int]
        self.suma_dados = int
        self.mapa = Mapa()
        self.fase_inicio()

    def fase_inicio(self):
        random.shuffle(self.cola_turnos)
        self.mapa.cargar_mapa()
        self.construir_construcciones_iniciales()

    def construir_construcciones_iniciales(self):
        #  Construye las primeras casas
