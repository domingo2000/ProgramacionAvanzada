def imprimir_copa(nombre):
    if nombre == "IEEEsparta":
        nombre = "IEE"
        l13 = ": ~    IEE    ~ :"
    elif nombre == "DCCrotona":
        nombre = "DCC"
        l13 = ": ~    DCC    ~ :"
    else:
        nombre = "{1}"
    """
    original extraido de
    url : https://ascii.co.uk/art/trophy
    """
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
    if nombre == "IEEEsparta":
        nombre = "I E E"
        l13 = ": ~    IEE    ~ :"
    elif nombre == "DCCrotona":
        nombre = "D C C"
        l13 = ": ~    DCC    ~ :"
    else:
        l13 = ": ~ A W A R D ~ :"
    """
    original extraido de
    url : https://ascii.co.uk/art/medal
    """
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


def imprimir_moneda():
    print("                 ,.=ctE55ttt553tzs.,                   \n"
          "             ,,c5;z==!!::::  .::7:==it3>.,             \n"
          "          ,xC;z!::::::    ::::::::::::!=c33x,          \n"
          "        ,czz!:::::  ::;;..===:..:::   ::::!ct3.        \n"
          "      ,C;/.:: :  ;=c!:::::::::::::::..      !tt3.      \n"
          "     /z/.:   :;z!:::::J  :E3.  E:::::::..     !ct3.    \n"
          "   ,E;F   ::;t::::::::J  :E3.  E::.     ::.     \\ttL   \n"
          "  ;E7.    :c::::F******   **.  *==c;..    ::     Jttk  \n"
          " .EJ.    ;::::::L                   \"\\:.   ::.    Jttl \n"
          " [:.    :::::::::773.    JE773zs.     I:. ::::.    It3L\n"
          ";:[     L:::::::::::L    |t::!::J     |::::::::    :Et3\n"
          "[:L    !::::::::::::L    |t::;z2F    .Et:::.:::.  ::[13\n"
          "E:.    !::::::::::::L               =Et::::::::!  ::|13\n"
          "E:.    (::::::::::::L    .......       \\:::::::!  ::|i3\n"
          "[:L    !::::      ::L    |3t::::!3.     ]::::::.  ::[13\n"
          "!:(     .:::::    ::L    |t::::::3L     |:::::; ::::EE3\n"
          " E3.    :::::::::;z5.    Jz;;;z=F.     :E:::::.::::II3[\n"
          " Jt1.    :::::::[                    ;z5::::;.::::;3t3 \n"
          "  \\z1.::::::::::l......   ..   ;.=ct5::::::/.::::;Et3L \n"
          "   \\t3.:::::::::::::::J  :E3.  Et::::::::;!:::::;5E3L  \n"
          "    \"cz\\.:::::::::::::J   E3.  E:::::::z!     ;Zz37`   \n"
          "      \\z3.       ::;:::::::::::::::;='      ./355F     \n"
          "        \\z3x.         ::~======='         ,c253F       \n"
          "          \"tz3=.                      ..c5t32^         \n"
          "             \"=zz3==...         ...=t3z13P^            \n"
          "                 `*=zjzczIIII3zzztE3>*^`               \n")


if __name__ == "__main__":
    imprimir_copa("IEEEsparta")
    imprimir_copa("DCCrotona")
    imprimir_copa("luchito")
