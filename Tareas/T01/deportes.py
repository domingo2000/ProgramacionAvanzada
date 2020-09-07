from abc import ABC, abstractmethod


class Deporte(ABC):
    """
    DOCUMENTACION
    """
    def __init__(self, implemento, riego):
        self.implemento = implemento
        self.riesgo = riesgo

    def validez_de_competencia(self):
        pass

    @abstractmethod
    def calcular_ganador(self):
        pass


class Atletismo(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(False, 0.2)

    def calcular_ganador(self):
        pass


class Ciclismo(Deporte):
    """
    DOCUMENTACION
    """
    def __init__(self):
        super().__init__(True, 0.35)

    def calcular_ganador(self):
        pass


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
