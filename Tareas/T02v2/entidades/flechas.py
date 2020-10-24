import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, QTimer, QObject, QEventLoop, QRect, QPoint
from PyQt5.QtGui import QPixmap

# from backend.animacion import Animacion
from backend.animacion import Animacion
import parametros as p
import random
from backend.funciones import sleep


class FlechaObjeto(QObject):
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
        # Label
        self.label = QLabel(parent)
        # Colider
        self.colider = QRect(self.columna * self.tamaño, 0, self.tamaño, self.tamaño)

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
        pos_x = self.columna * p.TAMANO_VENTANAS["zona_captura"]
        pos_y = self.altura
        self.colider.moveTopLeft(QPoint(pos_x, pos_y))
        self.senal_actualizar_flecha.emit(self, pos_x, pos_y)

    def init_gui(self, ruta_imagen, parent):
        # Setea parametros y imagenes del label
        self.label.setGeometry(self.columna * self.tamaño, 0, self.tamaño, self.tamaño)
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


class Flecha(QThread):
    contador_clase = 0
    senal_actualizar_flecha = pyqtSignal(object, int, int)
    senal_destruir = pyqtSignal(QLabel)

    def __init__(self, parent):
        super().__init__()
        Flecha.contador_clase += 1
        self.numero = Flecha.contador_clase
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
        pos_x = self.columna * p.TAMANO_VENTANAS["zona_captura"]
        pos_y = self.altura
        self.colider.moveTopLeft(QPoint(pos_x, pos_y))
        self.senal_actualizar_flecha.emit(self, pos_x, pos_y)
        """
        if self.altura > self.parent.height():
            self.destruir()
        """
    def init_gui(self, ruta_imagen, parent):
        separacion = p.TAMANO_VENTANAS["zona_captura"]
        # genera la caja del Qrect
        self.colider = QRect(self.columna * separacion, 0, separacion, separacion)
        # Setea parametros y imagenes del label
        self.label.setGeometry(self.columna * separacion, 0, separacion, separacion)
        self.label.setStyleSheet("background-color:transparent;")
        imagen_flecha = QPixmap(path.join(*ruta_imagen))
        self.label.setPixmap(imagen_flecha)
        self.label.setScaledContents(True)
        self.label.setVisible(True)

    def mover_flecha(self):
        self.altura += p.TASA_DE_REFRESCO * self.velocidad

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

    def cambiar_velocidad(self, ponderador, tiempo_reduccion):
        print(f"{self}, reduciendo _velocidad")
        velocidad_original = self.velocidad
        self.velocidad = self.velocidad * ponderador
        sleep(tiempo_reduccion)
        print("VOLVIENDO A VELOCIDAD ORIGINAL")
        self.velocidad = velocidad_original

    def run(self):
        while self.label.y() < self.parent.height():
            sleep(p.TASA_DE_REFRESCO)
            self.mover_flecha()
        # Destruye la flecha si pasa la zona de captura
        self.destruir()

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
        self.puntos = p.PUNTOS_FLECHA_x2
        self.tipo = "x2"


class FlechaDorada(Flecha):

    def __init__(self, parent):
        super().__init__(parent)
        ruta_imagen = p.IMAGENES[f"imagen_flecha_{self.direccion}_2"]
        super().init_gui(ruta_imagen, parent)
        self.probabilidad = p.PROB_FLECHA_DORADA
        self.velocidad = p.VELOCIDAD_FLECHA_DORADA
        self.puntos = p.PUNTOS_FLECHA_DORADA
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


