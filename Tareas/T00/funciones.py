import clases


def apodo_valido(apodo):  # revisa el apodo, retorna un booleando
    if len(apodo) >= 5 and apodo.isalnum():
        return(True)
    else:
        return(False)


def disparo_valido(partida, x, y):
    if type(x) == int and type(y) == int:
        if 0 <= x < partida.dimensiones[0] and 0 <= y < partida.dimensiones[1]:
            return True
    return False

