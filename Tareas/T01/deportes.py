from abc import ABC, abstractmethod
from parametros impor NIVEL_IMPLEMENTOS, PUNTAJE_MINIMO


class Deporte(ABC):
    """
    DOCUMENTACION
    """
    def __init__(self, implemento, riego):
        self.implemento = implemento
        self.riesgo = riesgo

    def validez_de_competencia(self, competidores, delegacion1, delegacion2):
        if len(competidores < 2):
            print("No hay suficientes competidores para realizar la competencia!")
            return False
        for competidor in competidores:
            if competidor.lesionado:
                print(f"El competidor {competidor.nombre} se encuentra lesionado")
                return False

        if self.implemento:
            if delegacion1.implementos_deportivos < NIVEL_IMPLEMENTOS and \
                delegacion2.implementos_deportivos < NIVEL_IMPLEMENTOS:
                return True
            else:
                return False
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
        super().__init__(False, 0.2)

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (0.55 * competidor1.velocidad
                                 + 0.2 * competidor1.resistencia
                                 + 0.25 * competidor1.moral)
        puntaje1 = max(PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (0.55 * competidor2.velocidad
                                 + 0.2 * competidor2.resistencia
                                 + 0.25 * competidor2.moral)
        puntaje2 = max(PUNTAJE_MINIMO, ponderado_cualidades2)
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
        super().__init__(True, 0.35)

    def calcular_ganador(self, competidor1, competidor2):
        ponderado_cualidades1 = (0.47 * competidor1.velocidad
                                 + 0.36 * competidor1.resistencia
                                 + 0.17 * competidor1.moral)
        puntaje1 = max(PUNTAJE_MINIMO, ponderado_cualidades1)
        ponderado_cualidades2 = (0.55 * competidor2.velocidad
                                 + 0.2 * competidor2.resistencia
                                 + 0.25 * competidor2.moral)
        puntaje2 = max(PUNTAJE_MINIMO, ponderado_cualidades2)
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
        super().__init__(True, 0.3)

    def calcular_ganador(self):
        pass


class Natacion(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(False, 0.3)

    def calcular_ganador(self):
        pass
