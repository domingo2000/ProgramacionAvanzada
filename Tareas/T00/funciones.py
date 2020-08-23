import clases


def apodo_valido(apodo):  # revisa el apodo, retorna un booleando
    if len(apodo) >= 5 and apodo.isalnum():
        return(True)
    else:
        return(False)


def mi_funcion():
    a = input("Ingresa un numero: ")
    print(a)
