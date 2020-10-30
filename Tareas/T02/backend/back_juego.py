from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QEventLoop, QRect, QUrl
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from os import path
from entidades.pasos import GeneradorPasos
from entidades.pinguinos import Pinguino
import parametros as p
from ronda import Ronda


class BackJuego(QObject):
    """
    Backend del juego
    """
    senal_compra_valida = pyqtSignal(bool)
    senal_actualizar_dinero_tienda = pyqtSignal(int)
    senal_escribir_puntaje_ranking = pyqtSignal(str, int)
    senal_juego_terminado = pyqtSignal()
    senal_activar_boton_comenzar = pyqtSignal()
    senal_mostrar_ventana_resumen = pyqtSignal(int, int, int, int, int, str, str, bool)
    senal_esconder_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.usuario = ""
        self.puntaje_acumulado = 0
        self.__dinero_tienda = p.DINERO_INCIAL
        self.costo_pinguino = p.PRECIO_PINGUIRIN
        self.ronda = Ronda()
        self.pinguinos_pista_baile = set()
        self.pinguinos_tienda = set()

        self.coliders_pista_baile = []
        colider_pista_baile_1 = QRect(310, 420, 421, 181)
        colider_pista_baile_2 = QRect(350, 400, 331, 91)
        self.coliders_pista_baile.append(colider_pista_baile_1)
        self.coliders_pista_baile.append(colider_pista_baile_2)

    @property
    def dinero_tienda(self):
        return self.__dinero_tienda

    @dinero_tienda.setter
    def dinero_tienda(self, valor):
        self.__dinero_tienda = valor
        self.senal_actualizar_dinero_tienda.emit(valor)

    def set_usuario(self, usuario):
        self.usuario = usuario

    def terminar_juego(self):
        self.ronda.terminar(interrumpido=True)
        self.senal_escribir_puntaje_ranking.emit(self.usuario, self.puntaje_acumulado)
        self.borrar_datos()

    def borrar_datos(self):
        self.puntaje_acumulado = 0
        self.limpiar_pinguinos_pista_baile()
        self.limpiar_flechas_juego()
        self.senal_juego_terminado.emit()

    def limpiar_pinguinos_pista_baile(self):
        for pinguino in self.pinguinos_pista_baile:
            pinguino.setParent(None)
        self.pinguinos_pista_baile = set()

    def limpiar_flechas_juego(self):
        for paso in self.ronda.pasos_generados:
            for flecha in paso.flechas:
                flecha.setParent(None)

    def pausar_juego(self):
        pass

    def comenzar_juego(self):
        ventana_juego = self.sender()
        ventana_juego.tienda.show()
        self.ronda.generador_pasos.parent = ventana_juego
        self.dinero_tienda = p.DINERO_INCIAL

    def comenzar_ronda(self, dificultad, cancion):
        self.setear_ronda(dificultad, cancion)
        print("Comenzando ronda")
        self.ronda.comenzar()

    def setear_ronda(self, dificultad, nombre_cancion):
        url = QUrl()
        url = QUrl.fromLocalFile(path.join(*p.CANCIONES[f"{nombre_cancion}"]))
        content = QMediaContent(url)
        self.ronda.cancion.setMedia(content)
        duracion, tiempo_entre_pasos, aprobacion_necesaria = \
            tuple(p.NIVELES[f"{dificultad}"].values())
        self.ronda.duracion = duracion
        self.ronda.tiempo_entre_pasos = tiempo_entre_pasos
        self.ronda.aprobacion_necesaria = aprobacion_necesaria
        self.ronda.dificultad = dificultad

    def revisar_cheatcodes(self, set_teclas):
        if {"m", "o", "n"}.issubset(set_teclas):
            self.cheat_dinero()
        elif {"n", "i", "v"}.issubset(set_teclas):
            self.cheat_niv()
        elif {"p"} == set_teclas:
            if not self.ronda.nivel_comenzado:
                return
            if self.ronda.esta_pausada:
                self.ronda.reanudar()
            else:
                self.ronda.pausar()

    def cheat_dinero(self):
        self.dinero_tienda += p.DINERO_TRAMPA

    def cheat_niv(self):
        self.ronda.terminar()

    def chequear_compra(self):
        if self.dinero_tienda >= p.PRECIO_PINGUIRIN:
            self.senal_compra_valida.emit(True)
        else:
            self.senal_compra_valida.emit(False)

    def manejar_dropeo(self, drop_event):
        ventana_juego = self.sender()
        pos = drop_event.pos()
        x = pos.x()
        y = pos.y()
        pinguino_original = drop_event.source()

        copia_pinguino = Pinguino(pinguino_original.color, ventana_juego, iscopy=True, pos=(x, y))
        pinguino_en_zona_correcta = False
        for colider in self.coliders_pista_baile:
            if copia_pinguino.colider.intersects(colider):
                pinguino_en_zona_correcta = True
                break
        for pinguino in self.pinguinos_pista_baile:
            if pinguino.colider.intersects(copia_pinguino.colider):
                pinguino_en_zona_correcta = False

        if pinguino_en_zona_correcta:
            print("Zona Correcta")
            copia_pinguino.senal_cambiar_frame.connect(ventana_juego.actualizar_frame_label)
            drop_event.acceptProposedAction()
            self.pinguinos_pista_baile.add(copia_pinguino)
            self.realizar_compra(p.PRECIO_PINGUIRIN)
            if len(self.pinguinos_pista_baile) == 1:
                self.senal_activar_boton_comenzar.emit()

        else:
            print("ZONA INCORRECTA")
            copia_pinguino.setParent(None)

    def realizar_compra(self, costo):
        self.dinero_tienda -= costo

    def hacer_bailar_pinguinos(self, flechas):
        set_flechas = set(flechas)
        for pinguino in self.pinguinos_pista_baile:
            pinguino.bailar(flechas)

    def calcular_estadisticas(self, puntaje_obtenido, combo_maximo, pasos_fallados, aprobacion,
                              interrumpido=False):
        self.actualizar_dinero_tienda(puntaje_obtenido)
        if aprobacion >= self.ronda.aprobacion_necesaria:
            mensaje = "Has ganado, puedes jugar nuevamente"
            ventana__a_volver = "ventana_juego"
        else:
            ventana__a_volver = "ventana_inicio"
            mensaje = "Has perdido, vuelve a intentarlo otra vez"
            self.borrar_datos()

        self.puntaje_acumulado += puntaje_obtenido
        self.senal_mostrar_ventana_resumen.emit(puntaje_obtenido, self.puntaje_acumulado,
                                                combo_maximo, pasos_fallados, aprobacion,
                                                mensaje, ventana__a_volver, interrumpido)
        self.senal_esconder_juego.emit()

    def actualizar_dinero_tienda(self, dinero):
        self.dinero_tienda += dinero
