import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)
    COSTOS = PARAMETROS["costos"]


class Choza:
    num = 0
    costo = COSTOS["choza"]
    puntos = 1
    cartas_entregadas = 1

    def __init__(self, usuario):
        Choza.num += 1
        self.num = Choza.num
        self.__usuario = usuario
        self.nombre = "choza"

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, valor):
        self.__usuario = valor


class Ciudad:
    costo = COSTOS["ciudad"]
    puntos = 2
    cartas_entregadas = 2

    def __init__(self, nombre_usuario):
        self.__usuario = str
        self.nombre = "ciudad"


    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, valor):
        self.__usuario = valor


class Camino:
    costo = COSTOS["camino"]
    puntos = 1

    def __init__(self, usuario):
        self.__usuario = usuario
        self.nombre = "camino"

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, valor):
        self.__usuario = valor



if __name__ == "__main__":
    choza = Choza("pepito")
    print(choza.costo)
