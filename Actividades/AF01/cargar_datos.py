import os
from random import choice, sample

from bolsillo import BolsilloCriaturas
from entidades import Criatura, Entrenador

# devuelve un diccionario de la forma {"Nombre_creatura, Creatura"}
def cargar_criaturas(archivo_criaturas):
    dict_creaturas = {}
    archivo = open(archivo_criaturas, "r")
    nombre_columnas = archivo.readline()[:-1].split(",")
    for linea in archivo.readlines():
        linea = linea[:-1].split(",")
        nombre = linea[0]
        tipo = linea[1]
        hp = int(linea[2])
        atk = int(linea[3])
        sp_atk = int(linea[4])
        defense = int(linea[5])
        criatura = Criatura(nombre, tipo, hp, atk, sp_atk, defense)
        dict_creaturas[linea[0]] = criatura
    archivo.close()
    return dict_creaturas


def cargar_rivales(archivo_rivales):
    rivales = []
    criaturas = cargar_criaturas("criaturas.csv")
    archivo = open(archivo_rivales, "r")
    nombre_columnas = archivo.readline()[:-1].split(",")
    for linea in archivo.readlines():
        datos = linea[:-1].split(",")
        nombre_entrenador = datos[0]
        nombre_creaturas = datos[1].split(";")
        bolsillo = BolsilloCriaturas()
        for nombre_creatura in nombre_creaturas:
            creatura = criaturas[nombre_creatura]
            bolsillo.append(creatura)
        entrenador = Entrenador(nombre_entrenador, bolsillo)
        rivales.append(entrenador)
    return rivales
    
    # Completar


def crear_jugador(nombre):
    criaturas = cargar_criaturas("criaturas.csv")
    bolsillo = BolsilloCriaturas()
    lista_creaturas = list(criaturas.values())
    # Elije 6 criaturas al azar
    creaturas_al_azar = sample(lista_creaturas, 6)
    for creatura in creaturas_al_azar:
        bolsillo.append(creatura)

    entrenador = Entrenador(nombre, bolsillo)
    return entrenador
    # Completar


if __name__ == "__main__":
    # NO MODIFICAR
    # El siguiente codigo te ayudara a debugear este archivo.
    # Simplemente corre este archivo (cargar_datos.py)

    # Aquí revisamos si te encuentras en la ruta adecuada, para esto
    # vemos si el archivo criaturas.csv se encuentra dentro de la
    # carpera en la que estás trabajando
    if "criaturas.csv" not in list(os.walk(os.getcwd()))[0][2]:
        print(f"No estas en el directorio adecuado!")
    criaturas = cargar_criaturas("criaturas.csv")
    rivales = cargar_rivales("rivales.csv")
    jugador = crear_jugador("El Cracks")

    # Aquí revisamos si retornas lo adecuado, para esto se revisa si
    # lo retornado es una instancia de la clase correspondiente
    if (type(criaturas) is not dict or \
        not all(type(criatura) is Criatura for criatura in criaturas.values())):
            print("Recuerda: cargar_criaturas retorna un diccionario con Criatura")
    else:
        print("Lista de Criatura tiene formato correcto")
    if type(rivales) is not list or not all(type(rival) is Entrenador for rival in rivales):
        print("Recuerda: cargar_rivales retorna una lista de Entrenador")
    else:
        print("Lista de Entrenador tiene formato correcto")

    # Aquí revisamos que los datos que deben ser entregados como int
    # al __init__ de Criaturas se almacenen con el tipo correcto
    if type(criaturas) is dict:
        if not all(
            type(atributo) is int
            for criatura in criaturas.values()
            for atributo in [criatura.hp_base, criatura.atk, criatura.sp_atk, criatura.defense]
        ):
            print("Recuerda: los atributos de Criatura hp, atk, sp_atk y defensa deben ser int")
        else:
            print("Instancias de Criatura tienen atributos con tipo correcto")

    # Aquí revisamos que la cantidad de Criaturas en el Bolsillo del
    # Jugador sea la adecuada
    if type(jugador) is not Entrenador or len(jugador.bolsillo) < 6:
        print("Recuerda: debes agregar 6 Criaturas a tu bolsillo")
    else:
        print("Jugador tiene la cantidad correcta de Criatura en su Bolsillo")
