def leer_datos_delegaciones(archivo):
    """
    Esta funcion toma un archivo.csv y retorna una lista con diccionarios
    que contienen los datos de la delegacion como {nombre_dato : dato}
    """
    archivo = open(archivo, "r")
    lista_delegaciones = []  # esta lista contiene los datos de las delegaciones ordenados

    # diccionario que tiene como llaves los label del archivo y como value el dato
    datos_delegacion = dict()
    llaves = archivo.readline()[:-1].split(",")

    for llave in llaves:
        datos_delegacion[llave] = None
    for linea in archivo.readlines():
        datos_delegacion_i = datos_delegacion.copy()
        datos_linea = linea[:-1].split(",")

        COUNT = 0
        for dato in datos_linea:
            datos_delegacion_i[llaves[COUNT]] = dato
            COUNT += 1
        lista_delegaciones.append(datos_delegacion_i)

    return lista_delegaciones


def leer_datos_deportistas(archivo):
    """
    Esta funcion toma un archivo.csv y retorna una lista con diccionarios
    que contienen los datos de los deportistas como {nombre_dato : dato}
    """
    archivo = open(archivo, "r")
    lista_deportistas = []  # esta lista contiene los datos de los deportistas

    # diccionario que tiene como llaves los label del archivo y como value el dato
    datos_deportista = dict()
    llaves = archivo.readline()[:-1].split(",")

    # crea el diccionario de los datos de 1 deportista {"label_dato" : dato}
    COUNT = 0
    for llave in llaves:
        llaves[COUNT] = llave.strip()
        llave = llave.strip()
        datos_deportista[llave] = None
        COUNT += 1

    # lee el archivo y llena la lista deportistas con los datos
    for linea in archivo.readlines():
        datos_deportista_i = datos_deportista.copy()
        datos_linea = linea[:-1].split(",")
        COUNT = 0
        for dato in datos_linea:
            datos_deportista_i[llaves[COUNT]] = dato.strip()
            COUNT += 1
        lista_deportistas.append(datos_deportista_i)

    return lista_deportistas


def leer_bool(string):
    if string == "True":
        return (True)
    elif string == "False":
        return (False)
    else:
        print("Error leyendo booleando")


if __name__ == "__main__":
    from clases_simulacion import DCCrotona, IEEEsparta, Deportista

    # Testeo delegaciones.csv
    d1 = Deportista("Alexis", 14, 20, 30, 88, False, 20)
    d2 = Deportista("Charles", 15, 23, 43, 50, True, 23)
    d3 = Deportista("Mago Valdivia", 23, 34, 21, 21, False, 100)
    d4 = Deportista("Mati Fernandez", 21, 22, 12, 44, False, 42)
    equipo = [d1, d2, d3, d4]

    datos = leer_datos_delegaciones("delegaciones.csv")

    for dato in datos:
        tipo_delegacion = dato["Delegacion"]
        entrenador = input("Ingrese el nombre del entrenador: ")
        equipo = equipo
        moral = dato["Moral"]
        dinero = dato["Dinero"]
        medallas = dato["Medallas"]
        if tipo_delegacion == "DCCrotona":
            delegacion = DCCrotona(entrenador, equipo, medallas, moral, dinero)
        elif tipo_delegacion == "IEEEsport":
            delegacion = IEEEsparta(entrenador, equipo, medallas, moral, dinero)

    # testeo deportistas.csv
    datos_deportistas = leer_datos_deportistas("deportistas.csv")
    lista_deportistas = []
    for dato in datos_deportistas:
        nombre = dato["nombre"]
        velocidad = int(dato["velocidad"])
        resistencia = int(dato["resistencia"])
        flexibilidad = int(dato["flexibilidad"])
        moral = int(dato["moral"])
        lesionado = leer_bool(dato["lesionado"])
        precio = dato["precio"]
        deportista = Deportista(nombre, velocidad, 
                                resistencia, flexibilidad, moral, lesionado, precio)
        lista_deportistas.append(deportista)
    print("FIN")
