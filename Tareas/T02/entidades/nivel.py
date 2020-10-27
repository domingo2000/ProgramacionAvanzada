from PyQt5.QtCore import QObject, pyqtSignal, QRect, QTimer
from PyQt5.QtMultimedia import QSound
from entidades.pasos import GeneradorPasos
from backend.funciones import sleep
from os import path
import parametros as p
import sys


class Nivel(QObject):
    contador = 1

    senal_pasos_en_zona_captura = pyqtSignal(set)
    senal_actualizar_combo = pyqtSignal(int)
    senal_actualizar_combo_maximo = pyqtSignal(int)
    senal_actualizar_progreso = pyqtSignal(int)
    senal_actualizar_aprobacion = pyqtSignal(int)
    senal_juego_terminado = pyqtSignal()
    senal_esconder_juego = pyqtSignal()
    senal_abrir_ventana_resumen = pyqtSignal(int, int, int, int, int, str, str)
    senal_escribir_puntaje_en_ranking = pyqtSignal(int)
    senal_enviar_dinero = pyqtSignal(int)
    senal_nivel_comenzado = pyqtSignal()
    senal_nivel_terminado = pyqtSignal()

    def __init__(self,
                 ventana_contenedora):
        super().__init__()
        self.numero = Nivel.contador
        Nivel.contador += 1
        self.__combo = 0
        self.__combo_maximo = 0
        self.__pasos_correctos = 0
        self.__pasos_incorrectos = 0
        self.__puntaje = 0
        self.puntaje_acumulado = 0
        self.pasos_totales = 0
        self.flechas_capturadas = {
            "normal": 0,
            "x2": 0,
            "dorada": 0,
            "hielo": 0,
        }
        self.__aprobacion = 0
        self.__progreso = 0
        self.aprobacion_necesaria = None
        self.tiempo_entre_pasos = None
        self.__duracion = None
        self.pasos_dobles = False
        self.pasos_triples = False
        self.pasos_actuales = set()
        self.pasos_capturados = set()
        self.ventana_contenedora = ventana_contenedora
        self.nivel_cargado = False

        # Musica
        self.cancion = None
        # Entidades para funcionamiento
        # Timer nivel que revisa el termino de este
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.terminar)

        # Timer que actualiza la barra de progreso y aprobacion
        self.timer_actualizador = QTimer()
        self.timer_actualizador.setInterval(p.TASA_DE_REFRESCO)
        self.timer_actualizador.timeout.connect(self.actualizar_progreso_aprobacion)
        # Generador
        self.generador_pasos = None
        self.colider_zona_captura = QRect(*p.UBICACION_VENTANAS["zona_captura"],
                                          *p.TAMANO_VENTANAS["zona_captura_2"])

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        self.__duracion = valor
        self.timer.setInterval(valor * 1000)

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
    def pasos_correctos(self):
        return self.__pasos_correctos

    @pasos_correctos.setter
    def pasos_correctos(self, valor):
        self.__pasos_correctos = valor
        self.pasos_totales += 1

    @property
    def pasos_incorrectos(self):
        return self.__pasos_incorrectos

    @pasos_incorrectos.setter
    def pasos_incorrectos(self, valor):
        self.__pasos_incorrectos = valor

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
    def puntaje(self):
        return self.__puntaje

    @puntaje.setter
    def puntaje(self, valor):
        self.__puntaje = valor
        self.puntaje_acumulado += self.puntaje

    def crear_generador(self):
        self.generador_pasos = GeneradorPasos(self.tiempo_entre_pasos, self.ventana_contenedora,
                                              self.pasos_dobles, self.pasos_triples)

    def comenzar(self):
        self.reiniciar_estadisticas()
        self.timer.start()
        self.timer_actualizador.start()
        print("Comenzando Nivel :)")
        self.generador_pasos.comenzar()
        self.cancion.play()
        self.senal_nivel_comenzado.emit()

    def terminar(self):
        print("Terminando Nivel")
        # Esperar a que no hayan flechas
        # Completar parar_cancion
        self.generador_pasos.parar()
        sleep(p.TAMANO_VENTANAS["ventana_nivel"][1] / p.VELOCIDAD_FLECHA)
        self.cancion.stop()
        self.timer.stop()
        self.timer_actualizador.stop()
        # mostrar_ventana_resumen
        self.calcular_ventana_resumen()
        self.senal_enviar_dinero.emit(self.puntaje)
        self.senal_nivel_terminado.emit()

    def destruir_label(self, label):
        label.setParent(None)

    def pasos_en_zona_captura(self):
        pasos_en_zona = set()
        pasos = self.generador_pasos.pasos
        for paso in pasos:
            if paso.colider.intersects(self.colider_zona_captura):
                pasos_en_zona.add(paso)
        return(pasos_en_zona)

    def manejar_teclas(self, teclas):
        """
        Recibe la señal de teclas presionadas donde ventana_nivel es la
        ventana del nivel que se esta jugando, y teclas es un set con las teclas
        presionadas
        """
        if not(self.generador_pasos):
            return None
        if teclas.issubset({p.FLECHA_DERECHA, p.FLECHA_izquierda, p.FLECHA_ABAJO, p.FLECHA_ARRIBA}):
            pasos = self.pasos_en_zona_captura()
            if pasos:
                for paso in pasos:
                    paso_correcto = self.manejar_paso(paso, teclas)
                    print(f"DEBUG paso Correcto = {paso_correcto}")
                    if paso_correcto:
                        self.pasos_correctos += 1
                        self.combo += 1
                    else:
                        self.pasos_incorrectos += 1
                        self.combo = 0
            else:  # En caso de que no hayan pasos en la zona de captura
                self.pasos_incorrectos += 1
                self.combo = 0

    def manejar_paso(self, paso, teclas):
        """
        Determina si un paso es correcto o incorrecto y además realiza las acciones
        necesarias para las flechas que se encuentran dentro del paso dadas las teclas
        presionadas
        """
        paso_correcto = False
        set_true_false = set()  # Determinara si se cumplieron todos los pasos
        for flecha in paso.flechas:
            flecha_es_correcta = self.manejar_flecha(flecha, teclas)
            set_true_false.add(flecha_es_correcta)
        if False in set_true_false:  # Caso en que hay flechas incorrectas
            return False
        elif len(teclas) > len(paso.flechas):  # Caso presiona teclas ademas de las correctas
            return False
        else:
            return True

    def manejar_flecha(self, flecha, teclas):
        direcciones = {
            "derecha": p.FLECHA_DERECHA,
            "izquierda": p.FLECHA_izquierda,
            "arriba": p.FLECHA_ARRIBA,
            "abajo": p.FLECHA_ABAJO
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
            aprobacion = p.MULTIPLCIADOR_APROBACION * \
                ((self.pasos_correctos - self.pasos_incorrectos) / self.pasos_totales)
        except ZeroDivisionError:
            aprobacion = 0

        return aprobacion

    def calcular_ventana_resumen(self):
        self.actualizar_puntaje()

        if self.aprobacion < self.aprobacion_necesaria:
            mensaje = "Andate de la DCC Cumbia eres horrible para este juego"
            self.senal_escribir_puntaje_en_ranking.emit(self.puntaje_acumulado)
            ventana_a_volver = "ventana_inicio"
            self.senal_esconder_juego.emit()
            self.senal_abrir_ventana_resumen.emit(self.puntaje, self.puntaje_acumulado,
                                                  self.combo_maximo, self.pasos_incorrectos,
                                                  self.aprobacion, mensaje, ventana_a_volver)
            self.senal_juego_terminado.emit()
        else:
            mensaje = "Eres el bailarin Maestro, podras demostrar tu valia otra ronda"
            ventana_a_volver = "ventana_juego"
            self.senal_esconder_juego.emit()
            self.senal_abrir_ventana_resumen.emit(self.puntaje, self.puntaje_acumulado,
                                                  self.combo_maximo, self.pasos_incorrectos,
                                                  self.aprobacion, mensaje, ventana_a_volver)

    def reiniciar_estadisticas(self):
        self.combo = 0
        self.combo_maximo = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.pasos_totales = 0
        self.flechas_capturadas = {
            "normal": 0,
            "x2": 0,
            "dorada": 0,
            "hielo": 0,
        }
        self.aprobacion = 0
        self.progreso = 0

    def actualizar_puntaje(self):  # Calcula y actualiza el puntaje
        suma_flechas = 0
        for tipo_flecha, numero in self.flechas_capturadas.items():
            if tipo_flecha == "normal":
                puntos = numero * 1
            elif tipo_flecha == "x2":
                puntos = numero * p.MULTIPLICADOR_PUNTOS_FLECHA_x2
            elif tipo_flecha == "dorada":
                puntos = numero * p.MULTIPLICADOR_PUNTOS_FLECHA_DORADA
            elif tipo_flecha == "hielo":
                puntos = numero * 1
            suma_flechas += puntos

        self.puntaje = self.combo_maximo * suma_flechas * p.PUNTOS_FLECHA

    def terminar_interrumpidamente(self):
        if self.timer.isActive():  # En caso de que este en medio de una ronda
            self.actualizar_puntaje()
        else:  # En caso de que este entre rondas
            pass

        if self.nivel_cargado:
            self.generador_pasos.parar()
            self.cancion.stop()
        self.timer.stop()
        self.timer_actualizador.stop()
        self.senal_escribir_puntaje_en_ranking.emit(self.puntaje_acumulado)
        self.reiniciar_estadisticas()
        self.borrar_juego()

    def borrar_juego(self):
        self.puntaje_acumulado = 0

    def setear_nivel_cargado(self, bool):
        self.nivel_cargado = bool

    def __repr__(self):
        string = f"Nivel_Object generado numero {self.numero}"
        return string
