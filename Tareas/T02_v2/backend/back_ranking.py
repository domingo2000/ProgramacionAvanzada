import os
from PyQt5.QtCore import QObject, pyqtSignal
from parametros import NUMERO_PUNTAJES_MAXIMOS_RANKING


class BackRanking(QObject):
    senal_procesar_puntajes = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.senal_actualizar_puntaje = None
        self.senal_procesar_puntajes.connect(self.actualizar_puntajes)

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
        return(puntajes[0:NUMERO_PUNTAJES_MAXIMOS_RANKING])

    def actualizar_puntajes(self):
        puntajes = self.ordenar_puntajes()
        if self.senal_actualizar_puntaje:
            self.senal_actualizar_puntaje.emit(puntajes)


if __name__ == "__main__":
    procesador = BackRanking()
    print(procesador.ordenar_puntajes())
