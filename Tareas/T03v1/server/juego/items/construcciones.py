import json
from juego.items.funciones import crear_diccionario_costos
with open("parametros.json") as file:
    data = json.load(file)
costos = data["costos"]


class Construccion:

    def __init__(self, nombre, puntos, data_costo):
        self.nombre = nombre
        self.puntos = puntos
        self.costo = crear_diccionario_costos(data_costo)

    def __repr__(self):
        return f"{self.__class__}: Puntos: {self.puntos}"


class Carretera(Construccion):

    def __init__(self):
        super().__init__("carretera", 1, costos["carretera"])


class Choza(Construccion):

    def __init__(self):
        super().__init__("choza", 1, costos["choza"])


if __name__ == "__main__":
    choza = Choza()
    camino = Carretera()

    print(choza)
    print(camino)
