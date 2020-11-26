from juego.items.cartas import Mazo
from juego.mapa.mapa import Mapa


class Juego():

    def __init__(self, usuarios, net):
        self.net = net
        self.usuarios = usuarios
        self.puntos = {usuario: 0 for usuario in self.usuarios}
        self.mazos = {usuario: Mazo() for usuario in self.usuarios}
        self.mapa = Mapa()
        self.iniciar_juego()

    def iniciar_juego(self):
        numeros, materias_primas = self.mapa.datos_mapa()
        self.net.send_command_to_all("cargar_mapa", [numeros, materias_primas])
        self.net.send_command_to_all("cargar_usuarios")

    def actualizar_materias_primas(self):
        dict_materias = {}
