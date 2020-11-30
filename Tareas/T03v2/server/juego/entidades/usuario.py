from juego.items.mazo import Mazo
from faker import Faker
from networking import interfaz_network

faker = Faker()


class Usuario:

    def __init__(self, nombre):
        self.__nombre = nombre
        self.mazo = Mazo(self.nombre)
        self.__puntos = 0
        self.__puntos_victoria = 0
        self.init_usuario()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor
        interfaz_network.send_command_to_all("load_user_name", self.nombre)
        print(f"Enviar Comando Fijar nombre usuario {self.nombre}")

    @property
    def puntos(self):
        return self.__puntos

    @puntos.setter
    def puntos(self, valor):
        self.__puntos = valor
        interfaz_network.send_command_to_all("update_points", self.nombre, valor)

    @property
    def puntos_victoria(self):
        return self.__puntos_victoria

    @puntos_victoria.setter
    def puntos_victoria(self, valor):
        self.__puntos_victoria = valor
        interfaz_network.send_command(self.nombre, "update_victory_points", valor)
        print(f"Enviar Comando cambiar puntos: {valor}, {self.nombre}")

    def __repr__(self):
        return f"Usuario: {self.nombre}"

    def init_usuario(self):
        self.puntos = 0
        self.puntos_victoria = 0
        self.nombre = self.nombre


if __name__ == "__main__":
    usuario_1 = Usuario()
    print(usuario_1)
