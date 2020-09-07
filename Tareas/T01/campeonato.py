import parametros as p


class Campeonato:
    """
    DOCUMENTACION
    """
    def __init__(self, diccionario_medallero, delegacion1, delegacion2, lista_deportes, lista_menu):
        self.dia_actual = p.DIA_ACTUAL_INICIAL
        self.medallero = diccionario_medallero
        self.delegacion1 = delegacion1
        self.delegacion2 = delegacion2
        self.deportes = lista_deportes
        self.menus = lista_menu

    def realizar_competencias_del_dia(self):
        pass

    def premiar(self):
        pass

    def calcular_nivel_moral_delegaciones(self):
        pass

    def mostrar_estado(self):
        pass
