import os
from PyQt5.QtCore import QObject, pyqtSignal
from parametros import CANTIDAD_RANKING


class BackRanking(QObject):
    senal_actualizar_puntaje = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def ordenar_puntajes(self):
        ruta_archivo = os.path.join("ranking.txt")
        try:
            archivo = open(ruta_archivo, "r")
        except FileNotFoundError:
            print("Creando archivo ranking")
            archivo = open(ruta_archivo, "w")
            archivo.close()
            archivo = open(ruta_archivo, "r")

        puntajes = []
        for linea in archivo.readlines():
            dato = linea.strip().split(",")
            usuario = dato[0]
            puntos = int(dato[1][1:])
            puntajes.append([usuario, puntos])
        puntajes.sort(key=lambda puntaje: puntaje[1], reverse=True)
        archivo.close()
        print(puntajes[0:CANTIDAD_RANKING])
        self.senal_actualizar_puntaje.emit(puntajes[0:CANTIDAD_RANKING])

    def escribir_puntaje(self, usuario, puntaje):
        ruta_archivo = os.path.join("ranking.txt")
        try:
            archivo = open(ruta_archivo, "a")
        except FileNotFoundError:
            print("Creando archivo ranking")
            archivo = open(ruta_archivo, "w")
            archivo.close()
            archivo = open(ruta_archivo, "a")

        archivo.write(f"{usuario}, {puntaje}\n")
        archivo.close()


if __name__ == "__main__":
    procesador = BackRanking()
