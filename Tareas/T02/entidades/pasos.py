import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QTimer, QObject, QEventLoop, QRect, QPoint
from PyQt5.QtGui import QPixmap

from backend.animacion import Animacion
import parametros as p
import random
from backend.funciones import sleep


class Flecha(QObject):
    contador_clase = 0
    senal_actualizar_flecha = pyqtSignal(object, int, int)
    senal_destruir = pyqtSignal(QLabel)

    def __init__(self, parent):
        super().__init__()
        Flecha.contador_clase += 1
        # Atributos flecha abstracta
        self.velocidad = p.VELOCIDAD_FLECHA
        self.direccion = random.choice(p.DIRECCIONES)
        self.puntos = p.PUNTOS_FLECHA
        self.probabilidad = None  # float entre 0 y 1
        self.tipo = None
        self.columna = p.DIRECCIONES.index(self.direccion)
        self.__altura = p.ALTURA_INICIAL_FLECHA
        self.parent = parent
        self.capturada = False
        self.viva = True
        self.tamaño = p.TAMANO_VENTANAS["flecha"]
        self.numero = Flecha.contador_clase
        # Label
        self.label = QLabel(parent)

        # Animacion
        rutas_imagenes_explosion = [p.IMAGENES[f"imagen_flecha_{self.direccion}_{i}"]
                                    for i in range(5, 9)]
        rutas_imagenes_explosion.append(p.IMAGENES[f"imagen_explosion_{self.direccion}"])
        paths_imagenes_explosion = [path.join(*rutas_imagenes_explosion[i]) for i in range(5)]
        imagenes_explosion = [QPixmap(paths_imagenes_explosion[i]) for i in range(5)]
        self.animacion_explosion = Animacion(self.label, p.DELAY_EXPLOSION, imagenes_explosion)

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, y):
        self.__altura = y
        x_zona_nivel, y_zona_nivel = p.UBICACION_VENTANAS["ventana_nivel"]
        pos_x = self.columna * p.TAMANO_VENTANAS["zona_captura"] + x_zona_nivel
        pos_y = self.altura
        self.senal_actualizar_flecha.emit(self.label, pos_x, pos_y)

    def init_gui(self, ruta_imagen, parent):
        # Setea parametros y imagenes del label
        x_zona_nivel, y_zona_nivel = p.UBICACION_VENTANAS["ventana_nivel"]
        self.label.setGeometry(self.columna * self.tamaño + x_zona_nivel,
                               y_zona_nivel,
                               self.tamaño, self.tamaño)
        self.label.setStyleSheet("background-color:transparent;")
        imagen_flecha = QPixmap(path.join(*ruta_imagen))
        self.label.setPixmap(imagen_flecha)
        self.label.setScaledContents(True)
        self.label.setVisible(True)

    def capturar(self):
        if self.capturada:
            return None
        else:
            self.capturada = True
            self.animacion_explosion.comenzar()
            sleep(self.animacion_explosion.duracion, milisec=True)
            self.destruir()

    def destruir(self):
        self.senal_destruir.emit(self.label)

    def __repr__(self):
        string = f"Flecha {self.numero}: {self.tipo} = Label:({self.label.x()}, \
            {self.label.y()}), Colider{self.colider.x(), self.colider.y()}"
        return string


