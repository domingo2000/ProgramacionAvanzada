import funciones as func
from clases import Partida
import tablero


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
        if entrada_usuario == "0":
            print("Te has rendido")
            break  # por hacer guardar datos al rendirse en archivo
        elif entrada_usuario == "1":
            # Lanzar una bomba
            print("Seleccione el tipo de bomba")
            print("[0] Regular")
            print("[1] Especial")
            tipo_bomba = input("Ingrese un valor para la bomba: ")

            if tipo_bomba == "0":  # bombas regulares
                while True:
                    print("Indique la casilla donde va a atacar")
                    coordenada_letra = input("Ingrese la coordenada letra: ")
                    coordenada_num = input("Ingrese la coordenada numerica: ")
                    if coordenada_num.isnumeric():
                        x = int(coordenada_num)
                    else:
                        x = coordenada_num
                    if len(coordenada_letra) == 1 and coordenada_letra in letras:
                        y = letras.index(coordenada_letra)
                    else:
                        y = coordenada_letra

                    if not(func.disparo_valido(partida, x, y)):
                        print("Disparo no valido, ingrese coordenadas validas")
                    else:
                        break
                # sigue con el bucle y se dispara
                print(f"Ha disparado a la cordenada \
    {coordenada_letra}, {coordenada_num}")
                valor_casilla_rival = partida.tablero_rival[x][y] 
                if valor_casilla_rival == "B":
                    partida.tablero_rival[x][y] = "F"
                elif valor_casilla_rival == " ":
                    partida.tablero_rival[x][y] = "X"
            elif tipo_bomba == "1":  # bombas especiales
                if not(bomba_especial_utilizada):
                    pass
                    # por hacer programar tipos de bomba e implementar aqui
                elif bomba_especial_utilizada:
                    print("Usted ya jugo una bomba especial, elija la regular")
                pass
            else:
                print("Entrada invalida, ingrese un valor valido")

            pass
        elif entrada_usuario == "2":
            # por hacer terminar codigo para salir del programa de una
            break
            pass
        else:
            print("Entrada Invalida! Ingresa una opcion valida")


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
        datos.append(dato)

    # UI Rankings
    while True:
        print("--- Ranking de Puntajes ---")
        lugar = 1
        for dato in datos:
            nombre = dato[0]
            puntaje = dato[1]
            print(f"{lugar}) {nombre}: {puntaje} Pts")
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
                    print("Apodo Inválido!, Por favor ingrese nuevamente")

            while True:
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
            menu_juego(partida)

        elif entrada_usuario == "1":  # ver rankings
            menu_rankings("puntajes.txt")
            pass
        elif entrada_usuario == "2":  # salir
            print("Hasta Luego, Gracias por jugar DCCombateNaval")
            break
            pass
        else:
            print("Entrada Invalida!, por favor ingrese un valor valido")
