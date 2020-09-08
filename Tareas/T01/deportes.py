from abc import ABC, abstractmethod
import parametros as p


class Deporte(ABC):
    """
    DOCUMENTACION
    """
    def __init__(self, implemento, riesgo):
        self.implemento = implemento
        self.nombre = None
        self.__riesgo = riesgo

    @property
    def riesgo(self):
        return(self.__riesgo)

    @riesgo.setter
    def riesgo(self, riesgo):
        if riesgo < p.RIESGO_MINIMO:
            self.__riesgo = p.RIESGO_MINIMO
        elif riesgo > p.RIESGO_MAXIMO:
            self.__riesgo = p.RIESGO_MAXIMO
        else:
            self.__riesgo = riesgo

    def validez_de_competencia(self, competidores, delegacion1, delegacion2):
        """ 
        Competidores es una lista [competidor_propio, competidor_rival] de los competidores
        que participan en la competencia
        """
        if len(competidores) < 2:
            print("No hay suficientes competidores para realizar la competencia!")
            return False
        for competidor in competidores:
            if competidor.lesionado:
                print(f"El competidor {competidor.nombre} se encuentra lesionado")
                return False

        if self.implemento:
            if delegacion1.implementos_deportivos < p.NIVEL_IMPLEMENTOS or \
               delegacion2.implementos_deportivos < p.NIVEL_IMPLEMENTOS:
                print("No se cumplen los implementos necesarios para la competencia")
                return False
            else:
                return True
        else:
            return True

    @abstractmethod
    def calcular_ganador(self, competidor1, competidor2):
        pass


class Atletismo(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(False, p.RIESGO_ATLETISMO)
        self.nombre = "atletismo"

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (p.PONDERADOR_VELOCIDAD_ATLETISMO * competidor1.velocidad
                                 + p.PONDERADOR_RESISTENCIA_ATLETISMO * competidor1.resistencia
                                 + p.PONDERADOR_MORAL_ATLETISMO * competidor1.moral)
        puntaje1 = max(p.PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (p.PONDERADOR_VELOCIDAD_ATLETISMO * competidor2.velocidad
                                 + p.PONDERADOR_RESISTENCIA_ATLETISMO * competidor2.resistencia
                                 + p.PONDERADOR_MORAL_ATLETISMO * competidor2.moral)
        puntaje2 = max(p.PUNTAJE_MINIMO, ponderado_cualidades2)
        if puntaje1 > puntaje2:
            print(f"Ha ganado {competidor1.nombre}")
            return competidor1
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            return competidor2
        else:
            print("Se ha producido un empate!")
            retrun("empate")


class Ciclismo(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(True, p.RIESGO_CICLISMO)
        self.nombre = "ciclismo"

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (p.PONDERADOR_VELOCIDAD_CICLISMO * competidor1.velocidad
                                 + p.PONDERADOR_RESISTENCIA_CICLISMO * competidor1.resistencia
                                 + p.PONDERADOR_FLEXIBILIDAD_CICLISMO * competidor1.flexibilidad)
        puntaje1 = max(p.PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (p.PONDERADOR_VELOCIDAD_CICLISMO * competidor2.velocidad
                                 + p.PONDERADOR_RESISTENCIA_CICLISMO * competidor2.resistencia
                                 + p.PONDERADOR_FLEXIBILIDAD_CICLISMO * competidor2.flexibilidad)
        puntaje2 = max(p.PUNTAJE_MINIMO, ponderado_cualidades2)
        if puntaje1 > puntaje2:
            print(f"Ha ganado {competidor1.nombre}")
            return competidor1
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            return competidor2
        else:
            print("Se ha producido un empate!")
            retrun("empate")


class Gimnacia(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(True, p.RIESGO_GIMNACIA)
        self.nombre = "gimnacia"

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (p.PONDERADOR_FLEXIBILIDAD_GIMNACIA * competidor1.flexibilidad
                                 + p.PONDERADOR_RESISTENCIA_GIMNACIA * competidor1.resistencia
                                 + p.PONDERADOR_MORAL_GIMNACIA * competidor1.moral)
        puntaje1 = max(p.PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (p.PONDERADOR_FLEXIBILIDAD_GIMNACIA * competidor2.flexibilidad
                                 + p.PONDERADOR_RESISTENCIA_GIMNACIA * competidor2.resistencia
                                 + p.PONDERADOR_MORAL_GIMNACIA * competidor2.moral)
        puntaje2 = max(p.PUNTAJE_MINIMO, ponderado_cualidades2)
        if puntaje1 > puntaje2:
            print(f"Ha ganado {competidor1.nombre}")
            return competidor1
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            return competidor2
        else:
            print("Se ha producido un empate!")
            retrun("empate")


class Natacion(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(False, 0.3)
        self.nombre = "natacion"

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (p.PONDERADOR_VELOCIDAD_NATACION * competidor1.velocidad
                                 + p.PONDERADOR_RESISTENCIA_NATACION * competidor1.resistencia
                                 + p.PONDERADOR_FLEXIBILIDAD_NATACION * competidor1.flexibilidad)
        puntaje1 = max(p.PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (p.PONDERADOR_VELOCIDAD_NATACION * competidor2.velocidad
                                 + p.PONDERADOR_RESISTENCIA_NATACION * competidor2.resistencia
                                 + p.PONDERADOR_FLEXIBILIDAD_NATACION * competidor2.flexibilidad)
        puntaje2 = max(p.PUNTAJE_MINIMO, ponderado_cualidades2)
        if puntaje1 > puntaje2:
            print(f"Ha ganado {competidor1.nombre}")
            return competidor1
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            return competidor2
        else:
            print("Se ha producido un empate!")
            retrun("empate")
