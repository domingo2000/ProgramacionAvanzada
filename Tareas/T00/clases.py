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
        alidados_descubiertos = 0
        enemigos_descubiertos = 0

        for fila in self.tablero_rival:
            for casilla in fila:
                if casilla == "F":
                    enemigos_descubiertos += 1
        
        for fila in self.tablero_propio:
            for casilla in fila:
                if casilla == "F":
                    alidados_descubiertos += 1

        puntaje = filas * columnas * barcos *(enemigos_descubiertos - alidados_descubiertos)
        puntaje = max(0, puntaje)
        return(puntaje)

    def guardar_puntaje(self, puntaje, archivo):
        pass