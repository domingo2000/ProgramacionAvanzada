import funciones as func
from clases import Partida


def menu_juego(partida):
    pass


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
