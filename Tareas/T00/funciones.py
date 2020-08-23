import clases


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


# Lanza una bomba y cambia el tablero segun la bomba y las coordenadas
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
                        break
                    elif casilla_atacada == "B":
                        partida.tablero_rival[x][y] = "F"
                        break
                    elif casilla_atacada == "X" or casilla_atacada == "F":
                        print("Ya a atacado esa casilla, ingrese otra casilla")
                else:  # coordenadas invalidas
                    print("Coordenadas Invalidas!, ingrese nuevamente")
            break
        elif entrada == "1":  # Especial
            break
        else:  # Invalida
            continue

    pass