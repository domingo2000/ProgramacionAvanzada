from abc import ABC, abstractmethod
from random import uniform, random
import parametros as p


class Delegacion(ABC):
    """Clase que define las delegaciones

    Esta clase contiene las delegaciones que participan en la simulacion,
    dentro de estas estaran los deportistas que compiter

    """

    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        self.nombre = None
        self.entrenador = entrenador
        self.equipo = equipo
        self.medallero_delegacion = {"atletismo": 0, "ciclismo": 0, "gimnacia": 0, "natacion": 0}
        self._medallas = medallas
        self.__moral = moral
        self.__dinero = dinero
        self.__excelencia_y_respeto = None
        self.__implementos_deportivos = None
        self.__implementos_medicos = None

    @property
    def medallas(self):
        return(self._medallas)

    @medallas.setter
    def medallas(self, medallas):
        self.excelencia_y_respeto += p.AUMENTO_EXCELENCIA_POR_MEDALLA
        self._medallas = medallas

    @property
    def moral(self):
        # completar recalcular moral
        return self.__moral

    @moral.setter
    def moral(self, moral):
        if p.MORAL_MINIMA_DELEGACION <= moral <= p.MORAL_MAXIMA_DELEGACION:
            self.__moral = moral
        elif moral < p.MORAL_MINIMA_DELEGACION:
            self.__moral = p.MORAL_MINIMA_DELEGACION
        elif moral > p.MORAL_MAXIMA_DELEGACION:
            self.__moral = p.MORAL_MAXIMA_DELEGACION

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, dinero):
        if dinero < 0:
            self.__dinero = 0
        else:
            self.__dinero = dinero

    # Properties Fortalezas
    @property
    def excelencia_y_respeto(self):
        return self.__excelencia_y_respeto

    @excelencia_y_respeto.setter
    def excelencia_y_respeto(self, excelencia_y_respeto):
        if excelencia_y_respeto < p.FORTALEZA_MINIMA:
            self.__excelencia_y_respeto = p.FORTALEZA_MINIMA
        elif excelencia_y_respeto > p.FORTALEZA_MAXIMA:
            self.__excelencia_y_respeto = p.FORTALEZA_MAXIMA
        else:
            self.__excelencia_y_respeto = excelencia_y_respeto

    @property
    def implementos_deportivos(self):
        return self.__implementos_deportivos

    @implementos_deportivos.setter
    def implementos_deportivos(self, implementos_deportivos):
        if implementos_deportivos < p.FORTALEZA_MINIMA:
            self.__implementos_deportivos = p.FORTALEZA_MINIMA
        elif implementos_deportivos > p.FORTALEZA_MAXIMA:
            self.__implementos_deportivos = p.FORTALEZA_MAXIMA
        else:
            self.__implementos_deportivos = implementos_deportivos

    @property
    def implementos_medicos(self):
        return self.__implementos_medicos

    @implementos_medicos.setter
    def implementos_medicos(self, implementos_medicos):
        if implementos_medicos < p.FORTALEZA_MINIMA:
            self.__implementos_medicos = p.FORTALEZA_MINIMA
        elif implementos_medicos > p.FORTALEZA_MAXIMA:
            self.__implementos_medicos = p.FORTALEZA_MAXIMA
        else:
            self.__implementos_medicos = implementos_medicos

    # Metodos
    def fichar_deportista(self, nombre_deportista, lista_deportistas):
        if self.moral > p.MORAL_NECESARIA_FICHAR_DEPORTISTA:
            for deportista in lista_deportistas:
                if nombre_deportista == deportista.nombre:
                    costo = deportista.precio
                    if self.dinero > costo:
                        self.dinero -= costo
                        self.equipo.append(deportista)
                        lista_deportistas.remove(deportista)
                        print(f"Ha fichado a {nombre_deportista} por {costo} DCCoins")
                        print(f"El deporista {nombre_deportista} se ha unido a tu equipo!")
                    else:
                        print("No tiene DCCoins suficientes para realizar el fichaje!")
        else:
            print("Tu delegacion no posee la moral suficiente para fichar un deportista")

    def entrenar_deportista(self, ponderador_entrenamiento=1):
        # Chequea que haya suficiente dinero
        if self.dinero >= p.COSTO_ENTRENAR_DEPORTISTA:
            self.dinero -= p.COSTO_ENTRENAR_DEPORTISTA
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

    def sanar_lesiones(self, ponderador_costo=1):
        if self.dinero >= p.COSTO_SANAR_LESIONES:
            print(f"Esta accion le costara {p.COSTO_SANAR_LESIONES * ponderador_costo} DCCoins")
            print(f"¿Esta seguro de que quiere Sanar Lesiones?")
            print("[0] Si\n Ingrese cualquier cosa para cancelar")
            entrada = input("Seleccione una opcion: ")
            if entrada == "0":
                pass
            else:
                print("Accion Cancelada\n")
                return None
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
            datos_delegacion = self.implementos_medicos + self.excelencia_y_respeto
            valor_calculado = ((deportista_seleccionado.moral * datos_delegacion)
                               / p.DIVISOR_FORMULA_SANAR_LESIONES)
            probabilidad_recuperacion = min(p.PROBABILIDAD_MAX_SANAR_LESIONES,
                                            max(p.PROBABILIDAD_MIN_SANAR_LESIONES,
                                                valor_calculado))
            probabilidad_recuperacion = round(probabilidad_recuperacion, 1)
            numero_aleatorio = random()
            # cobro por sanar jugador
            self.dinero -= p.COSTO_SANAR_LESIONES * ponderador_costo
            # chequea la probabilidad y sana al jugador
            if numero_aleatorio < probabilidad_recuperacion:
                print("Enhorabuena! Tu deportista se ha recuperado de su lesión")
                deportista_seleccionado.lesionado = False
            else:
                print("Que lástima!, tu deportista no se ha recuperado")
        else:
            print(f"Su dinero ({self.dinero}) no alcanza para sanar un deportista")

    def comprar_tecnologia(self):
        if self.dinero >= p.COSTO_COMPRAR_TECNOLOGIA:
            self.dinero -= p.COSTO_COMPRAR_TECNOLOGIA
            tecnologia_anterior = [self.implementos_deportivos, self.implementos_medicos]
            self.implementos_deportivos *= (1 + p.PORCENTAJE_AUMENTO_IMPLEMENTOS_POR_TECNOLOGIA)
            self.implementos_medicos *= (1 + p.PORCENTAJE_AUMENTO_IMPLEMENTOS_POR_TECNOLOGIA)
            print(f"Usted ha Mejorado su tecnologia!")
            print(f"Sus Implementos deportivos an pasado de {tecnologia_anterior[0]}"
                  f" a {self.implementos_deportivos}")
            print(f"Sus Implementos medicos an pasado de {tecnologia_anterior[1]}"
                  f" a {self.implementos_medicos}")
        else:
            print(f"Su dinero ({self.dinero}) no alcanza para compra tecnología")

    @abstractmethod
    def utilizar_habilidad_especial(self):
        pass


