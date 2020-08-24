import parametros
import random


class Partida:
    """
    Clase Partida: Esta clase define una partida del juego, con el tablero,
    el estado de la partida y los nombres de los jugadores
    """
    def __init__(self, apodo, filas, columnas):
        self.apodo = apodo
        self.dimensiones = (filas, columnas)
        self.bomba_especial_usada = False
        self.aliados_descubiertos = 0
        self.enemigos_descubiertos = 0
        self.puntaje = 0
        self.ganador = ""
        self.perdedor = ""
        self.terminada = False

        # Crea el tablero vacio
        self.tablero_rival = []
        self.tablero_propio = []
        for i in range(filas):
            fila_rival = []
            fila_propio = []
            for j in range(columnas):
                fila_rival.append(" ")
                fila_propio.append(" ")
            self.tablero_rival.append(fila_rival)
            self.tablero_propio.append(fila_propio)
        # Agrega barcos (rivales y propios) al tablero
        coordenadas_barcos_rival = set()
        coordenadas_barcos_propio = set()
        while len(coordenadas_barcos_rival) < parametros.NUM_BARCOS:
            coordenada_x = random.randint(0, filas - 1)
            coordenada_y = random.randint(0, columnas - 1)
            coordenada_barco = (coordenada_x, coordenada_y)
            coordenadas_barcos_rival.add(coordenada_barco)
        while len(coordenadas_barcos_propio) < parametros.NUM_BARCOS:
            coordenada_x = random.randint(0, filas - 1)
            coordenada_y = random.randint(0, columnas - 1)
            coordenada_barco = (coordenada_x, coordenada_y)
            coordenadas_barcos_propio.add(coordenada_barco)
        for coordenada_barco in coordenadas_barcos_rival:
            x = coordenada_barco[0]
            y = coordenada_barco[1]
            self.tablero_rival[x][y] = "B"
        for coordenada_barco in coordenadas_barcos_propio:
            x = coordenada_barco[0]
            y = coordenada_barco[1]
            self.tablero_propio[x][y] = "B"

    # metodos
    def calcular_puntaje(self):
        filas = self.dimensiones[0]
        columnas = self.dimensiones[1]
        barcos = parametros.NUM_BARCOS
        aliados_descubiertos = self.aliados_descubiertos
        enemigos_descubiertos = self.enemigos_descubiertos

        puntaje = filas * columnas * barcos * (enemigos_descubiertos - aliados_descubiertos)
        puntaje = max(0, puntaje)
        self.puntaje = puntaje

    def guardar_puntaje(self, path_archivo):
        puntaje = self.puntaje
        string_datos = f"\n{self.apodo},{self.puntaje}"
        archivo = open(path_archivo, "a")
        archivo.write(string_datos)
        archivo.close()

    def ver_si_gano(self):
        if self.enemigos_descubiertos == parametros.NUM_BARCOS:
            self.ganador = self.apodo
            self.perdedor = "computador"
            self.terminada = True
        elif self.aliados_descubiertos == parametros.NUM_BARCOS:
            self.ganador = "computador"
            self.perdedor = self.apodo
            self.terminada = True
        else:
            terminada = False