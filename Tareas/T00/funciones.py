import clases


def apodo_valido(apodo):  # revisa el apodo, retorna un booleando
    if len(apodo) >= 5 and apodo.isalnum():
        return(True)
    else:
        return(False)


def crear_partida(apodo, filas, columnas):
    print("Partida creada!")
    print(f"Partida de {apodo}")
    print(f"El tablero tiene tamaño [{filas} x {columnas}]")

    return(clases.Partida(apodo, filas, columnas))
