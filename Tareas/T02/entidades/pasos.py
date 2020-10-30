from entidades.flechas import FlechaNormal, FlechaDorada, FlechaHielo, FlechaX2
from PyQt5.QtCore import QTimer, QRect, QPoint, QSize, QObject
import parametros as p
import random


class Paso(QTimer):

    def __init__(self, flechas):
        super().__init__()
        self.flechas = flechas
        self.__altura = flechas[0].y()
        self.velocidad = flechas[0].velocidad
        self.realizado = False
        self.crear_rect()
        self.setInterval(p.TASA_REFRESCO * 1000)
        self.timeout.connect(self.mover)

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, valor):
        self.__altura = valor
        self.rect.moveTop(valor)

        if self.altura > 657:
            self.stop()
            for flecha in self.flechas:
                flecha.setParent(None)

    def crear_rect(self):
        x_flechas = [flecha.x() for flecha in self.flechas]
        x_min = min(x_flechas)
        x_max = max(x_flechas)
        y = self.altura
        ancho = x_max - x_min + p.ALTO_FLECHA
        alto = p.ALTO_FLECHA
        self.rect = QRect(QPoint(x_min, y), QSize(ancho, alto))

    def mover(self):
        self.altura += p.TASA_REFRESCO * self.velocidad
        for flecha in self.flechas:
            flecha.mover()

    def comenzar(self):
        self.start()


class GeneradorPasos(QTimer):

    def __init__(self, tiempo_entre_pasos, ronda):
        super().__init__()
        self.__tiempo_entre_pasos = tiempo_entre_pasos
        self.direcciones = ("derecha", "izquierda", "arriba", "abajo")
        self.posicion = (20, 140)  # Lugar donde esta "puesto" el generador de pasos
        self.ronda = ronda
        self.parent = None
        self.pasos_dobles = False
        self.pasos_triples = False
        # Timer
        self.setInterval(tiempo_entre_pasos * 1000)
        self.timeout.connect(self.generar_paso)

    @property
    def tiempo_entre_pasos(self):
        return self.__tiempo_entre_pasos

    @tiempo_entre_pasos.setter
    def tiempo_entre_pasos(self, valor):
        self.__tiempo_entre_pasos = valor
        self.setInterval(valor * 1000)

    def crear_paso(self, numero_flechas):
        direcciones = random.choices(self.direcciones, k=numero_flechas)
        flechas = []
        tipo_flecha = self.calcular_tipo_flecha()
        for direccion in direcciones:
            flecha = self.crear_flecha(direccion, tipo_flecha)
            flechas.append(flecha)
        paso = Paso(flechas)

        paso.comenzar()
        return paso

    def crear_flecha(self, direccion, tipo):
        multiplicadores_direccion = {"izquierda": 0, "arriba": 1, "abajo": 2, "derecha": 3}
        # Posicion de la flecha
        x = self.posicion[0] + (p.ALTO_FLECHA * multiplicadores_direccion[f"{direccion}"])
        y = self.posicion[1]

        if tipo == "normal":
            flecha = FlechaNormal(direccion, self.parent, posicion=(x, y))
        elif tipo == "hielo":
            flecha = FlechaHielo(direccion, self.parent, posicion=(x, y))
        elif tipo == "dorada":
            flecha = FlechaDorada(direccion, self.parent, posicion=(x, y))
        elif tipo == "x2":
            flecha = FlechaX2(direccion, self.parent, posicion=(x, y))

        flecha.senal_cambiar_posicion.connect(self.parent.cambiar_pos_label)
        return flecha

    def calcular_tipo_flecha(self):
        a = random.uniform(0, 1)
        rango_normal = p.PROB_NORMAL
        rango_dorada = rango_normal + p.PROB_FLECHA_DORADA
        rango_hielo = rango_dorada + p.PROB_FLECHA_HIELO
        rango_x2 = rango_hielo + p.PROB_FLECHA_X2
        if a < rango_normal:
            tipo = "normal"
        elif a < rango_dorada:
            tipo = "dorada"
        elif a < rango_hielo:
            tipo = "hielo"
        elif a < rango_x2:
            tipo = "x2"
        return tipo

    def generar_paso(self):
        if self.pasos_triples:
            n = random.randint(1, 3)
        elif self.pasos_dobles:
            n = random.randint(1, 2)
        else:
            n = 1
        paso = self.crear_paso(n)
        self.ronda.pasos_generados.add(paso)
