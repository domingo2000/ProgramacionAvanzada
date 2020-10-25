from entidades.nivel import Nivel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
import parametros as p
from os import path


class BackJuego(QObject):
    senal_cargar_nivel = pyqtSignal(Nivel, QSound, int, int, bool, bool)
    senal_nivel_cargado = pyqtSignal(bool)

    def __init__(self, nivel):
        self.nivel = nivel
        super().__init__()

    def generar_nivel(self, cancion, dificultad):
        if dificultad == "Principiante":
            duracion, tiempo_entre_pasos, aprobacion = p.NIVEL_PRINCIPIANTE.values()
            pasos_dobles = False
            pasos_triples = False
        elif dificultad == "Aficionado":
            duracion, tiempo_entre_pasos, aprobacion = p.NIVEL_AFICIONADO.values()
            pasos_dobles = True
            pasos_triples = False
        elif dificultad == "Maestro Cumbia":
            duracion, tiempo_entre_pasos, aprobacion = p.NIVEL_MAESTRO_CUMBIA.values()
            pasos_dobles = True
            pasos_triples = True
        else:
            print(f"Error: Dificultad vale: {dificultad}, cancion vale: {cancion}")

        self.nivel.duracion = duracion
        self.nivel.tiempo_entre_pasos = tiempo_entre_pasos
        self.nivel.aprobacion = aprobacion
        self.nivel.pasos_dobles = pasos_dobles
        self.nivel.pasos_triples = pasos_triples

        ruta_cancion = path.join(*p.CANCIONES[f"{cancion}"])
        self.nivel.cancion = QSound(ruta_cancion)
        self.nivel.crear_generador()
        self.nivel.comenzar()
