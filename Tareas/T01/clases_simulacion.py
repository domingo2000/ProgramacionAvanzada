from abc import ABC, abstractmethod


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

    @excelencia.setter
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

    def fichar_deportista(self):
        pass

    def entrenar_deportista(self):
        pass

    def sanar_lesiones(self):
        pass

    def comprar_tecnología(self):
        pass

    @abstractmethod
    def utilizar_habilidad_especial(self):
        pass


class IEEEsparta(Delegacion):
    def __init__(self, entrenador, equipo, medallas, moral, dinero):
        super().__init__(entrenador, equipo, medallas, moral, dinero)
        self.excelencia_y_respeto
