class Juego():

    def __init__(self, usuarios, net):
        self.usuarios = usuarios
        self.net = net
        self.puntos = {self.usuario: 0 for usuario in self.usuarios}
        molde_materias_primas = {"madera"}
        self.materias_primas = {self.usuario: 0 for usuario in self.usuarios}
