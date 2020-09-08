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

    def validez_de_competencia(self, competidores):
        """
        Competidores es una lista [[delegacion1, competidor1], [delegacion2, compeidor2]]
        de los competidores que participan en la competencia y retorna
        los resultados que son un diccionario
        return {"ganador": [delegacion, deportista], "pededor": [delegacion, deportista]}
        o en caso de que no halla nadie lesionado y se cumplan los implementos retorna True
        """
        # {"ganador": [delegacion, depoertista], "pededor": [delegacion, deportista]}
        resultado_competencia = {"ganador": None, "pededor": None}

        delegacion_propia = competidores[0][0]
        delegacion_rival = competidores[1][0]
        deportista_propio = competidores[0][1]
        deportista_rival = competidores[1][1]

        if deportista_propio.lesionado and deportista_rival.lesionado:
            print("Ambos deportistas se encuentran lesionados!")
            print("¡Se ha producido un empate!")
            return "Empate"
        elif delegacion_propia.implementos_deportivos < p.NIVEL_IMPLEMENTOS and\
                delegacion_rival.implementos_deportivos < p.NIVEL_IMPLEMENTOS:
            print("Ambas delegaciones no cumplen con los implementos!")
            print("¡Se ha producido un empate!")
            return "Empate"
        elif deportista_propio.lesionado:
            print(f"{deportista_propio.nombre} se encuentra lesionado")
            resultado_competencia["ganador"] = [delegacion_rival, deportista_rival]
            resultado_competencia["perdedor"] = [delegacion_propia, deportista_propio]
            return resultado_competencia
        elif deportista_rival.lesionado:
            print(f"{deportista_rival.nombre} se encuentra lesionado")
            resultado_competencia["perdedor"] = [delegacion_rival, deportista_rival]
            resultado_competencia["ganador"] = [delegacion_propia, deportista_propio]
            return resultado_competencia
        elif delegacion_propia.implementos_deportivos < p.NIVEL_IMPLEMENTOS:
            print(f"Delegacion {delegacion_propia.nombre} no cumple con el nivel de implementos"
                    "necesario")
            resultado_competencia["ganador"] = [delegacion_rival, deportista_rival]
            resultado_competencia["perdedor"] = [delegacion_propia, deportista_propio]
            return resultado_competencia
        elif delegacion_rival.implementos_deportivos < p.NIVEL_IMPLEMENTOS:
            print(f"Delegacion {delegacion_rival.nombre} no cumole con el nivel de implementos"
                    "necesario")
            resultado_competencia["perdedor"] = [delegacion_rival, deportista_rival]
            resultado_competencia["ganador"] = [delegacion_propia, deportista_propio]
            return resultado_competencia
        else:
            return True

    @abstractmethod
    def calcular_ganador(self, competidores):
        """
        Competidores es una lista [[delegacion1, competidor1], [delegacion2, compeidor2]]
        de los competidores que participan en la competencia
        """
        pass


class Atletismo(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(False, p.RIESGO_ATLETISMO)
        self.nombre = "atletismo"

    def calcular_ganador(self, competidores):
        """
        Competidores es una lista [[delegacion1, competidor1], [delegacion2, compeidor2]]
        de los competidores que participan en la competencia
        """
        resultado_competencia = {"ganador": None, "pededor": None}
        competidor1 = competidores[0][1]
        competidor2 = competidores[1][1]
        delegacion1 = competidores[1][0]
        delegacion2 = competidores[1][1]

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
            resultado_competencia["ganador"] = [delegacion1, competidor1]
            resultado_competencia["perdedor"] = [delegacion2, competidor2]
            return resultado_competencia
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            resultado_competencia["ganador"] = [delegacion2, competidor2]
            resultado_competencia["perdedor"] = [delegacion1, competidor1]
            return resultado_competencia
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

    def calcular_ganador(self, competidores):
        resultado_competencia = {"ganador": None, "pededor": None}
        competidor1 = competidores[0][1]
        competidor2 = competidores[1][1]
        delegacion1 = competidores[1][0]
        delegacion2 = competidores[1][1]

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
            resultado_competencia["ganador"] = [delegacion1, competidor1]
            resultado_competencia["perdedor"] = [delegacion2, competidor2]
            return resultado_competencia
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            resultado_competencia["ganador"] = [delegacion2, competidor2]
            resultado_competencia["perdedor"] = [delegacion1, competidor1]
            return resultado_competencia
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

    def calcular_ganador(self, competidores):
        resultado_competencia = {"ganador": None, "pededor": None}
        competidor1 = competidores[0][1]
        competidor2 = competidores[1][1]
        delegacion1 = competidores[1][0]
        delegacion2 = competidores[1][1]

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
            resultado_competencia["ganador"] = [delegacion1, competidor1]
            resultado_competencia["perdedor"] = [delegacion2, competidor2]
            return resultado_competencia
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            resultado_competencia["ganador"] = [delegacion2, competidor2]
            resultado_competencia["perdedor"] = [delegacion1, competidor1]
            return resultado_competencia
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

    def calcular_ganador(self, competidores):
        resultado_competencia = {"ganador": None, "pededor": None}
        competidor1 = competidores[0][1]
        competidor2 = competidores[1][1]
        delegacion1 = competidores[1][0]
        delegacion2 = competidores[1][1]

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
            resultado_competencia["ganador"] = [delegacion1, competidor1]
            resultado_competencia["perdedor"] = [delegacion2, competidor2]
            return resultado_competencia
        elif puntaje1 < puntaje2:
            print(f"Ha ganado {competidor2.nombre}")
            return competidor2
        else:
            print("Se ha producido un empate!")
            retrun("empate")
