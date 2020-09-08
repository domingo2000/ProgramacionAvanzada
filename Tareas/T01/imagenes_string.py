def imprimir_copa(nombre):
    """
    original extraido de
    url : https://ascii.co.uk/art/trophy
    """
    if nombre == "IEEEsparta":
        nombre = "IEE"
        l13 = ": ~    IEE    ~ :"
    elif nombre == "DCCrotona":
        nombre = "DCC"
        l13 = ": ~    DCC    ~ :"
    else:
        nombre = "{1}"

    l1 = "             .-=========-."
    l2 = "             \\'-=======-'/"
    l3 = "             _|   .=.   |_"
    l4 = f"            ((|   {nombre}   |)"
    l5 = "             \|    1°    |/"
    l6 = "              \__ '`' __/"
    l7 = "                _`) (`_"
    l8 = "              _/_______\\_"
    l9 = "             /___________\\"

    lineas_copa = [l1,l2,l3,l4,l5,l6,l7,l8,l9,""]
    for linea in lineas_copa:
        print(linea)


def imprimir_icono_medalla():
    a = chr(127941)
    print(a)


def imprimir_medalla(nombre):
    """
    original extraido de
    url : https://ascii.co.uk/art/medal
    """
    if nombre == "IEEEsparta":
        nombre = "I E E"
        l13 = ": ~    IEE    ~ :"
    elif nombre == "DCCrotona":
        nombre = "D C C"
        l13 = ": ~    DCC    ~ :"
    else:
        l13 = ": ~ A W A R D ~ :"
    l1 = " _______________"
    l2 = "|@@@@|     |####|"
    l3 = "|@@@@|  D  |####|"
    l4 = "|@@@@|  C  |####|"
    l5 = "\\@@@@|  C  |####/"
    l6 = " \\@@@|     |###/"
    l7 = "  `@@|_____|##'"
    l8 = "       (O)"
    l9 = "    .-'''''-."
    l10 = "  .'  * * *  `."
    l11 = " :  *       *  :"
    l12 = f": ~  Ganador  ~ :"
    # l13 = ": ~ A W A R D ~ :"
    l14 = " :  *       *  :"
    l15 = "  `.  * * *  .'"
    l16 = "    `-.....-'"
    
    lineas_medalla = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,
                      l11, l12, l13, l14, l15, l16]
    for linea in lineas_medalla:
        print(linea)


if __name__ == "__main__":
    imprimir_copa("IEEEsparta")
    imprimir_copa("DCCrotona")
    imprimir_copa("luchito")