class Paso(QThread):
    # Rectangulo ABCD que define el colider del paso
    def __init__(self, flechas, parent):
        super().__init__()
        self.parent = parent
        self.flechas = flechas
        self.cantidad_flechas = len(self.flechas)
        self.__altura = 0
        # Inicializa el QRect
        x_flechas = [flecha.label.x() for flecha in flechas]
        posicion_esquina_x = min(x_flechas)
        tamaño_flecha = self.flechas[0].colider.height()
        ancho = (max(x_flechas) + tamaño_flecha) - min(x_flechas)
        self.qrect = QRect(posicion_esquina_x, self.altura, ancho, tamaño_flecha)
        # Fija la posicion

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, valor):
        self.__altura = valor
        self.qrect.moveTop(valor)
        print(f"DEBUG: {self.qrect.getCoords()}")
        for flecha in self.flechas:
            flecha.altura = valor

    def mover_paso(self):
        self.altura += p.VELOCIDAD_FLECHA * p.TASA_DE_REFRESCO

    def destruir_flechas(self):
        for flecha in self.flechas:
            flecha.destruir()

    def run(self):
        while self.altura < self.parent.height():
            sleep(p.TASA_DE_REFRESCO)
            self.mover_paso()
        # Destruye la flecha si pasa la zona de captura
        self.destruir_flechas()

    def __repr__(self):
        string = f"Paso_Object: qrect_pos = {self.qrect.getCoords()}"


class GeneradorFlecha(QObject):

    def __init__(self, tiempo_entre_flechas, parent,
                 pasos_dobles=False, pasos_triples=False):
        self.flechas = set()
        self.parent = parent
        self.tiempo_entre_flechas = tiempo_entre_flechas
        self.pasos_dobles = pasos_dobles
        self.pasos_triples = pasos_triples
        super().__init__()

        # Timer
        self.timer = QTimer()
        self.timer.setInterval(tiempo_entre_flechas * 1000)
        self.timer.timeout.connect(self.generar_flechas)

    def generar_flechas(self):
        if self.pasos_triples:
            funciones_generadoras_pasos = [self.generar_flecha,
                                           self.generar_dos_flechas,
                                           self.generar_tres_flechas]
            funcion_escogida = random.choice(funciones_generadoras_pasos)
            funcion_escogida()
        elif self.pasos_dobles:
            funciones_generadoras_pasos = [self.generar_flecha,
                                           self.generar_dos_flechas]
            funcion_escogida = random.choice(funciones_generadoras_pasos)
            funcion_escogida()
        else:
            self.generar_flecha()

    def generar_tres_flechas(self):
        for _ in range(3):
            self.generar_flecha()

    def generar_dos_flechas(self):
        self.generar_flecha()
        self.generar_flecha()

    def generar_flecha(self):
        n = random.uniform(0, 1)
        if n < p.PROB_NORMAL:
            # GENERA FLECHA NORMAL
            flecha = FlechaNormal(self.parent)
        elif p.PROB_NORMAL < n < p.PROB_NORMAL + p.PROB_FLECHA_DORADA:
            # GENERA DORADA
            flecha = FlechaDorada(self.parent)
        elif p.PROB_NORMAL + p.PROB_FLECHA_DORADA < n < \
                p.PROB_NORMAL + p.PROB_FLECHA_DORADA + p.PROB_FLECHA_X2:
            # GENERA X2
            flecha = Flecha2(self.parent)
        else:
            # Genera Hielo
            flecha = FlechaHielo(self.parent)
        flecha.senal_actualizar_flecha.connect(self.parent.actualizar_flecha)
        flecha.senal_destruir.connect(self.parent.destruir_label)
        # Si es de hielo conecta la señal
        if flecha.tipo == "hielo":
            for flecha_a_conectar in self.flechas:
                flecha.senal_poder_hielo.connect(flecha_a_conectar.cambiar_velocidad)
        flecha.start()
        self.flechas.add(flecha)

    def comenzar(self):
        print("Empieza generacion de flechas")
        # Genera la primera flecha antes que el timer
        self.generar_flecha()

        self.timer.start()

    def parar(self):
        print("Deteniendo Generacion de flechas")
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication([])

    ventana = QWidget()
    ventana.setGeometry(0, 0, 500, 500)
    flechas = [FlechaNormal() for _ in range(3)]
    paso = Paso(flechas)

    sys.exit(app.exec_())
