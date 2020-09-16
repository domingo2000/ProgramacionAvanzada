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

    archivo.close()
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

    archivo.close()
    return lista_deportistas


def leer_bool(string):
    if string == "True":
        return (True)
    elif string == "False":
        return (False)
    else:
        print("Error leyendo booleando")


def escribir_resultados_dia(archivo, resultados_dia, numero_dia):
    # resultados competencia debe ser un lista:
    # [nombre_deporte, [delegacion_ganadora, deportista_ganador],
    #                  [delegacion_perdedora, deportista perdedor]]
    archivo = open(archivo, "a", encoding="utf8")

    # Escritura de datos en resultados
    archivo.write(f"Día: {numero_dia}\n")
    # resto de  la info de la comepetencia
    for resultado_competencia in resultados_dia:
        if resultado_competencia == "empate":
            archivo.write(f"EMPATE\n")
        else:
            competencia = resultado_competencia[0]
            delegacion_ganadora = resultado_competencia[1][0]
            deportista_ganador = resultado_competencia[1][1]
            archivo.write(f"Competencia: {competencia}\n")
            archivo.write(f"Delegación Ganadora: {delegacion_ganadora.nombre}\n")
            archivo.write(f"Deportista Ganador: {deportista_ganador.nombre}\n")
            archivo.write("\n")
    archivo.write("*****************************************\n")

    archivo.close()


def limpiar_archivo_resultados(archivo):
    archivo = open(archivo, "w", encoding="utf8")
    archivo.write("RESULTADOS DÍA A DÍA DCCUMBRE OLÍMPICA\n")
    archivo.write("-----------------------------------------\n")
    archivo.close()


if __name__ == "__main__":
    from clases_simulacion import DCCrotona, IEEEsparta, Deportista

    # Testeo delegaciones.csv
    d1 = Deportista("Alexis", 14, 20, 30, 88, False, 20)
    d2 = Deportista("Charles", 15, 23, 43, 50, True, 23)
    d3 = Deportista("Mago Valdivia", 23, 34, 21, 21, False, 100)
    d4 = Deportista("Mati Fernandez", 21, 22, 12, 44, False, 42)
    equipo = [d1, d2, d3, d4]

    datos_delegaciones = leer_datos_delegaciones("delegaciones.csv")
    lista_delegaciones = []
    for dato in datos_delegaciones:
        tipo_delegacion = dato["Delegacion"]
        entrenador = input("Ingrese el nombre del entrenador: ")
        equipo = equipo
        moral = dato["Moral"]
        dinero = dato["Dinero"]
        medallas = dato["Medallas"]
        if tipo_delegacion == "DCCrotona":
            delegacion = DCCrotona(entrenador, equipo, medallas, moral, dinero)
        elif tipo_delegacion == "IEEEsparta":
            delegacion = IEEEsparta(entrenador, equipo, medallas, moral, dinero)
        else:
            print("ERROR")
        lista_delegaciones.append(delegacion)

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
