from abc import ABC, abstractmethod
import sys


class Menu:

    def __init__(self, nombre, opciones=None):
        self.nombre = nombre
        self.opciones = opciones
        self.ui = f"-----Menu {self.nombre}----\n"

        # agrega la opcion de salir al final
        self.opciones.append(self.salir)
        # Agrega las opciones a la interfaz del menu
        i = 0
        for opcion in opciones:
            nombre_opcion = ""
            for palabra in opcion.__name__.split("_"):
                nombre_opcion += (palabra + " ")
            self.ui += f"[{i}]  {nombre_opcion}\n"
            i += 1

    def interactuar(self):
        print(self.ui)
        while True:
            numero_opcion = input("Ingrese el valor deseado: ")
            if numero_opcion.isnumeric():
                numero_opcion = int(numero_opcion)
                if 0 <= numero_opcion < len(self.opciones):
                    break
            print("Opcion Invalida, ingrese otro valor!")
        # booleano que decide si se avanza o se retrocede de menu
        cambiar_menu = self.opciones[numero_opcion]()
        return cambiar_menu

    def salir(self):
        print("Saliendo del programa...")
        sys.exit()


class MenuInicio(Menu):
    def __init__(self):
        super().__init__("Inicio", [self.iniciar_nueva_partida])

    def iniciar_nueva_partida(self):
        # loop nombre usuario
        while True:
            nombre = input("Ingrese su nombre: ")
            if nombre.isalnum():
                break
            else:
                print("Nombre Inválido, ingrese nuevamente")
        # loop nombre rival
        while True:
            nombre_rival = input("Ingrese el nombre de su rival: ")
            if nombre_rival.isalnum():
                break
            else:
                print("Nombre Inválido, ingrese nuevamente")

        return ("Avanzar")


class MenuPrincipal(Menu):
    def __init__(self):
        super().__init__("Principal", [self.menu_entrenador,
                                       self.simular_competencias,
                                       self.mostrar_estado, volver])

    def menu_entrenador(self):
        return("Avanzar")

    def simular_competencias(self):
        pass

    def mostrar_estado(self):
        pass


class MenuEntrenador(Menu):
    def __init__(self):
        super().__init__("Entrenador", [self.fichar, self.entrenar,
                                        self.comprar_tecnologia,
                                        self.usar_habilidad_especial, volver])

    def fichar(self):
        pass

    def entrenar(self):
        pass

    def comprar_tecnologia(self):
        pass

    def usar_habilidad_especial(self):
        pass


class ListaMenu(list):
    """Es un stack de menus de la clase Menu, con el cual se invoca el ultimo
    menu del stack, y se puede volver entre menus corriendo y popeando el
    ultimo menu"""
    def __init__(self):
        self.indice = 0

    def invocar(self):
        menu = self[self.indice]
        while True:
            cambiar_menu = menu.interactuar()
            if cambiar_menu == "Avanzar":
                self.avanzar()
                break
            elif cambiar_menu == "Retroceder":
                self.volver()
                break

    def volver(self):
        self.indice -= 1

    def avanzar(self):
        self.indice += 1


def volver():
    return "Retroceder"


if __name__ == "__main__":
    def suma():
        print("FUNCION SUMA!")

    def resta():
        print("FUNCION RESTA!")

    def mult():
        print("FUNCION MULT!")

    def volver():
        return("Retroceder")

    menu_inicio = MenuInicio()
    menu_2 = Menu("2", [suma, resta, volver])
    menu_principal = MenuPrincipal()
    menu_entrenador = MenuEntrenador()

    menus = ListaMenu()

    menus.append(menu_inicio)
    menus.append(menu_principal)
    menus.append(menu_entrenador)
    menus.append(menu_2)


while True:
    menus.invocar()
