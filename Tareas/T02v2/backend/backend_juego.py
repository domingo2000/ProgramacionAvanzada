from entidades.nivel import Nivel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
import parametros as p
from os import path


class BackJuego(QObject):
    senal_nivel_cargado = pyqtSignal(bool)
    senal_abrir_inicio = pyqtSignal()

    def __init__(self, nivel):
        self.nivel = nivel
        self.usuario = ""
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
        self.nivel.aprobacion_necesaria = aprobacion
        self.nivel.pasos_dobles = pasos_dobles
        self.nivel.pasos_triples = pasos_triples

        ruta_cancion = path.join(*p.CANCIONES[f"{cancion}"])
        self.nivel.cancion = QSound(ruta_cancion)
        self.nivel.crear_generador()
        self.nivel.comenzar()
        self.senal_nivel_cargado.emit(True)

    def borrar_juego(self):
        self.nivel.puntaje_acumulado = 0

    def salir(self):
        self.nivel.terminar_interrumpidamente()
        self.senal_abrir_inicio.emit()

    def escribir_puntaje_en_ranking(self, puntaje_acumulado):
        ruta = path.join(*p.ARCHIVOS["ranking"])
        archivo = open(ruta, "a")
        archivo.write(f"{self.usuario}, {puntaje_acumulado}\n")
        archivo.close()

    def fijar_usuario(self, nombre_usuario):
        self.usuario = nombre_usuario
