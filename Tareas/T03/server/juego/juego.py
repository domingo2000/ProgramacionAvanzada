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
        self.actualizar_materias_primas()

    def actualizar_materias_primas(self):
        dict_materias = {usuario: self.mazos[usuario].cartas for usuario in self.usuarios}
        self.net.send_command_to_all("actualizar_materias_primas", [dict_materias])

    def actualizar_construcciones(self):
        self.net.send_command_to_all("actualizar_construcciones")

    def asignar_casas_aleatorias(self):
        pass

    def asignar_caminos_aleatorios(self):
        pass

    def asignar_casa(self, id_nodo, usuario):
        self.mapa.nodos[id_nodo].estado = "ocupado"
        self.mapa.nodos[id_nodo].usuario = usuario

        return True

    def validar_posicion_casa(self, id_nodo):
        vecinos = self.mapa.vecinos(id_nodo)
        for id_nodo in vecinos:
            if self.mapa.nodos[id_nodo].estado == "ocupado":
                return False
        return True
