from collections import namedtuple, defaultdict
import os


# Para esta parte necesitarás los contenidos de la semana 0
def cargar_datos(path):
    archivo = open(path, "rt", encoding="utf-8")
    lista_lineas = archivo.readlines()
    # Para esta función te puede servir el cuaderno 3 de la semana 0
    return lista_lineas

# De aquí en adelante necesitarás los contenidos de la semana 1


def crear_ayudantes(datos):
    ayudantes = []
    Ayudantes = namedtuple("ayudantes", ["nombre", "cargo", "usuario"])
    datos.pop(0)
    for linea in datos:
        dato = linea[:-1].split(", ")
        ayudante = Ayudantes(dato[0], dato[1], dato[2])
        ayudantes.append(ayudante)
    return ayudantes


def encontrar_cargos(ayudantes):
    cargos = set()
    for ayudante in ayudantes:
        cargo = ayudante.cargo
        cargos.add(cargo)
    return cargos


def ayudantes_por_cargo(ayudantes):
    ayudantes_cargo = \
        {"Híbrido Tareas": [], "Híbrido Docencia": [], "Full Tareas": [], "Full Docencia": []}
    for ayudante in ayudantes:
        cargo = ayudante.cargo
        ayudantes_cargo[cargo].append(ayudante.nombre)
    return ayudantes_cargo


if __name__ == '__main__':
    datos = cargar_datos('ayudantes.csv')
    if datos is not None:
        print('Se lograron leer los datos')
    else:
        print('Debes completar la carga de datos')

    ayudantes = crear_ayudantes(datos)
    if ayudantes is not None:
        print('\nLos ayudantes son:')
        for ayudante in ayudantes:
            print(ayudante)
    else:
        print('\nDebes completar la creación de Ayudantes')

    cargos = encontrar_cargos(ayudantes)
    if cargos is not None:
        print('\nLos cargos son:')
        for cargo in cargos:
            print(cargo)
    else:
        print('\nDebes completar la búsqueda de Cargos')

    clasificados = ayudantes_por_cargo(ayudantes)
    if clasificados is not None:
        print('\nLos ayudantes por cargos son:')
        for cargo in clasificados:
            print(f'\n{cargo}')
            for ayudante in clasificados[cargo]:
                print(ayudante)
    else:
        print('\nDebes completar la clasificación de Ayudantes')
