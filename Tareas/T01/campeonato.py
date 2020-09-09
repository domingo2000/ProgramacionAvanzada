import parametros as p
import random
import imagenes_string
import sys
import lectura_datos
from beautifultable import BeautifulTable


class Campeonato:
    """
    DOCUMENTACION
    """
    def __init__(self, delegacion1, delegacion2, lista_deportistas_no_fichados, lista_deportes):
        self.dia_actual = p.DIA_ACTUAL_INICIAL
        self.medallero = {f"{delegacion1.nombre}": 0,
                          f"{delegacion2.nombre}": 0}
        self.delegacion1 = delegacion1
        self.delegacion2 = delegacion2
        self.deportistas_no_fichados = lista_deportistas_no_fichados
        self.deportes = lista_deportes

    def realizar_competencias_del_dia(self):
        # diccionarios {"nombre_competencia" : Deportista}
        deportistas_competencia = dict()
        deportistas_competencia_rival = dict()
        equipo_propio = self.delegacion1.equipo
        equipo_rival = self.delegacion2.equipo
        resultados_dia = []
        for deporte in self.deportes:
            # selecciona un deportista del equipo
            while True:
                print(f"Selecciona un competidor para que participe en {deporte.nombre}")
                i = 0
                for deportista in equipo_propio:
                    print(f"[{i}] {deportista.nombre}")
                    i += 1
                entrada = input("selecciona una opción: ")
                if entrada.isdigit():
                    entrada = int(entrada)
                    if 0 <= entrada < len(equipo_propio):
                        deportista_seleccionado = equipo_propio[entrada]
                        print(f"Has escogido a {deportista_seleccionado.nombre}")
                        deportistas_competencia[f"{deporte.nombre}"] = deportista_seleccionado
                        break
            # Selecciona un deportista rival aleatorio
            deportista_seleccionado_rival = random.choice(equipo_rival)
            print(f"{self.delegacion2.entrenador} ha elegido a "
                  f"{deportista_seleccionado_rival.nombre} para competir\n")

            deportistas_competencia_rival[f"{deporte.nombre}"] = deportista_seleccionado_rival

        for deporte in self.deportes:
            # competidores validar_competencia = [[delegacion1, competidor1],
            #                                     [delegacion2, compeidor2]]
            resultados_competencia = [deporte.nombre, [], []]
            deportistas = [deportistas_competencia[deporte.nombre],
                           deportistas_competencia_rival[deporte.nombre]]
            competidores = [[self.delegacion1, deportistas[0]],
                            [self.delegacion2, deportistas[1]]]

            # Verifica la validez del resultado de la competencia
            # si es invalida setea resultador_validez, si no calcula puntajes
            resultados_validez = deporte.validez_de_competencia(competidores)
            if resultados_validez == "empate":
                resultados_competencia = resultados_validez
                resultados_dia.append(resultados_competencia)
                continue
            # Opcion de que la competencia es invalida
            elif resultados_validez != True:
                resultados_competencia = resultados_validez
            # calcula puntajes y setea resultados_competencia
            elif resultados_validez:
                # calcular ganador para cada competencia
                resultados_competencia = deporte.calcular_ganador(competidores)
                # hace que los deportistas se lesionen segun la probabilidad de lesion
                for deportista in deportistas:
                    deportista.lesionarse(deporte.riesgo)
            if resultados_competencia == "empate":
                resultados_dia.append(resultados_competencia)
                continue
            else:
                resultados_competencia = [deporte.nombre,
                                          resultados_competencia["ganador"],
                                          resultados_competencia["perdedor"]]
            self.premiar_deportistas_y_delegaciones(resultados_competencia)
            resultados_dia.append(resultados_competencia)
            print("\n")
        lectura_datos.escribir_resultados_dia("resultados.txt", resultados_dia, self.dia_actual)

    def premiar_deportistas_y_delegaciones(self, resultados_competencia):
        # resultados competencia debe ser un lista:
        # [nombre_deporte, [delegacion_ganadora, deportista_ganador],
        #                  [delegacion_perdedora, deportista perdedor]]
        nombre_deporte = resultados_competencia[0]
        delegacion_ganadora = resultados_competencia[1][0]
        delegacion_perdedora = resultados_competencia[2][0]
        deportista_ganador = resultados_competencia[1][1]
        deportista_perdedor = resultados_competencia[2][1]

        print(f"Felicitaciones delegacion {delegacion_ganadora.nombre} has ganado la competencia "
              f"de {nombre_deporte}! con el competidor {deportista_ganador.nombre}")

        delegacion_ganadora.medallas += 1
        delegacion_ganadora.dinero += p.DINERO_GANADO_POR_COMPETENCIA
        print(f"La delegacion {delegacion_ganadora.nombre} ha recibido una medalla de Oro!")
        imagenes_string.imprimir_medalla(delegacion_ganadora.nombre)
        print(f"La delegacion {delegacion_ganadora.nombre} ha recibido "
              f"{p.DINERO_GANADO_POR_COMPETENCIA} DCCoins")

        deportista_ganador.moral += p.BONIFICACION_MORAL_COMPETENCIA
        deportista_perdedor.moral -= p.PENALIZACION_MORAL_COMPETENCIA
        delegacion_perdedora.excelencia_y_respeto -= p.BONIFICACION_EXCELENCIA_COMPETENCIA
        print(f"{deportista_perdedor.nombre} se siente horrible porque perdió la competencia")
        print(f"La delegacion {delegacion_perdedora.nombre} se siente deshonrada por su derrota")

        print(f"Ha finalizado la premiacion de {nombre_deporte}")

    def calcular_nivel_moral_delegaciones(self):
        print("Calculando moral...")
        suma_moral_delegacion1 = 0
        suma_moral_delegacion2 = 0
        for deportista in self.delegacion1.equipo:
            suma_moral_delegacion1 += deportista.moral
        for deportista in self.delegacion2.equipo:
            suma_moral_delegacion2 += deportista.moral

        promedio_moral_delegacion1 = suma_moral_delegacion1 / len(self.delegacion1.equipo)
        promedio_moral_delegacion2 = suma_moral_delegacion2 / len(self.delegacion2.equipo)

        self.delegacion1.moral = promedio_moral_delegacion1
        self.delegacion2.moral = promedio_moral_delegacion2
        print(f"La moral de la delegacion {self.delegacion1.nombre} es: {self.delegacion1.moral}")
        print(f"La moral de la delegacion {self.delegacion2.nombre} es: {self.delegacion2.moral}")

    def mostrar_estado(self):
        string = "ESTADO DE LAS DELEGACIONES Y DEPORTISTAS"
        print(f"{string: ^72}")
        # Info delegacion 1 
        tabla.append_row

    def calcular_ganador(self):
        empate = False
        if self.delegacion1.medallas > self.delegacion2.medallas:
            ganador_cumbre = self.delegacion1
            perdedor_cumbre = self.delegacion2
        elif self.delegacion2.medallas > self.delegacion1.medallas:
            ganador_cumbre = self.delegacion2
            perdedor_cumbre = self.delegacion1
        elif self.delegacion1.medallas == self.delegacion2.medallas:
            empate = True
            print("Se ha producido un empate!")
            print(f"{self.delegacion1.nombre} Consiguió {self.delegacion1.medallas} medallas!!")
            print(f"{self.delegacion2.nombre} Consiguió {self.delegacion2.medallas} medallas!!")
            print("AMBAS DELEGACIONES HAN CONSEGUIDO EL HONOR Y LA GLORA!")
            imagenes_string.imprimir_copa(self.delegacion1.nombre)
            imagenes_string.imprimir_copa(self.delegacion2.nombre)
        else:
            print("ERROR no deberia printear esto")

        if not empate:
            print(f"{ganador_cumbre.nombre} ha ganado la DCCumbre!")
            print(f"{ganador_cumbre.nombre} Consiguió {ganador_cumbre.medallas} medallas!!")
            print(f"{perdedor_cumbre.nombre} Consiguió {perdedor_cumbre.medallas} medallas!!")
            print(f"\n El entrenador {ganador_cumbre.entrenador} Se siente muy orgulloso "
                  f"por haber ganado la DCCumbre")
            imagenes_string.imprimir_copa(ganador_cumbre.nombre)

        while True:
            print("Que desea hacer:\n")
            print("[0] Realizar nueva simulacion")
            print("[1] Salir del programa")
            entrada = input("Ingrese una opcion: ")
            if entrada == "0":
                break
            elif entrada == "1":
                sys.exit()
                break
            else:
                print("Entrada Inválida! ingrese otra opcion")


if __name__ == "__main__":
    from clases_simulacion import Deportista, IEEEsparta, DCCrotona
    from deportes import Atletismo, Ciclismo, Gimnacia, Natacion
    import lectura_datos as csv

    datos_deportistas = csv.leer_datos_deportistas("deportistas.csv")

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

    atletismo = Atletismo()
    ciclismo = Ciclismo()
    gimnacia = Gimnacia()
    natacion = Natacion()

    lista_deportes = [atletismo, ciclismo, gimnacia, natacion]
    equipo1 = []
    equipo2 = []
    for i in range (6):
        deportista = random.choice(lista_deportistas)
        lista_deportistas.remove(deportista)
        equipo1.append(deportista)
        deportista = random.choice(lista_deportistas)
        lista_deportistas.remove(deportista)
        equipo2.append(deportista)

    delegacion1 = IEEEsparta("Luchito", equipo1, 0, 35, 500)
    delegacion2 = DCCrotona("Pancho", equipo2, 0, 54.7, 350)
    campeonato = Campeonato(delegacion1, delegacion2,
                            lista_deportistas, lista_deportes)
    print("Testeo")
