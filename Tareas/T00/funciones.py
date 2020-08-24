import clases
from parametros import RADIO_EXP
import random


def apodo_valido(apodo):  # revisa el apodo, retorna un booleando
    if len(apodo) >= 5 and apodo.isalnum():
        return(True)
    else:
        return(False)


# Valida si los string de coordenadas son validos, es decir, la entrada
# es valida, y la coordenada pertenece al mapa
def coordenadas_validas(partida, letra, num):
    letras_tablero = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(letra) == 1 and letra.isalpha():  # valida la primera coordenada
        letra = letra.upper()
        y = letras_tablero.index(letra)
        if 0 <= y < partida.dimensiones[1]:
            letra_valida = True
        else:
            letra_valida = False
    else:
        letra_valida = False
    if num.isnumeric():  # valida la segunda coordenada
        x = int(num)
        if 0 <= x < partida.dimensiones[0]:
            num_valido = True
        else:
            num_valido = False
    else:
        num_valido = False

    if letra_valida and num_valido:
        return True
    else:
        return False


# Elimina las coordenadas que estan fuera del mapa al explotar una bomba
def coordenadas_en_mapa(partida, coordenadas):
    coordenadas_mapa = set()
    for coordenada in coordenadas:
        x = coordenada[0]
        y = coordenada[1]
        if 0 <= x < partida.dimensiones[0] and 0 <= y < partida.dimensiones[1]:
            coordenadas_mapa.add((x, y))
    return coordenadas_mapa


def coordenadas_bomba_cruz(partida, x, y):
    print("BOOM cruz")
    coordenadas_explosion = set()
    for i in range(RADIO_EXP):
        coordenadas_explosion.add(((x - i), y))
        coordenadas_explosion.add(((x + i), y))
        coordenadas_explosion.add((x, (y - i)))
        coordenadas_explosion.add((x, (y + i)))

    coordenadas_explosion = coordenadas_en_mapa(partida, coordenadas_explosion)
    return(coordenadas_explosion)


def coordenadas_bomba_x(partida, x, y):
    coordenadas_explosion = set()
    for i in range(RADIO_EXP):
        coordenadas_explosion.add(((x + i), (y + i)))
        coordenadas_explosion.add(((x + i), (y - i)))
        coordenadas_explosion.add(((x - i), (y - i)))
        coordenadas_explosion.add(((x - i), (y + i)))
    print("BOOM X bomb")
    coordenadas_explosion = coordenadas_en_mapa(partida, coordenadas_explosion)
    return(coordenadas_explosion)


def coordenadas_bomba_diamante(partida, x, y):
    print("BOOM diamante")


def atacar_coordenadas(partida, coordenadas):
    apunto = False
    for coordenada in coordenadas:
        x = coordenada[0]
        y = coordenada[1]
        casilla_atacada = partida.tablero_rival[x][y]
        if casilla_atacada == "B":
            partida.tablero_rival[x][y] = "F"
            partida.enemigos_descubiertos += 1
            apunto = True
        elif casilla_atacada == " ":
            partida.tablero_rival[x][y] = "X"
        elif casilla_atacada == "F" or casilla_atacada == "X":
            continue
    return apunto


