from abc import ABC, abstractmethod
from random import uniform, random
import parametros as p


class Delegacion(ABC):
    """Clase que define las delegaciones

    Esta clase contiene las delegaciones que participan en la simulacion,
    dentro de estas estaran los deportistas que compiter

    """

    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        self.entrenador = entrenador
        self.equipo = equipo
        self.__medallas = medallas
        self.__moral = moral
        self.__dinero = dinero
        self.__excelencia_y_respeto = None
        self.__implementos_deportivos = None
        self.__implementos_medicos = None

    @property
    def medallas(self):
        return(self.__medallas)

    @medallas.setter
    def medallas(self, medallas):
        self.__excelencia_y_respeto += 0.01
        self.__medallas = medallas

    @property
    def moral(self):
        # completar recalcular moral
        return self.__moral

    @moral.setter
    def moral(self, moral):
        if 0 <= moral <= 100:
            self.__moral = moral
        elif moral < 0:
            self.__moral = 0
        elif moral > 100:
            self.__moral = 100

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, dinero):
        if dinero < 0:
            self.__dinero = 0
        else:
            self.__dinero = dinero

    @property
    def excelencia_y_respeto(self):
        return self.__excelencia_y_respeto

    @excelencia_y_respeto.setter
    def excelencia_y_respeto(self, excelencia_y_respeto):
        if excelencia_y_respeto < 0:
            self.__excelencia_y_respeto = 0
        elif excelencia_y_respeto > 1:
            self.__excelencia_y_respeto = 1
        else:
            self.__excelencia_y_respeto = excelencia_y_respeto

    @property
    def implementos_deportivos(self):
        return self.__implementos_deportivos

    @implementos_deportivos.setter
    def implementos_deportivos(self, implementos_deportivos):
        if implementos_deportivos < 0:
            self.__implementos_deportivos = 0
        elif implementos_deportivos > 1:
            self.__implementos_deportivos = 1
        else:
            self.__implementos_deportivos = implementos_deportivos

    @property
    def implementos_medicos(self):
        return self.__implementos_medicos

    @implementos_deportivos.setter
    def implementos_medicos(self, implementos_medicos):
        if implementos_medicos < 0:
            self.__implementos_medicos = 0
        elif implementos_medicos > 1:
            self.__implementos_medicos = 1
        else:
            self.__implementos_medicos = implementos_medicos

    def fichar_deportista(self, nombre_deportista, lista_deportistas):
        for deportista in lista_deportistas:
            if nombre_deportista == deportista.nombre:
                costo = deportista.precio
                if self.dinero > costo:
                    self.dinero -= costo
                    self.equipo.append(deportista)
                    lista_deportistas.remove(deportista)
                    print(f"Ha fichado a {nombre_deportista} por {costo} DCCoins")
                else:
                    print("No tiene DCCoins suficientes para realizar el fichaje!")

    def entrenar_deportista(self, ponderador_entrenamiento=1):
        # Chequea que haya sufiiente dinero
        if self.dinero >= 30:
            self.dinero -= 30
            # string que se muestra en la interfaz
            print("Seleccione un jugador para entrenar")
            for i in range(len(self.equipo)):
                print(f"[{i}] {self.equipo[i]}")

            # selecciona deportista
            while True:
                entrada = input("Ingrese una opción: ")
                if entrada.isdigit():
                    entrada = int(entrada)
                    if 0 <= entrada <= (len(self.equipo) - 1):
                        deportista_seleccionado = self.equipo[entrada]
                        break
                print("Entrada Invalida!, Ingrese otra vez")
            # selecciona que atributo quiere entrenar
            dict_atributos = {0: "velocidad", 1: "resistencia", 2: "flexibilidad"}
            print("Seleccione un atributo para entrenar")
            print("[0] Velocidad")
            print("[1] Resistencia")
            print("[2] Flexibilidad")
            while True:
                entrada = input("Ingrese una opción: ")
                if entrada.isdigit():
                    entrada = int(entrada)
                    if 0 <= entrada <= 2:
                        atributo_seleccionado = dict_atributos[entrada]
                        break
                print("Entrada Invalida!, Ingrese otra vez")
            deportista_seleccionado.moral += 1
            deportista_seleccionado.entrenar(atributo_seleccionado, ponderador_entrenamiento)

        else:
            print("No tiene suficiente dinero para entrenar un deportista!")

    def sanar_lesiones(self, ponderador_costo = 1):
        if self.dinero >= 30:
            deportistas_lesionados = []
            i = 0
            # string que se muestra en la interfaz y llenado deportistas_lesionados
            print("Seleccione el deportista que desa sanar: ")
            for deportista in self.equipo:
                if deportista.lesionado:
                    deportistas_lesionados.append(deportista)
                    print(f"[{i}] {deportista.nombre}")
                    i += 1
            indice_opcion_volver = len(deportistas_lesionados)
            print(f"[{indice_opcion_volver}] Volver")
            # selecciona deportista
            while True:
                entrada = input("Ingrese una opción: ")
                # Caso que quiera volver por si no hay nadie a quien sanar
                if entrada == str(indice_opcion_volver):
                    return None
                if entrada.isdigit():
                    entrada = int(entrada)
                    if 0 <= entrada <= (len(deportistas_lesionados) - 1):
                        deportista_seleccionado = deportistas_lesionados[entrada]
                        break
                print("Entrada Invalida!, Ingrese otra vez")
            # calculo_probabilidad_recuperacion
            datos_delegacion = delegacion.implementos_medicos + delegacion.excelencia_y_respeto
            valor_calculado = (deportista_seleccionado.moral * datos_delegacion) / 200
            probabilidad_recuperacion = min(1, max(0, valor_calculado))
            probabilidad_recuperacion = round(probabilidad_recuperacion, 1)
            numero_aleatorio = random()
            # cobro por sanar jugador
            self.dinero -= 30 * ponderador_costo
            # chequea la probabilidad y sana al jugador
            if numero_aleatorio < probabilidad_recuperacion:
                print("Enhorabuena! Tu deportista se ha recuperado de su lesión")
                deportista_seleccionado.lesionado = False
            else:
                print("Que lástima!, tu deportista no se ha recuperado")
        else:
            print(f"Su dinero ({self.dinero}) no alcanza para sanar un deportista")

    def comprar_tecnologia(self):
        if self.dinero >= 20:
            self.dinero -= 20
            tecnologia_anterior = self.__implementos_deportivos
            self.implementos_deportivos *= 1.1
            self.implementos_medicos *= 1.1
            print(f"Usted ha Mejorado su tecnologia!")

        else:
            print(f"Su dinero ({self.dinero}) no alcanza para compra tecnología")

    @abstractmethod
    def utilizar_habilidad_especial(self):
        pass


