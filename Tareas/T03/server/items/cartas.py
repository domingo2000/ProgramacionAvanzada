import json
from funciones import crear_diccionario_costos

# Importa los datos del archivo de parametros
with open("parametros.json") as file:
    data = json.load(file)
costos = data["costos"]


class Carta():

    def __init__(self, nombre_carta):
        self.nombre_carta = f"carta_{nombre_carta}"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.nombre_carta}"


class CartaMateriaPrima(Carta):

    def __init__(self, materia_prima):
        super().__init__(materia_prima)
        self.materia = materia_prima


class CartaDesarrollo(Carta):

    def __init__(self, nombre_carta):
        super().__init__(nombre_carta)
        self.tipo = nombre_carta
        self.costo = crear_diccionario_costos(costos["carta_desarrollo"])


class CartaPuntoVictoria(CartaDesarrollo):

    def __init__(self, numero):
        super().__init__(f"punto_de_victoria_{numero}")
        self.tipo = "victoria"
        self.numero = 1
        self.puntos = 1


class CartaMonopolio(CartaDesarrollo):

    def __init__(self):
        super().__init__("monopolio")


if __name__ == "__main__":
    carta_madera = CartaMateriaPrima("madera")
    carta_arcilla = CartaMateriaPrima("arcilla")
    carta_trigo = CartaMateriaPrima("trigo")

    carta_monopolio = CartaMonopolio()
    carta_punto_victoria_1 = CartaPuntoVictoria(1)
    carta_punto_victoria_2 = CartaPuntoVictoria(2)

    mazo = []
    mazo.append(carta_arcilla)
    mazo.append(carta_trigo)
    mazo.append(carta_monopolio)
    mazo.append(carta_punto_victoria_1)
    mazo.append(carta_punto_victoria_2)

    print(mazo)
    print(carta_monopolio.costo)
    print(carta_punto_victoria_1.tipo)