# Lanza una bomba y cambia el tablero segun la bomba y las coordenadas,
# retorna si le apunto (True) o si no le apunto (False)
def lanzar_bomba(partida):
    letras_tablero = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:  # Bucle input tipo de bomba
        print("Seleccione el tipo de bomba")
        print("[0] Regular")
        print("[1] Especial")
        entrada = input("Ingrese un valor para la bomba: ")

        if entrada == "0":  # Regular
            while True:  # Bucle input coordenadas
                print("Indique la casilla donde va a atacar")
                coordenada_letra = input("Ingrese la coordenada letra: ")
                coordenada_num = input("Ingrese la coordenada numerica: ")

                if coordenadas_validas(partida, coordenada_letra, coordenada_num):
                    coordenada_letra = coordenada_letra.upper()
                    x = int(coordenada_num)
                    y = letras_tablero.index(coordenada_letra)
                    casilla_atacada = partida.tablero_rival[x][y]
                    if casilla_atacada == " ":
                        partida.tablero_rival[x][y] = "X"
                        return False
                    elif casilla_atacada == "B":
                        partida.tablero_rival[x][y] = "F"
                        partida.enemigos_descubiertos += 1
                        return True
                    elif casilla_atacada == "X" or casilla_atacada == "F":
                        print("Ya a atacado esa casilla, ingrese otra casilla")
                else:  # coordenadas invalidas
                    print("Coordenadas Invalidas!, ingrese nuevamente")
            break
        elif entrada == "1":  # Especial
            if partida.bomba_especial_usada:
                print("Usted ya jugo la bomba especial, elija la regular")
            else:  # se prosigue a jugar la bomba especial
                while True:  # bucle input tipo bomba
                    print("Indique que tipo de bomba quiere lanzar")
                    print("[0] Cruz")
                    print("[1] X Bomb")
                    print("[2] Diamante")

                    entrada = input("Ingrese un valor para el tipo de bomba: ")

                    while True:  # Bucle input coordenadas
                        print("Indique la casilla donde va a atacar")
                        coordenada_letra = input("Ingrese la coordenada letra: ")
                        coordenada_num = input("Ingrese la coordenada numerica: ")

                        if coordenadas_validas(partida, coordenada_letra, coordenada_num):
                            coordenada_letra = coordenada_letra.upper()
                            x = int(coordenada_num)
                            y = letras_tablero.index(coordenada_letra)
                            casilla_atacada = partida.tablero_rival[x][y]
                            if casilla_atacada == "X" or casilla_atacada == "F":
                                print("Ya a atacado esa casilla, ingrese otra casilla")
                            elif casilla_atacada == " " or casilla_atacada == "B":
                                break

                        else:  # coordenadas invalidas
                            print("Coordenadas Invalidas!, ingrese nuevamente")

                    if entrada == "0":  # bomba cruz
                        coordenadas_atacadas = coordenadas_bomba_cruz(partida, x, y)
                        apunto = atacar_coordenadas(partida, coordenadas_atacadas)
                        partida.bomba_especial_usada = True
                        if apunto:
                            return True
                        else:
                            return False
                    elif entrada == "1":  # bomba X
                        coordenadas_atacadas = coordenadas_bomba_x(partida, x, y)
                        apunto = atacar_coordenadas(partida, coordenadas_atacadas)
                        partida.bomba_especial_usada = True
                        if apunto == True:
                            return True
                        else:
                            return False
                    elif entrada == "2":  # bomba diamante
                        coordenadas_atacadas = coordenadas_bomba_diamante(partida, x, y)
                        apunto = atacar_coordenadas(partida, coordenadas_atacadas)
                        partida.bomba_especial_usada = True
                        if apunto == True:
                            return True
                        else:
                            return False
                    else:  # entrada invalida
                        print("Entrada Invalida! Ingresa una opcion valida")
                        continue
        else:  # entrada Invalida
            print("Entrada Invalida! Ingresa una opcion valida")
            continue

    pass


# Ataca una coordenada aleatoria que no haya sido atacada previamente
def ataque_oponente(partida):
    oponente_apunto = False
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    coordenada_valida = False
    while not(coordenada_valida):
        x = random.randint(0, partida.dimensiones[0] - 1)
        y = random.randint(0, partida.dimensiones[1] - 1)
        print("debug")
        casilla_atacada = partida.tablero_propio[x][y]
        if casilla_atacada == " ":
            partida.tablero_propio[x][y] = "X"
            coordenada_valida = True
        elif casilla_atacada == "B":
            partida.tablero_propio[x][y] = "F"
            partida.aliados_descubiertos += 1
            coordenada_valida = True
            oponente_apunto = True
        else:
            coordenada_valida = False
    letra = letras[y]
    print(f"¡Tu oponente ha disparado a la coordenada {letra}{x}!")
    return(oponente_apunto)