class IEEEsparta(Delegacion):
    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        super().__init__(entrenador, equipo, medallas, moral, dinero)
        self.excelencia_y_respeto = uniform(0.4, 0.8)
        self.implementos_deportivos = uniform(0.3, 0.7)
        self.implementos_medicos = uniform(0.2, 0.6)

    def entrenar_deportista(self):
        super().entrenar_deportista(ponderador_entrenamiento=1.7)

    def utilizar_habilidad_especial(self):
        pass


class DCCrotona(Delegacion):
    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        super().__init__(entrenador, equipo, medallas, moral, dinero)
        self.excelencia_y_respeto = uniform(0.3, 0.7)
        self.implementos_deportivos = uniform(0.2, 0.6)
        self.implementos_medicos = uniform(0.4, 0.8)

    @Delegacion.medallas.setter
    def medallas(self, medallas):
        self.__excelencia_y_respeto += 0.01 * 2
        self.__medallas = medallas

    def sanar_lesiones(self):
        super().sanar_lesiones(ponderador_costo=2)  # pondera el costo de sanar por 2

    def utilizar_habilidad_especial(self):
        pass


class Deportista:
    def __init__(self, nombre, velocidad, resistencia, flexibilidad, moral, lesionado, precio):
        self.nombre = nombre
        self.lesionado = lesionado
        self.precio = precio
        self.__velocidad = velocidad
        self.__resistencia = resistencia
        self.__flexibilidad = flexibilidad
        self.__moral = moral

    @property
    def velocidad(self):
        return self.__velocidad

    @velocidad.setter
    def velocidad(self, velocidad):
        if velocidad < 0:
            self.__velocidad = 0
        elif velocidad > 100:
            self.__velocidad = 100
        else:
            self.__velocidad = velocidad

    @property
    def resistencia(self):
        return self.__resistencia

    @resistencia.setter
    def resistencia(self, resistencia):
        if resistencia < 0:
            self.__resistencia = 0
        elif resistencia > 100:
            self.__resistencia = 100
        else:
            self.__resistencia = resistencia

    @property
    def flexibilidad(self):
        return self.__flexibilidad

    @flexibilidad.setter
    def flexibilidad(self, flexibilidad):
        if flexibilidad < 0:
            self.__flexibilidad = 0
        elif flexibilidad > 100:
            self.__flexibilidad = 100
        else:
            self.__flexibilidad = flexibilidad

    @property
    def moral(self):
        return self.__moral

    @moral.setter
    def moral(self, moral):
        if moral < 0:
            self.__moral = 0
        elif moral > 100:
            self.__moral = 100
        else:
            self.__moral = moral

    def entrenar(self, atributo, ponderador_entrenamiento):
        puntos_entrenamiento = p.PUNTOS_ENTRENAMIENTO * ponderador_entrenamiento
        if atributo == "velocidad":
            self.velocidad += puntos_entrenamiento
        elif atributo == "resistencia":
            self.resistencia += puntos_entrenamiento
        elif atributo == "flexibilidad":
            self.flexibilidad += puntos_entrenamiento
        else:
            print("ERROR ATRIBUTO MAL PASADO A LA FUNCION")

        print(f"Se ha entrenado la {atributo} de {self.nombre}")

    def __repr__(self):
        string = f"Jugador: {self.nombre}"
        return string


if __name__ == "__main__":
    d1 = Deportista("Alexis", 14, 20, 30, 88, True, 20)
    d2 = Deportista("Charles", 15, 23, 43, 50, True, 23)
    d3 = Deportista("Mago Valdivia", 23, 34, 21, 21, False, 100)
    d4 = Deportista("Mati Fernandez", 21, 22, 12, 44, False, 42)
    lista_deportistas = [d3, d4]
    delegacion = IEEEsparta("Lucho", [d1, d2], 5, 40, 300)

    """Testeo fichas deportista
    delegacion.fichar_deportista("Mago Valdivia", lista_deportistas)

    print(delegacion.equipo)
    """
    """ Testeo entrenar deportista
    print(f"dinero Delegacion: {delegacion.dinero}")
    print(f"moral: {d2.moral}, velocidad: {d2.velocidad}, resistencia: {d2.resistencia}, flexibilidad: {d2.flexibilidad}")
    delegacion.entrenar_deportista()
    print("######### Despues de entrenar ################")
    print(f"moral: {d2.moral}, velocidad: {d2.velocidad}, resistencia: {d2.resistencia}, flexibilidad: {d2.flexibilidad}")
    print(f"dinero Delegacion: {delegacion.dinero}")
    """
