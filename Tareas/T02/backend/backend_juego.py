from entidades.nivel import Nivel
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
import parametros as p
from os import path


class BackJuego(QObject):
    senal_nivel_cargado = pyqtSignal(bool)
    senal_abrir_inicio = pyqtSignal()
    senal_cambiar_dinero_tienda = pyqtSignal(int)
    senal_compra_valida = pyqtSignal(bool)

    def __init__(self, nivel):
        self.nivel = nivel
        self.usuario = ""
        self.pinguinos_tienda = None
        self.__dinero_tienda = p.DINERO_INICIAL
        super().__init__()

    @property
    def dinero_tienda(self):
        return self.__dinero_tienda

    @dinero_tienda.setter
    def dinero_tienda(self, valor):
        self.__dinero_tienda = valor
        self.senal_cambiar_dinero_tienda.emit(valor)

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

    def setear_pinguinos_tienda(self, list):
        print(list)
        self.pinguinos_tienda = list

    def chequear_compra(self):
        if self.dinero_tienda >= p.COSTO_PINGUINO:
            print("DEBUG COMPRA REALIZABLE")
            self.senal_compra_valida.emit(True)
        else:
            self.senal_compra_valida.emit(False)

    def realizar_compra(self):
        self.dinero_tienda -= p.COSTO_PINGUINO
