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

        return ("Principal")


class MenuPrincipal(Menu):
    def __init__(self, campeonato):
        super().__init__("Principal", [self.menu_entrenador,
                                       self.simular_competencias,
                                       self.mostrar_estado,
                                       self.volver])
        self.campeonato = campeonato

    def menu_entrenador(self):
        return("Entrenador")

    def simular_competencias(self):
        pass

    def mostrar_estado(self):
        pass

    def volver(self):
        return "Inicio"


class MenuEntrenador(Menu):
    def __init__(self, campeonato):
        super().__init__("Entrenador", [self.fichar, self.entrenar,
                                        self.comprar_tecnologia,
                                        self.usar_habilidad_especial,
                                        self.volver])
        self.campeonato = campeonato

    def fichar(self):
        pass

    def entrenar(self):
        pass

    def comprar_tecnologia(self):
        pass

    def usar_habilidad_especial(self):
        pass

    def volver(self):
        return("Principal")


class DictMenu(dict):
    """Diccionario de menus de la clase Menu, con el cual se puede ir moviendo entre
    menus segun la key que valla devolviendo el otro menu"""
    def __init__(self):
        self.key = "Inicio"

    def invocar(self):
        menu = self[self.key]
        while True:
            cambiar_menu = menu.interactuar()
            if cambiar_menu:
                self.key = cambiar_menu
                break


if __name__ == "__main__":
    from campeonato import Campeonato
    from clases_simulacion import Deportista, IEEEsparta, DCCrotona
    from deportes import Atletismo, Ciclismo, Gimnacia, Natacion

    menu_inicio = MenuInicio()

    # Crea instancias de prueba
    d1 = Deportista("Alexis", 14, 20, 30, 88, False, 20)
    d2 = Deportista("Charles", 15, 23, 43, 50, True, 23)
    d3 = Deportista("Mago Valdivia", 23, 34, 21, 21, False, 100)
    d4 = Deportista("Mati Fernandez", 21, 22, 12, 44, False, 42)
    lista_deportistas = [d3, d4]
    delegacion1 = DCCrotona("Lucho", [d1, d2, d3], 5, 40, 300)
    delegacion2 = IEEEsparta("Pancho", [d4], 4, 50, 400)
    atletismo = Atletismo()
    cilcismo = Ciclismo()
    gimnacia = Gimnacia()
    natacion = Natacion()
    campeonato = Campeonato(delegacion1, delegacion2, [atletismo, cilcismo, gimnacia, natacion])

    menu_principal = MenuPrincipal(campeonato)
    menu_entrenador = MenuEntrenador(campeonato)

    menus = DictMenu()

    menus["Inicio"] = menu_inicio
    menus["Principal"] = menu_principal
    menus["Entrenador"] = menu_entrenador

    while True:
        menus.invocar()
