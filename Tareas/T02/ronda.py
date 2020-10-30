from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QEventLoop, QRect, QUrl
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from os import path
from entidades.pasos import GeneradorPasos
from entidades.pinguinos import Pinguino
import parametros as p


class Ronda(QObject):
    senal_paso_correcto = pyqtSignal(list)
    senal_actualizar_combo = pyqtSignal(int)
    senal_actualizar_combo_maximo = pyqtSignal(int)
    senal_actualizar_progreso = pyqtSignal(int)
    senal_actualizar_aprobacion = pyqtSignal(int)
    senal_paso_correcto = pyqtSignal(set)
    senal_calcular_estadisticas = pyqtSignal(int, int, int, int, bool)

    def __init__(self, duracion=10, tiempo_entre_pasos=0.1, aprobacion_necesaria=0,
                 ruta_cancion=path.join(*p.CANCIONES["Shingeki"])):
        super().__init__()

        url = QUrl()
        url = url.fromLocalFile("cancion_1.wav")
        content = QMediaContent(url)
        self.__dificultad = ""
        self.cancion = QMediaPlayer()
        self.cancion.setMedia(content)
        self.esta_pausada = False
        self.__duracion = duracion
        self.__tiempo_entre_pasos = tiempo_entre_pasos
        self.aprobacion_necesaria = aprobacion_necesaria
        self.puntaje = 0
        self.aprobacion = 0
        self.__combo = 0
        self.__combo_maximo = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.pasos_generados = set()
        self.nivel_comenzado = False
        self.flechas_capturadas = {
            "normal": 0,
            "x2": 0,
            "dorada": 0,
            "hielo": 0,
        }
        self.rect_zona_captura = QRect(20, 550, 200, 50)
        # generador de pasos
        self.generador_pasos = GeneradorPasos(self.tiempo_entre_pasos, ronda=self)
        # Timer duracion
        self.timer = QTimer()
        self.timer.setInterval(self.duracion * 1000)
        self.timer.timeout.connect(self.terminar)

        # Timer barras de progreso
        self.timer_barras = QTimer()
        self.timer_barras.setInterval(p.TASA_REFRESCO * 1000)
        self.timer_barras.timeout.connect(self.actualizar_progreso_aprobacion)

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, string):
        self.__dificultad = string
        if string == "Principiante":
            self.generador_pasos.pasos_dobles = False
            self.generador_pasos.pasos_triples = False
        elif string == "Aficionado":
            self.generador_pasos.pasos_dobles = True
            self.generador_pasos.pasos_triples = False
        elif string == "Maestro Cumbia":
            self.generador_pasos.pasos_dobles = True
            self.generador_pasos.pasos_triples = True

    @property
    def combo(self):
        return self.__combo

    @combo.setter
    def combo(self, valor):
        self.__combo = valor

        # Actualiza el combo maximo
        if self.combo > self.combo_maximo:
            self.combo_maximo = self.combo
        self.senal_actualizar_combo.emit(self.combo)

    @property
    def combo_maximo(self):
        return self.__combo_maximo

    @combo_maximo.setter
    def combo_maximo(self, valor):
        self.__combo_maximo = valor
        self.senal_actualizar_combo_maximo.emit(self.combo)

    @property
    def aprobacion(self):
        return self.__aprobacion

    @aprobacion.setter
    def aprobacion(self, valor):
        self.__aprobacion = valor
        self.senal_actualizar_aprobacion.emit(valor)

    @property
    def progreso(self):
        return self.__progreso

    @progreso.setter
    def progreso(self, valor):
        self.__progreso = valor
        self.senal_actualizar_progreso.emit(valor)

    @property
    def tiempo_entre_pasos(self):
        return self.__tiempo_entre_pasos

    @tiempo_entre_pasos.setter
    def tiempo_entre_pasos(self, valor):
        self.__tiempo_entre_pasos = valor
        print("Cambiando tiempo entre pasos")
        print(self.tiempo_entre_pasos)
        self.generador_pasos.tiempo_entre_pasos = valor

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        self.__duracion = valor
        self.timer.setInterval(valor * 1000)

    def comenzar(self):
        print("Ronda Comenzada")
        self.nivel_comenzado = True
        self.timer.start()
        self.timer_barras.start()
        self.cancion.play()
        self.generador_pasos.start()

    def pausar(self):
        self.esta_pausada = True
        self.generador_pasos.stop()
        for paso in self.pasos_generados:
            paso.stop()
        self.timer_barras.stop()
        self.cancion.pause()
        tiempo_restante = self.timer.remainingTime()
        self.timer.stop()
        # crea un timer nuevo con el tiempo que quedaba
        self.timer = QTimer()
        self.timer.setInterval(tiempo_restante)
        self.timer.timeout.connect(self.terminar)

    def reanudar(self):
        self.esta_pausada = False
        for paso in self.pasos_generados:
            paso.start()
        self.timer.start()
        self.timer_barras.start()
        self.generador_pasos.start()
        self.cancion.play()

    def terminar(self, interrumpido=False):
        if interrumpido:
            self.nivel_interrupido = True
        else:
            self.nivel_interrupido = False
        print("Ronda Terminada")
        self.nivel_comenzado = False
        self.timer.stop()
        self.timer_barras.stop()
        self.cancion.stop()
        self.generador_pasos.stop()
        # Espera a que pasen todas las flechas
        self.timer_flechas_restantes = QTimer()
        self.timer_flechas_restantes.setInterval((500 / p.VELOCIDAD_FLECHA) * 1000)
        self.timer_flechas_restantes.setSingleShot(True)
        self.timer_flechas_restantes.timeout.connect(self.terminar_2)
        self.timer_flechas_restantes.start()

    def terminar_2(self):
        self.calcular_puntaje()
        self.senal_calcular_estadisticas.emit(self.puntaje, self.combo_maximo,
                                              self.pasos_incorrectos, self.aprobacion,
                                              self.nivel_interrupido)
        self.nivel_interrupido = False                                            
        self.reiniciar_estadisticas()

    def calcular_puntaje(self):
        flechas_normales = self.flechas_capturadas["normal"]
        flechas_x2 = self.flechas_capturadas["x2"]
        flechas_doradas = self.flechas_capturadas["dorada"]
        flechas_hielo = self.flechas_capturadas["hielo"]
        suma_flechas = flechas_normales + (p.MULT_FLECHA_X2 * flechas_x2)\
            + (p.MUTL_FLECHA_DORADA * flechas_doradas) + flechas_hielo
        self.puntaje = self.combo_maximo * suma_flechas * p.PUNTOS_FLECHA

    def reiniciar_estadisticas(self):
        self.puntaje = 0
        self.aprobacion = 0
        self.progreso = 0
        self.combo = 0
        self.combo_maximo = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.flechas_capturadas = {
            "normal": 0,
            "x2": 0,
            "dorada": 0,
            "hielo": 0,
        }

    def revisar_teclas(self, teclas):
        print("REVISANDO TECLAS")
        if teclas.issubset({p.FLECHA_DERECHA, p.FLECHA_IZQUIERDA, p.FLECHA_ABAJO, p.FLECHA_ARRIBA}):
            pasos = self.pasos_en_zona_captura()
            if pasos:
                for paso in pasos:
                    paso_correcto = self.revisar_paso(paso, teclas)
                    if paso_correcto:
                        paso.realizado = True
                        self.pasos_correctos += 1
                        self.combo += 1
                    else:
                        self.pasos_incorrectos += 1
                        self.combo = 0
            else:  # En caso de que no hayan pasos en la zona de captura
                self.pasos_incorrectos += 1
                self.combo = 0

    def pasos_en_zona_captura(self):
        print("REVISANDO PASOS ZONA CAPTURA")
        pasos_en_zona = set()
        pasos = self.pasos_generados
        for paso in pasos:
            if paso.rect.intersects(self.rect_zona_captura):
                pasos_en_zona.add(paso)
        print(pasos_en_zona)
        return(pasos_en_zona)

    def revisar_paso(self, paso, teclas):
        print("Revisando Paso")
        """
        Determina si un paso es correcto o incorrecto y además realiza las acciones
        necesarias para las flechas que se encuentran dentro del paso dadas las teclas
        presionadas
        """
        paso_correcto = False
        set_true_false = set()  # Determinara si se cumplieron todos los pasos
        for flecha in paso.flechas:
            flecha_es_correcta = self.revisar_flecha(flecha, teclas)
            set_true_false.add(flecha_es_correcta)
        if False in set_true_false:  # Caso en que hay flechas incorrectas
            return False
        elif len(teclas) > len(paso.flechas):  # Caso presiona teclas ademas de las correctas
            return False
        elif paso.realizado:  # Caso vuelve a capturar el mismo paso
            return False
        else:
            self.senal_paso_correcto.emit(paso.flechas)
            return True

    def revisar_flecha(self, flecha, teclas):
        print("Revisando Flechas")
        direcciones = {
            "derecha": p.FLECHA_DERECHA, "izquierda": p.FLECHA_IZQUIERDA,
            "arriba": p.FLECHA_ARRIBA, "abajo": p.FLECHA_ABAJO
        }
        if direcciones[flecha.direccion] in teclas:
            flecha.capturar()
            tipo = flecha.tipo
            self.flechas_capturadas[f"{tipo}"] += 1
            return True
        else:
            return False

    def actualizar_progreso_aprobacion(self):
        tiempo_restante = self.timer.remainingTime() / 1000
        self.progreso = int(((self.duracion - tiempo_restante) / self.duracion) * 100)
        self.aprobacion = self.calcular_aprobacion()

    def calcular_aprobacion(self):
        try:
            pasos_totales = (self.pasos_correctos + self.pasos_incorrectos)
            aprobacion = p.MULTIPLCIADOR_APROBACION * \
                ((self.pasos_correctos - self.pasos_incorrectos) / pasos_totales)
        except ZeroDivisionError:
            aprobacion = 0

        return aprobacion

    def cheat_jugar_solo(self, tiempo):
        print("COMENZANDO CHEAT")
        self.timer_solo = QTimer()
        self.timer_solo.setInterval((p.TASA_REFRESCO * 6) * 1000)
        self.timer_solo.timeout.connect(self.jugar_solo)
        self.timer_solo.start()

        self.timer_cheat = QTimer()
        self.timer_cheat.setInterval(tiempo * 1000)
        self.timer_cheat.setSingleShot(True)
        self.timer_cheat.timeout.connect(self.timer_solo.stop)
        self.timer_cheat.start()

    def jugar_solo(self):
        direccion_a_flecha = {"derecha": p.FLECHA_DERECHA, "izquierda": p.FLECHA_IZQUIERDA,
                              "arriba": p.FLECHA_ARRIBA, "abajo": p.FLECHA_ABAJO}
        pasos_en_zona = self.pasos_en_zona_captura()
        teclas_automaticas = set()
        if pasos_en_zona:
            for paso in pasos_en_zona:
                if paso.realizado:
                    continue
                for flecha in paso.flechas:
                    direccion = flecha.direccion
                    tecla = direccion_a_flecha[direccion]
                    teclas_automaticas.add(tecla)
                self.revisar_teclas(teclas_automaticas)
                print(f"TECLAS ENVIADAS: {teclas_automaticas}")
                teclas_automaticas = set()
