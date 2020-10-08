import random
import time
from threading import Thread, Event, Lock, Timer

from parametros import (PROB_IMPOSTOR, PROB_ARREGLAR_SABOTAJE,
                        TIEMPO_ENTRE_TAREAS, TIEMPO_TAREAS, TIEMPO_SABOTAJE,
                        TIEMPO_ENTRE_ACCIONES, TIEMPO_ESCONDITE)

from funciones import (elegir_accion_impostor, print_progreso, print_anuncio,
                       print_sabotaje, cargar_sabotajes, print_explosión)


class Tripulante(Thread):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas):
        # No modificar
        super().__init__(daemon=True)
        self.color = color
        self.tareas = tareas
        self.esta_vivo = True
        self.diccionario_tareas = diccionario_tareas
        self.evento_sabotaje = evento_sabotaje
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        
        while self.esta_vivo and (len(self.tareas) > 0):
            if not(self.evento_sabotaje.is_set()):
                self.hacer_tarea()
                time.sleep(TIEMPO_ENTRE_TAREAS)  # Descanso del tripulante
            else:  # Arregla el sabotaje
                if random.random() < PROB_ARREGLAR_SABOTAJE:
                    self.arreglar_sabotaje()
                else:
                    time.sleep(TIEMPO_ENTRE_TAREAS)

    def hacer_tarea(self):
        nombre_tarea = random.choice(self.tareas)
        tarea = self.diccionario_tareas[nombre_tarea]
        with tarea["lock"]:
            tiempo = random.uniform(TIEMPO_TAREAS[0], TIEMPO_TAREAS[1])
            step_tiempo = tiempo / 5
            for i in range(5):
                if self.esta_vivo:
                    print_progreso(self.color, f"Realizando {nombre_tarea}", 25 * i)
                    time.sleep(step_tiempo)
                else:
                    print(f"El triulante {self.color} esta muerto")
                    break
            self.tareas.remove(nombre_tarea)
            self.diccionario_tareas[nombre_tarea]["realizado"] = True

    def arreglar_sabotaje(self):
        print_anuncio(self.color, "Ha comenzado a reparar el sabotaje")
        tiempo = random.uniform(TIEMPO_SABOTAJE[0], TIEMPO_SABOTAJE[1])
        step_tiempo = tiempo / 4
        for i in range(4):
            if self.esta_vivo:
                print_progreso(self.color, "Arreglando Sabotaje", 25 * i)
                time.sleep(step_tiempo)
            else:
                print(f"El tripulante {self.color} esta muerto")
                break
        if self.esta_vivo:
            self.evento_sabotaje.clear()
            print_anuncio(self.color, "Ha Terminado de arreglar el Sabotaje")
        pass


class Impostor(Tripulante):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas, tripulantes, evento_termino):
        # No modificar
        super().__init__(color, tareas, evento_sabotaje, diccionario_tareas)
        self.tripulantes = tripulantes
        self.evento_termino = evento_termino
        self.sabotajes = cargar_sabotajes()
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        # Completar
        pass

    def matar_jugador(self):
        # Completar
        pass

    def sabotear(self):
        # Completar
        pass

    def terminar_sabotaje(self):
        # Completar
        pass


if __name__ == "__main__":
    print("\n" + " INICIANDO PRUEBA DE TRIPULANTE ".center(80, "-") + "\n")
    # Se crea un diccionario de tareas y un evento sabotaje de ejemplos.
    ejemplo_tareas = {
            "Limpiar el filtro de oxigeno": {
                "lock": Lock(),
                "realizado": False,
                "nombre": "Limpiar el filtro de oxigeno"
            }, 
            "Botar la basura": {
                "lock": Lock(),
                "realizado": False,
                "nombre":  "Botar la basura"
            }
        }
    ejemplo_evento = Event()

    # Se intancia un tripulante de color ROJO
    rojo = Tripulante("Rojo", list(ejemplo_tareas.keys()), ejemplo_evento, ejemplo_tareas)

    rojo.start()

    time.sleep(5)
    # ==============================================================
    # Descomentar las siguientes lineas para probar el evento sabotaje.

    # print(" HA COMENZADO UN SABOTAJE ".center(80, "*"))
    # ejemplo_evento.set()

    rojo.join()

    print("\n-" + "="*80 + "\n")
    print(" PRUEBA DE TRIPULANTE TERMINADA ".center(80, "-"))
    if sum((0 if x["realizado"] else 1 for x in ejemplo_tareas.values())) > 0:
        print("El tripulante no logró completar todas sus tareas. ")
    elif ejemplo_evento.is_set():
        print("El tripulante no logró desactivar el sabotaje")
    else:
        print("El tripulante ha GANADO!!!")
