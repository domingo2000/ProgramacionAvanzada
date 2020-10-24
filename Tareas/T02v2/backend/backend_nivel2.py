from PyQt5.QtCore import QObject, pyqtSignal
import parametros as p
from entidades.flechas import GeneradorFlecha
import sys


class Nivel(QObject):
    senal_pasos_en_zona_captura = pyqtSignal(set)
    senal_actualizar_combo = pyqtSignal(int)
    senal_actualizar_combo_maximo = pyqtSignal(int)

    def __init__(self, duracion, tiempo_entre_pasos, aprobacion_necesaria):
        super().__init__()
        self.__combo = 0
        self.__combo_maximo = 0
        self.pasos_correctos = 0
        self.pasos_incorrectos = 0
        self.flechas_capturadas = {
            "normal": 0,
            "x2": 0,
            "dorada": 0,
            "hielo": 0,
        }
        self.aprobacion_necesaria = aprobacion_necesaria
        self.tiempo_entre_pasos = tiempo_entre_pasos
        self.duracion = duracion
        self.pasos_actuales = set()
        self.pasos_capturados = set()
        

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

    def pasos_en_zona_captura(self, ventana_nivel):
        pasos_en_zona = set()
        pasos = ventana_nivel.generador_pasos.pasos
        for paso in pasos:
            for zona_captura in ventana_nivel.zonas_captura:
                if paso.colider.intersects(zona_captura.colider):
                    pasos_en_zona.add(paso)
        return(pasos_en_zona)

    def manejar_teclas(self, ventana_nivel, teclas):
        """
        Recibe la señal de teclas presionadas donde ventana_nivel es la
        ventana del nivel que se esta jugando, y teclas es un set con las teclas
        presionadas
        """
        pasos = self.pasos_en_zona_captura(ventana_nivel)
        if pasos:
            for paso in pasos:
                paso_correcto = self.manejar_paso(paso, teclas)
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
        set_true_false = set() # Determinara si se cumplieron todos los pasos
        for flecha in paso.flechas:
            for tecla in teclas:
                flecha_correcta = self.manejar_flecha(flecha, tecla)
                if flecha_correcta:
                    break
            set_true_false.add(flecha_correcta)
        if False in set_true_false:
            return False

    def manejar_flecha(self, flecha, tecla):
        if flecha.direccion == tecla:
            flecha.capturar()
            tipo = flecha.tipo
            self.flechas_capturadas["tipo"] += 1


class NivelPrincipiante(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_PRINCIPIANTE.values())
        self.pasos_dobles = False
        self.pasos_triples = False


class NivelAficionado(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_AFICIONADO.values())
        self.pasos_dobles = True
        self.pasos_triples = False


class NivelMaestroCumbia(Nivel):

    def __init__(self):
        super().__init__(*p.NIVEL_MAESTRO_CUMBIA.values())
        self.pasos_dobles = True
        self.pasos_triples = True