class FlechaNormal(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_3"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_NORMAL
        self.tipo = "normal"


class Flecha2(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_4"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_X2
        self.puntos = p.MULTIPLICADOR_PUNTOS_FLECHA_DORADA * p.PUNTOS_FLECHA
        self.tipo = "x2"


class FlechaDorada(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_2"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_DORADA
        self.velocidad = p.VELOCIDAD_FLECHA_DORADA
        self.puntos = p.MULTIPLICADOR_PUNTOS_FLECHA_DORADA * p.PUNTOS_FLECHA
        self.tipo = "dorada"


class FlechaHielo(Flecha):
    senal_poder_hielo = pyqtSignal(float, int)

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_1"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_HIELO
        self.tipo = "hielo"

    def poder(self, duracion_nivel):
        velocidad_actual = p.VELOCIDAD_FLECHA
        velocidad_nueva = velocidad_actual * (0.5)
        ponderador_velocidad = velocidad_nueva / velocidad_actual
        tiempo_reduccion = duracion_nivel * p.REDUCCION_VELOCIDAD_HIELO
        self.senal_poder_hielo.emit(ponderador_velocidad, tiempo_reduccion)
    """
    def capturar(self):
        if self.capturada:
            return None
        else:
            self.capturada = True
            self.animacion_explosion.comenzar()
            sleep(self.animacion_explosion.duracion, milisec=True)
            self.poder(self.parent.nivel.duracion)
            print("Activando Poder Hielo")
            self.destruir()
    """


class Paso(QTimer):
    contador_pasos = 1

    # Rectangulo ABCD que define el colider del paso
    def __init__(self, flechas, parent):
        Paso.contador_pasos += 1
        self.numero = Paso.contador_pasos
        super().__init__()
        self.parent = parent
        self.flechas = flechas
        self.cantidad_flechas = len(self.flechas)
        self.velocidad = self.flechas[0].velocidad
        self.__altura = p.UBICACION_VENTANAS["ventana_nivel"][1]
        self.destruido = False
        # Inicializa el QRect
        x_flechas = [flecha.label.x() for flecha in flechas]
        posicion_esquina_x = min(x_flechas)
        tamaño_flecha = self.flechas[0].label.height()
        ancho = (max(x_flechas) + tamaño_flecha) - min(x_flechas)
        self.colider = QRect(posicion_esquina_x, self.altura, ancho, tamaño_flecha)
        # Fija los valores del timer
        self.setInterval(p.TASA_DE_REFRESCO * 1000)
        self.timeout.connect(self.actualizar_paso)

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, valor):
        self.__altura = valor
        pos_x = self.colider.x()
        pos_y = self.altura
        self.colider.moveTopLeft(QPoint(pos_x, pos_y))
        for flecha in self.flechas:
            flecha.altura = valor

    def mover_paso(self):
        self.altura += self.velocidad * p.TASA_DE_REFRESCO

    def destruir_flechas(self):
        for flecha in self.flechas:
            flecha.destruir()

    def actualizar_paso(self):
        self.mover_paso()
        # Destruye la flecha si pasa la zona de captura
        if self.altura > self.parent.height():
            self.stop()
            self.destruir_flechas()
            self.destruir_paso()

    def destruir_paso(self):
        self.destruido = True

    def __repr__(self):
        string = f"Paso {self.numero}: pos = {self.colider.getCoords()}"
        return string


class GeneradorPasos(QObject):

    def __init__(self, tiempo_entre_pasos, parent,
                 pasos_dobles=False, pasos_triples=False):
        self.pasos = set()
        self.parent = parent
        self.tiempo_entre_pasos = tiempo_entre_pasos
        self.pasos_dobles = pasos_dobles
        self.pasos_triples = pasos_triples
        self.generador_flechas = GeneradorFlechas(self.parent)
        super().__init__()

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(self.tiempo_entre_pasos * 1000)
        self.timer.timeout.connect(self.generar_paso)

    def generar_paso(self):
        if self.pasos_triples:
            numero_flechas = random.randint(1, 3)
            flechas = self.generador_flechas.generar_flechas(numero_flechas)
        elif self.pasos_dobles:
            numero_flechas = random.randint(1, 2)
            flechas = self.generador_flechas.generar_flechas(numero_flechas)
        else:
            numero_flechas = 1
            flechas = self.generador_flechas.generar_flechas(numero_flechas)

        paso = Paso(flechas, self.parent)
        paso.start()
        self.pasos.add(paso)
        self.destruir_pasos_pasados()

    def destruir_pasos_pasados(self):
        pasos_vivos_actuales = set()
        for paso in self.pasos:
            if not(paso.destruido):
                pasos_vivos_actuales.add(paso)
        self.pasos = pasos_vivos_actuales

    def comenzar(self):
        # Genera el primer paso antes del timer
        self.generar_paso()
        self.timer.start()

    def parar(self):
        print("Deteniendo Generacion de pasos")
        self.timer.stop()


class GeneradorFlechas():

    def __init__(self, ventana_contenedora):
        self.ventana_contenedora = ventana_contenedora

    def generar_flechas(self, numero_flechas):
        columnas = random.sample({0, 1, 2, 3}, numero_flechas)
        n = random.uniform(0, 1)
        if n < p.PROB_NORMAL:
            # GENERA FLECHAS NORMALES
            flechas = [FlechaNormal(self.ventana_contenedora) for _ in range(numero_flechas)]
        elif p.PROB_NORMAL < n < p.PROB_NORMAL + p.PROB_FLECHA_DORADA:
            # GENERA DORADA
            flechas = [FlechaDorada(self.ventana_contenedora) for _ in range(numero_flechas)]
        elif p.PROB_NORMAL + p.PROB_FLECHA_DORADA < n < \
                p.PROB_NORMAL + p.PROB_FLECHA_DORADA + p.PROB_FLECHA_X2:
            # GENERA X2
            flechas = [Flecha2(self.ventana_contenedora) for _ in range(numero_flechas)]
        else:
            # Genera Hielo
            flechas = [FlechaHielo(self.ventana_contenedora) for _ in range(numero_flechas)]
        for flecha in flechas:
            flecha.senal_actualizar_flecha.connect(self.ventana_contenedora.actualizar_label)
            flecha.senal_destruir.connect(self.ventana_contenedora.destruir_label)

        return(flechas)
