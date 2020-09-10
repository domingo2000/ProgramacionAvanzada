from estudiante import cargar_datos, cargar_datos_corto


def verificar_numero_alumno(alumno):  # Levanta la excepción correspondiente
    # Condicion 1
    pos_char = 0
    for char in alumno.n_alumno:
        if char.isalpha():
            if (char != "J") or (pos_char != len(alumno.n_alumno) - 1):
                raise ValueError("El numero de alumno es incorrecto")
        pos_char += 1

    # Condicion 2
    primeros_dos_caracteres = alumno.n_alumno[0:1]
    if int(primeros_dos_caracteres) == alumno.generacion:
        pass
    else:
        raise ValueError("El numero de alumno es incorrecto")

    # Condicion 3
    tercer_y_cuarto_caracter = alumno.n_alumno[2:3]
    codigos_carrera = {"Ingeniería": 63, "College": 61}
    if (tercer_y_cuarto_caracter == codigos_carrera["College"]) and\
       alumno.carrera == "College":
        pass
    elif (tercer_y_cuarto_caracter == codigos_carrera["Ingeniería"]) and\
            alumno.carrera == "Ingeniería":
        pass
    else:
        raise ValueError("El numero de alumno es incorrecto")


def corregir_alumno(estudiante):
    # Captura la excepción anterior
    try:
        verificar_numero_alumno(estudiante)
        print(f"{estudiante.nombre} está correctamente"
              f"inscrite en el curso, todo en orden...\n")
    except ValueError as error:
        print(f"Error: {error}")
        # Codigo para corregir el numero


# ************
def verificar_inscripcion_alumno(n_alumno, base_de_datos):  # Levanta la excepción correspondiente
    try:
        alumno = base_de_datos[n_alumno]
        return(alumno)
    except KeyError:
        raise KeyError("El numero de alumno no se encuentra en la base de datos")


def inscripcion_valida(estudiante, base_de_datos):  # Captura la excepción anterior
    try:
        verificar_inscripcion_alumno(estudiante.n_alumno, base_de_datos)
    except KeyError as error:
        print(f"Error: {error}")
        print("¡Alerta! ¡Puede ser Dr. Pinto intentando atraparte!\n")


# ************

def verificar_nota(alumno):  # Levanta la excepción correspondiente
    promedio = alumno.promedio
    if isinstance(promedio, float):
        return True
    else:
        raise TypeError("El promedio no tiene el tipo correcto")


def corregir_nota(estudiante):  # Captura la excepción anterior
    try:
        if verificar_nota(estudiante):
            print(f"Procediendo a hacer git hack sobre {estudiante.promedio}...\n")
    except TypeError as error:
        print(f"Error: {error}")
        if isinstance(estudiante.promedio, int):
            estudiante.promedio = float(estudiante.promedio)
        elif isinstance(estudiante.promedio, int):
            estudiante.promedio = floar(estudiante.promedio.stip())
        print(f"Procediendo a hacer git hack sobre {estudiante.promedio}...\n")


if __name__ == "__main__":
    datos = cargar_datos_corto("alumnos.txt")  # Se cargan los datos
    for alumno in datos.values():
        if alumno.carrera != "Profesor":
            corregir_alumno(alumno)
            inscripcion_valida(alumno, datos)
            corregir_nota(alumno)
