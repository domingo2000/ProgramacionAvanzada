from widgets.niveles import NivelPrincipiante, NivelAficionado, NivelMaestroCumbia, Nivel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
import parametros as p
from os import path


class BackJuego(QObject):
    senal_cargar_nivel = pyqtSignal(Nivel, QSound)
    senal_nivel_cargado = pyqtSignal(bool)

    def __init__(self):
        self.nivel = NivelPrincipiante()
        super().__init__()

    def generar_nivel(self, cancion, dificultad):
        if dificultad == "Principiante":
            nivel = NivelPrincipiante()
        elif dificultad == "Aficionado":
            nivel = NivelAficionado()
        elif dificultad == "Maestro Cumbia":
            nivel = NivelMaestroCumbia()
        else:
            print(f"Error: Dificultad vale: {dificultad}, cancion vale: {cancion}")

        self.nivel = nivel

        ruta_cancion = path.join(*p.CANCIONES[f"{cancion}"])
        cancion = QSound(ruta_cancion)
        self.senal_cargar_nivel.emit(nivel, cancion)
