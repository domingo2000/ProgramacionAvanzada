from juego.entidades.usuario import Usuario
from collections import deque
import random


class Juego:

    def __init__(self, nombres_usuarios):
        self.usuarios = [Usuario(nombre_usuario) for nombre_usuario in nombres_usuarios]
        self.cola_turnos = deque()
        for usuario in self.usuarios:
            self.cola_turnos.append()
        self.dados = [int, int]
        self.suma_dados = int

    def fase_inicio(self):
        random.shuffle(self.cola_turnos)