class IEEEsparta(Delegacion):
    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        super().__init__(entrenador, equipo, medallas, moral, dinero)
        self.nombre = "IEEEsparta"
        self.excelencia_y_respeto = uniform(p.EXCELENCIA_MAXIMA_IEEE,
                                            p.EXCELENCIA_MINIMA_IEEE)
        self.implementos_deportivos = uniform(p.IMPLEMENTOS_DEPORTIVOS_MINIMOS_IEEE,
                                              p.IMPLEMENTOS_DEPORTIVOS_MAXIMOS_IEEE)
        self.implementos_medicos = uniform(p.IMPLEMENTOS_MEDICOS_MINIMOS_IEEE,
                                           p.IMPLEMENTOS_MEDICOS_MAXIMOS_IEEE)

    def entrenar_deportista(self):
        super().entrenar_deportista(ponderador_entrenamiento=p.PONDERADOR_ENTRENAMIENTO_IEEE)

    def utilizar_habilidad_especial(self):
        pass


class DCCrotona(Delegacion):
    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        super().__init__(entrenador, equipo, medallas, moral, dinero)
        self.nombre = "DCCrotona"
        self.excelencia_y_respeto = uniform(p.EXCELENCIA_MAXIMA_DCC,
                                            p.EXCELENCIA_MINIMA_DCC)
        self.implementos_deportivos = uniform(p.IMPLEMENTOS_DEPORTIVOS_MINIMOS_DCC,
                                              p.IMPLEMENTOS_DEPORTIVOS_MAXIMOS_DCC)
        self.implementos_medicos = uniform(p.IMPLEMENTOS_MEDICOS_MINIMOS_DCC,
                                           p.IMPLEMENTOS_MEDICOS_MAXIMOS_DCC)

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
        if velocidad < p.VELOCIDAD_MINIMA:
            self.__velocidad = p.VELOCIDAD_MINIMA
        elif velocidad > p.VELOCIDAD_MAXIMA:
            self.__velocidad = p.VELOCIDAD_MAXIMA
        else:
            self.__velocidad = velocidad

    @property
    def resistencia(self):
        return self.__resistencia

    @resistencia.setter
    def resistencia(self, resistencia):
        if resistencia < p.RESISTENCIA_MINIMA:
            self.__resistencia = p.RESISTENCIA_MINIMA
        elif resistencia > p.RESISTENCIA_MAXIMA:
            self.__resistencia = p.RESISTENCIA_MAXIMA
        else:
            self.__resistencia = resistencia

    @property
    def flexibilidad(self):
        return self.__flexibilidad

    @flexibilidad.setter
    def flexibilidad(self, flexibilidad):
        if flexibilidad < p.FLEXIBILIDAD_MINIMA:
            self.__flexibilidad = p.FLEXIBILIDAD_MINIMA
        elif flexibilidad > p.FLEXIBILIDAD_MAXIMA:
            self.__flexibilidad = p.FLEXIBILIDAD_MAXIMA
        else:
            self.__flexibilidad = flexibilidad

    @property
    def moral(self):
        return self.__moral

    @moral.setter
    def moral(self, moral):
        if moral < p.MORAL_MINIMA:
            self.__moral = p.MORAL_MINIMA
        elif moral > p.MORAL_MAXIMA:
            self.__moral = p.MORAL_MAXIMA
        else:
            self.__moral = moral

    def entrenar(self, atributo, ponderador_entrenamiento=1):
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

    def lesionarse(self, riesgo):
        numero_aleatorio = random()
        if numero_aleatorio <= riesgo:
            print(f"{self.nombre} se ha lesionado durante la competencia")
            self.lesionado = True

    def __repr__(self):
        string = (f"{self.nombre}:\n-----Vel: {self.velocidad} "
                  + f"Res :{self.resistencia} "
                  + f"Flex : {self.flexibilidad} "
                  + f"Moral: {self.moral}")
        return string


if __name__ == "__main__":
    d1 = Deportista("Alexis", 14, 20, 30, 88, True, 20)
    d2 = Deportista("Charles", 15, 23, 43, 50, True, 23)
    d3 = Deportista("Mago Valdivia", 23, 34, 21, 21, False, 100)
    d4 = Deportista("Mati Fernandez", 21, 22, 12, 44, False, 42)
    lista_deportistas = [d3, d4]
    delegacion = DCCrotona("Lucho", [d1, d2], 5, 40, 300)

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
