from abc import ABC, abstractmethod
import sys
import lectura_datos as csv
from clases_simulacion import Deportista, DCCrotona, IEEEsparta
from campeonato import Campeonato
from deportes import Atletismo, Ciclismo, Gimnacia, Natacion
import parametros as p


class Menu(ABC):

    def __init__(self, nombre, opciones=None, atributos_mostrados=[]):
        self.nombre = nombre
        self.opciones = opciones
        self.ui = [f"\n-----Menu {self.nombre}----"]
        self.atributos_mostrados = atributos_mostrados
        # agrega la opcion de salir al final
        self.opciones.append(self.salir)
        # Agrega los atributos mostrados a la interfaz del menu
        for atributo in self.atributos_mostrados:
            self.ui.append(f"{atributo[0]}: {atributo[1]}")
        # Agrega las opciones a la interfaz del menu
        i = 0
        for opcion in opciones:
            nombre_opcion = ""
            for palabra in opcion.__name__.split("_"):
                nombre_opcion += (palabra + " ")
            self.ui.append(f"[{i}]  {nombre_opcion}")
            i += 1

    def interactuar(self):
        self.actualizar_ui()
        self.mostrar_ui()
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

    def actualizar_ui(self):
        pass

    def mostrar_ui(self):
        for linea in self.ui:
            print(linea)

    def salir(self):
        print("Saliendo del programa...")
        sys.exit()


class MenuInicio(Menu):
    def __init__(self):
        super().__init__("Inicio", [self.iniciar_nueva_partida])

    def iniciar_nueva_partida(self):
        # borra los datos preexistentes del archivo resultados
        csv.limpiar_archivo_resultados("resultados.txt")
        # loop nombre usuario
        while True:
            nombre_propio = input("Ingrese su nombre: ")
            if nombre_propio.isalnum():
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
        # loop escoger delegacion
        while True:
            delegaciones_disponibles = {0: "IEEEsparta", 1: "DCCrotona"}
            print("\nEscoja entre una de las dos delegaciones")
            print(f"[0] IEEEsparta\n[1] DCCrotona")
            delegacion_escogida = input("Escoja una opcion: ")
            if ((delegacion_escogida != "0") and (delegacion_escogida != "1")):
                print("Entrada Invalida!, por favor ingrese una opcion valida")
                continue
            else:
                delegacion_escogida = delegaciones_disponibles[int(delegacion_escogida)]
                break

        # lectura de datos de archivos .csv
        datos_deportistas = csv.leer_datos_deportistas("deportistas.csv")
        datos_delegaciones = csv.leer_datos_delegaciones("delegaciones.csv")

        # instancia todos los deportistas
        lista_deportistas = []
        for dato in datos_deportistas:
            nombre = dato["nombre"]
            velocidad = int(dato["velocidad"])
            resistencia = int(dato["resistencia"])
            flexibilidad = int(dato["flexibilidad"])
            moral = int(dato["moral"])
            lesionado = csv.leer_bool(dato["lesionado"])
            precio = int(dato["precio"])
            deportista = Deportista(nombre, velocidad,
                                    resistencia, flexibilidad, moral, lesionado, precio)
            lista_deportistas.append(deportista)
        # instancia los deportes
        atletismo = Atletismo()
        ciclismo = Ciclismo()
        gimnacia = Gimnacia()
        natacion = Natacion()
        lista_deportes = [atletismo, ciclismo, gimnacia, natacion]
        # instancia las delegaciones
        lista_delegaciones = []
        for dato in datos_delegaciones:
            equipo = []
            nombres_equipo = dato["Equipo"].split(";")
            for nombre_deportista in nombres_equipo:
                COUNT = 0
                while True:
                    deportista = lista_deportistas[COUNT]
                    if deportista.nombre == nombre_deportista:
                        equipo.append(lista_deportistas.pop(COUNT))
                        break
                    else:
                        COUNT += 1
            tipo_delegacion = dato["Delegacion"]
            entrenador = "NADIE_POR_AHORA"
            equipo = equipo
            moral = float(dato["Moral"])
            dinero = int(dato["Dinero"])
            medallas = int(dato["Medallas"])
            if tipo_delegacion == "DCCrotona":
                delegacion = DCCrotona(entrenador, equipo, medallas, moral, dinero)
            elif tipo_delegacion == "IEEEsparta":
                delegacion = IEEEsparta(entrenador, equipo, medallas, moral, dinero)
            else:
                print("ERROR")
            lista_delegaciones.append(delegacion)

        # Decide que delegacion es para que jugador , referencia ambas delegaciones
        # y asigna los entrenadores a las delegaciones
        i = 0
        while len(lista_delegaciones) > 0:
            delegacion = lista_delegaciones[i]
            if delegacion.nombre == delegacion_escogida:
                delegacion_propia = lista_delegaciones.pop(i)
                delegacion_propia.entrenador = nombre_propio
            else:
                delegacion_rival = lista_delegaciones.pop(i)
                delegacion_rival.entrenador = nombre_rival
        # Instancia Campeonato
        campeonato = Campeonato(delegacion_propia, delegacion_rival,
                                lista_deportistas, lista_deportes)
        return ["Principal", campeonato]


