import funciones as func
from clases import Partida
import tablero
import parametros


def menu_juego(partida):
    bomba_especial_utilizada = False
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:
        print("--- Menu Juego ---")
        tablero.print_tablero(partida.tablero_rival, partida.tablero_propio, utf8=True)
        print("[0] Rendirse")
        print("[1] Lanzar una bomba")
        print("[2] Salir del programa")
        entrada_usuario = input("Ingresa tu eleccion: ")
        if entrada_usuario == "0":  # Rendirse
            print("Te has rendido")
            puntaje = partida.calcular_puntaje()
            print(f"Tu puntaje fue de {partida.puntaje} puntos")
            partida.guardar_puntaje("puntajes.txt")
            break  # por hacer guardar datos al rendirse en archivo
        elif entrada_usuario == "1":  # Lanzar bomba
            apunto = func.lanzar_bomba(partida)
        elif entrada_usuario == "2":
            print("Saliendo...")
            salir = True
            return(salir)
            # por hacer terminar codigo para salir del programa de una
            break
        else:
            print("Entrada Invalida! Ingresa una opcion valida")
            continue

        # Turno Oponente
        if not(apunto):
            oponente_apunto = True
            while oponente_apunto and (partida.aliados_descubiertos < parametros.NUM_BARCOS):
                oponente_apunto = func.ataque_oponente(partida)
                print("El tablero actual es:")
                tablero.print_tablero(partida.tablero_rival, partida.tablero_propio)
                input("Presione enter para continuar: ")

        #Chequea ganador
        partida.ver_si_gano()
        if partida.terminada:
            print(f"Ha ganado {partida.ganador}!")
            partida.calcular_puntaje()
            print(f"Has conseguido {partida.puntaje} puntos!")
            print("Tablero final:")
            tablero.print_tablero(partida.tablero_rival, partida.tablero_propio)
            partida.guardar_puntaje("puntajes.txt")
            break
    salir = False
    return salir


def menu_rankings(path):
    # manejo del archivo
    archivo = open(path, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()
    datos = []
    for linea in lineas:
        if "\n" in linea:
            linea = linea[:-1]
        dato = linea.split(",")
        dato = [dato[0], int(dato[1])]
        datos.append(dato)
    datos = sorted(datos, key=lambda dato: dato[1], reverse=True)
    # UI Rankings
    while True:
        print("--- Ranking de Puntajes ---")
        lugar = 1
        for dato in datos:
            nombre = dato[0]
            puntaje = dato[1]
            print(f"{lugar}) {nombre}: {puntaje} Pts")
            if len(datos) >= 5 and lugar == 5:
                break
            lugar += 1
        print("[0] Volver")
        # Entrada del usuario
        entrada_usuario = input("Indique su opcion (0): ")
        print("-" * 20)

        if entrada_usuario == "0":
            break
        else:
            print("Entrada Invalida!, por favor ingrese un valor valido")


# muestra el menu de inicio, y en caso de crearse una partida la retorna como
# un objeto "Partida", o sino solamente termina el ciclo y no retorna nada.
def menu_inicio():
    while True:
        volver = False
        # UI del menu
        print("---Menu de Inicio---")
        print("[0] Iniciar una Partida")
        print("[1] Ver Ranking de Puntajes")
        print("[2] Salir")
        print("-" * 20)

        # Entrada del usuario
        entrada_usuario = input("Indique su opcion (0, 1 o 2): ")

        # Opciones posibles
        if entrada_usuario == "0":  # iniciar partida
            while True:  # Bucle para pedir el apodo
                apodo = input("Ingrese un apodo para su partida: ")
                if func.apodo_valido(apodo):
                    break
                else:
                    while True:
                        print("Apodo Inválido!, Por favor ingrese nuevamente")
                        print("[0] ingresar un nuevo apodo")
                        print("[1] volver al menu de inicio")
                        entrada = input("Escoja una opcion: ")
                        if entrada == "0":
                            volver = False
                            break
                        elif entrada == "1":
                            volver = True
                            break
                    if volver:
                        break

            if volver:
                continue
            while True:
                print("Las filas y columnas deben tener un tamaño entre 3 y 15")
                filas = input("Ingrese el numero de filas: ")
                columnas = input("Ingrese el numero de columnas: ")

                if filas.isnumeric() and columnas.isnumeric():
                    filas = int(filas)
                    columnas = int(columnas)
                    if (3 <= filas <= 15) and (3 <= columnas <= 15):
                        break
                print("Entrada invalida,\
 vuelva a señalar las dimensiones del tablero")
            partida = Partida(apodo, filas, columnas)

            # pasa al menu Juego
            salir = menu_juego(partida)
            if salir:
                break
        elif entrada_usuario == "1":  # ver rankings
            menu_rankings("puntajes.txt")
        elif entrada_usuario == "2":  # salir
            print("Hasta Luego, Gracias por jugar DCCombateNaval")
            break
        else:
            print("Entrada Invalida!, por favor ingrese un valor valido")
