import os
from PyQt5.QtCore import QObject, pyqtSignal
import parametros as p
from entidades.flechas import GeneradorFlecha
import sys


class Nivel(QObject):
    senal_flechas_en_zona_captura = pyqtSignal(set)
    senal_actualizar_combo = pyqtSignal(int)
    senal_actualizar_combo_maximo = pyqtSignal(int)

    def __init__(self, duracion, tiempo_entre_pasos, aprobacion_necesaria):
        super().__init__()
        self.__combo = 0
        self.__combo_maximo = 0
        self.aprobacion_necesaria = aprobacion_necesaria
        self.tiempo_entre_pasos = tiempo_entre_pasos
        self.duracion = duracion
        self.flechas_capturadas = set()

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

    def flechas_en_zona_captura(self, ventana_nivel):
        flechas_en_zona = set()
        flechas = ventana_nivel.generador_flechas.flechas
        for flecha in flechas:
            for zona_captura in ventana_nivel.zonas_captura:
                if flecha.colider.intersects(zona_captura.colider):
                    flechas_en_zona.add(flecha)
        return(flechas_en_zona)

    def capturar_flechas(self, set_flechas):
        for flecha in set_flechas:
            flecha.capturar()
            self.combo += 1
            self.flechas_capturadas.add(flecha)

    def sumar_puntos(self):
        pass

    def manejar_tecla(self, ventana_nivel, tecla):
        # Revisa que la tecla sea del WASD (agregar espacion despues)
        teclas = {p.FLECHA_DERECHA, p.FLECHA_izquierda, p.FLECHA_ARRIBA, p.FLECHA_ABAJO}
        if tecla in teclas:
            flechas = self.flechas_en_zona_captura(ventana_nivel)
            self.revisar_flechas_tecleadas(tecla, flechas)
            paso_correcto = self.revisar_paso(tecla, flechas)
            if not(paso_correcto):
                self.combo = 0
        else:
            # En caso de que presione una tecla fuera del WASD la omite
            pass

    def revisar_flechas_tecleadas(self, tecla, flechas):
        for flecha in flechas:
            if self.revisar_flecha_tecleada(tecla, flecha):
                flecha.capturar()

    def revisar_flecha_tecleada(self, tecla, flecha):
        if tecla == p.FLECHA_ARRIBA and (flecha.direccion == "arriba"):
            return True
        elif tecla == p.FLECHA_ABAJO and (flecha.direccion == "abajo"):
            return True
        elif tecla == p.FLECHA_DERECHA and (flecha.direccion == "derecha"):
            return True
        elif tecla == p.FLECHA_izquierda and (flecha.direccion == "izquierda"):
            return True
        else:
            return False

    def revisar_paso(self, tecla, flechas):
        if flechas:
            for flecha in flechas:
                if tecla == p.FLECHA_ARRIBA and (flecha.direccion == "arriba"):
                    return True
                elif tecla == p.FLECHA_ABAJO and (flecha.direccion == "abajo"):
                    return True
                elif tecla == p.FLECHA_DERECHA and (flecha.direccion == "derecha"):
                    return True
                elif tecla == p.FLECHA_izquierda and (flecha.direccion == "izquierda"):
                    return True
            # En caso de que ninguna flecha calza con la tecla retorna false
            return False
        else:
            return False


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


if __name__ == "__main__":
    procesador = ProcesadorRanking()
    print(procesador.ordenar_puntajes())