class MenuPrincipal(Menu):
    def __init__(self, campeonato):
        self.campeonato = campeonato
        atributos_mostrados = [["Dinero Delegacion", self.campeonato.delegacion1.dinero],
                               ["Moral Delegacion", self.campeonato.delegacion1.moral]]
        super().__init__("Principal", [self.menu_entrenador,
                                       self.simular_competencias,
                                       self.mostrar_estado,
                                       self.volver], atributos_mostrados=atributos_mostrados)

    def actualizar_ui(self):
        linea_dinero = f"Dinero delegacion: {self.campeonato.delegacion1.dinero}"
        linea_moral = f"Moral delegacion: {self.campeonato.delegacion1.moral}"
        self.ui[1] = linea_dinero
        self.ui[2] = linea_moral

    def menu_entrenador(self):
        return ["Entrenador"]

    def simular_competencias(self):
        self.campeonato.dia_actual += 1

        self.campeonato.realizar_competencias_del_dia()
        self.campeonato.dia_actual += 1

        if self.campeonato.dia_actual > p.DIAS_COMPETENCIA:
            # Flujo fin competencia
            self.campeonato.calcular_ganador()
            return["Inicio"]
            pass
        else:
            pass

    def mostrar_estado(self):
        campeonato = self.campeonato.mostrar_estado()

    def volver(self):
        return ["Inicio"]


class MenuEntrenador(Menu):
    def __init__(self, campeonato):
        self.campeonato = campeonato
        atributos_mostrados = [["Dinero Delegacion", self.campeonato.delegacion1.dinero],
                               ["Moral Delegacion", self.campeonato.delegacion1.moral]]
        super().__init__("Entrenador", [self.fichar, self.entrenar,
                                        self.sanar, self.comprar_tecnologia,
                                        self.usar_habilidad_especial,
                                        self.volver], atributos_mostrados=atributos_mostrados)

    def actualizar_ui(self):
        linea_dinero = f"Dinero delegacion: {self.campeonato.delegacion1.dinero}"
        linea_moral = f"Moral delegacion: {self.campeonato.delegacion1.moral}"
        self.ui[1] = linea_dinero
        self.ui[2] = linea_moral

    def fichar(self):
        lista_deportistas = self.campeonato.deportistas_no_fichados
        while True:
            print(f"\nDinero Actual: {self.campeonato.delegacion1.dinero}")
            print(f"Seleccione un deportista para fichar")
            i = 0
            for deportista in lista_deportistas:
                print(f"[{i}] {deportista.nombre}")
                print(f"    precio : {deportista.precio} DCCoins")
                print(f"    velocidad : {deportista.velocidad}")
                print(f"    resistencia : {deportista.resistencia}")
                print(f"    flexibilidad : {deportista.flexibilidad}")
                print(f"    moral : {deportista.moral}")
                print(f"    lesionado : {deportista.lesionado}")
                i += 1
            print(f"[{i}] Volver")
            entrada = input("Seleccione un deportista para fichar: ")
            print("\n")
            if entrada == str(i):
                print("Usted no ha fichado ningun jugador")
                print("Volviendo al Menu de Entrenador...")
                return None
            elif entrada.isdigit():
                entrada = int(entrada)
                if 0 <= entrada <= i:
                    deportista_seleccionado = lista_deportistas[entrada]
                    nombre_deportista = deportista_seleccionado.nombre
                    self.campeonato.delegacion1.fichar_deportista(nombre_deportista,
                                                                  lista_deportistas)
                    break
            else:
                print("Entrada inválida! Ingrese una opción valida")

    def entrenar(self):
        print(f"Dinero Actual: {self.campeonato.delegacion1.dinero}")
        self.campeonato.delegacion1.entrenar_deportista()

    def sanar(self):
        print(f"Dinero Actual: {self.campeonato.delegacion1.dinero}")
        self.campeonato.delegacion1.sanar_lesiones()

    def comprar_tecnologia(self):
        print(f"Dinero Actual: {self.campeonato.delegacion1.dinero}")
        print(f"Esta accion le costara {p.COSTO_COMPRAR_TECNOLOGIA} DCCoins")
        print(f"¿Esta seguro de que quiere comprar tecnología?")
        print("[0] Si\n Ingrese cualquier cosa para cancelar")
        entrada = input("Seleccione una opcion: ")
        if entrada == "0":
            self.campeonato.delegacion1.comprar_tecnologia()
        else:
            print("Compra cancelada\n")

    def usar_habilidad_especial(self):
        self.campeonato.delegacion1.utilizar_habilidad_especial()

    def volver(self):
        return ["Principal"]


class DictMenu(dict):
    """Diccionario de menus de la clase Menu, con el cual se puede ir moviendo entre
    menus segun la key que valla devolviendo el otro menu"""
    def __init__(self):
        self.key = "Inicio"

    def invocar(self):
        menu = self[self.key]
        while True:
            datos_menu = menu.interactuar()
            if type(datos_menu) == list:
                cambiar_menu = datos_menu[0]
            else:
                cambiar_menu = False
            if cambiar_menu:
                self.key = cambiar_menu
                break
        return(datos_menu[1:])


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
    campeonato = Campeonato(delegacion1, delegacion2, lista_deportistas,
                            [atletismo, cilcismo, gimnacia, natacion])

    menu_principal = MenuPrincipal(campeonato)
    menu_entrenador = MenuEntrenador(campeonato)

    menus = DictMenu()

    menus["Inicio"] = menu_inicio
    menus["Principal"] = menu_principal
    menus["Entrenador"] = menu_entrenador

    while True:
        menus.invocar()
