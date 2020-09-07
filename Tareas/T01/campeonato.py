import parametros as p


class Campeonato:
    """
    DOCUMENTACION
    """
    def __init__(self, delegacion1, delegacion2, lista_deportes, lista_menu):
        self.dia_actual = p.DIA_ACTUAL_INICIAL
        self.medallero = {f"{delegacion1.nombre}": 0,
                          f"{delegacion2.nombre}": 0}
        self.delegacion1 = delegacion1
        self.delegacion2 = delegacion2
        self.deportes = lista_deportes
        self.menus = lista_menu

    def realizar_competencias_del_dia(self):
        for deporte in self.deportes:
            pass

    def premiar_deportistas_y_delegaciones(self, resultados_competencia):
        # resultados competencia debe ser un lista:
        # [nombre_deporte, [delegacion_ganadora, deportista_ganador],
        #                  [delegacion_perdedora, deportista perdedor]]
        nombre_deporte = resultados_competencia[0]
        delegacion_ganadora = resultados_competencia[1][0]
        delegacion_perdedora = resultados_competencia[2][0]
        deportista_ganador = resultados_competencia[1][1]
        deportista_perdedor = resultados_competencia[2][0]

        print(f"Felicitaciones delegacion {delegacion_ganadora.nombre} has ganado la competencia \
de {nombre_deporte}! con el competidor {deportista_ganador.nombre}")

        delegacion_ganadora.medallas += 1
        delegacion_ganadora.dinero += p.DINERO_GANADO_POR_COMPETENCIA
        print(f"La delegacion {delegacion_ganadora.nombre} ha recibido una medalla de Oro!")
        print(f"La delegacion {delegacion_ganadora.nombre} ha recibido \
{p.DINERO_GANADO_POR_COMPETENCIA}")

        deportista_ganador.moral += p.BONIFICACION_MORAL_COMPETENCIA
        deportista.perdedor -= p.PENALIZACION_MORAL_COMPETENCIA
        delegacion_perdedora.excelencia_y_respeto -= p.BONIFICACION_EXCELENCIA_COMPETENCIA
        print(f"Por otro lado {deportista.nombre} se siente horrible porque perdió la competencia")
        print(f"La delegacion {delegacion_perdedora} se siente deshonrada por su derrotaS")

        print(f"Ha finalizado la premiacion de {nombre_deporte}")

    def calcular_nivel_moral_delegaciones(self):
        print("Calculando moral...")
        suma_moral_delegacion1 = 0
        suma_moral_delegacion2 = 0
        for deportista in self.delegacion1.equipo:
            suma_moral_delegacion1 += deportista.moral
        for deportista in self.delegacion2.equipo:
            suma_moral_delegacion2 += deportista.moral

        promedio_moral_delegacion1 = suma_moral_delegacion1 / len(self.elegacion1.equipo)
        promedio_moral_delegacion2 = suma_moral_delegacion2 / len(self.delegacion2.equipo)

        delegacion1.moral = promedio_moral_delegacion1
        delegacion2.moral = promedio_moral_delegacion2
        print(f"La moral de la delegacion {self.delegacion1.nombre} es: {self.delegacion1.moral}")
        print(f"La moral de la delegacion {self.delegacion2.nombre} es: {self.delegacion2.moral}")

    def mostrar_estado(self):
        pass
