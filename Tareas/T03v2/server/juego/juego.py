from juego.entidades.usuario import Usuario
from juego.entidades.banco import Banco
from juego.items.construcciones import Choza, Ciudad
from juego.mapa.mapa import Mapa
from networking import interfaz_network, thread_revisar_comandos
from threading import Event, Thread
from collections import deque
import random
import json

with open("parametros.json") as file:
    PARAMETROS = json.load(file)


class Juego:

    def __init__(self, nombres_usuarios):
        self.usuarios = [Usuario(nombre_usuario) for nombre_usuario in nombres_usuarios]
        self.cola_turnos = deque()
        self.jugador_actual = None
        for usuario in self.usuarios:
            self.cola_turnos.append(usuario)
        self.dados = [int, int]
        self.event_dados_lanzados = Event()
        self.event_accion_realizada = Event()
        self.event_monopolio = Event()
        self.banco = Banco()
        self.mapa = Mapa()
        # Empieza a revisar los comandos de los usuarios
        self.comandos = {
            "throw_dices": self.lanzar_dados,
            "buy_development_card": self.comprar_carta_desarrollo,
            "activate_development_card": self.activar_carta_desarrollo,
            "pass_turn": self.pasar_turno
        }
        self.thread_comandos = Thread(name="thread_revisar_comandos",
                                      target=thread_revisar_comandos,
                                      args=(self.comandos, ),
                                      daemon=True)
        self.thread_comandos.start()
        self.fase_inicio()
        self.fase_juego()

    def fase_inicio(self):
        random.shuffle(self.cola_turnos)
        self.mapa.cargar_mapa()
        self.construir_construcciones_iniciales()
        self.banco.repartir_cartas_iniciales(self.mapa)

    def construir_construcciones_iniciales(self):
        lista_nodos = list(self.mapa.nodos.keys())
        for usuario in self.usuarios:
            for _ in range(PARAMETROS["CANTIDAD_CHOZAS_INICIALES"]):
                choza = Choza(usuario)
                while True:
                    id_nodo = random.choice(lista_nodos)
                    if self.mapa.anadir_construccion(choza, id_nodo, inicial=True):
                        break

    def fase_juego(self):
        interfaz_network.send_command_to_all("close_wait_window")
        interfaz_network.send_command_to_all("open_game_window")
        ganador = self.ganador()
        while not ganador:
            self.comenzar_turno()
            ganador = self.ganador()

    def comenzar_turno(self):
        self.jugador_actual = self.cola_turnos.popleft()
        interfaz_network.send_command_to_all("update_current_player", self.jugador_actual.nombre)
        interfaz_network.send_command(self.jugador_actual.nombre, "enable_dice_throw")
        # Espera a que se lanzen los dados y resetea el evento
        self.event_dados_lanzados.wait()
        self.event_dados_lanzados.clear()
        # Reparte las cartas y lo deja jugar
        self.banco.repartir_cartas(self.mapa, self.suma_dados())
        interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")
        self.event_accion_realizada.wait()
        self.event_accion_realizada.clear()
        self.cola_turnos.append(self.jugador_actual)

    def lanzar_dados(self):
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.dados[0] = dado_1
        self.dados[1] = dado_2
        interfaz_network.send_command_to_all("update_dices", dado_1, dado_2)
        self.event_dados_lanzados.set()

    def suma_dados(self):
        suma = self.dados[0] + self.dados[1]
        return suma

    def comprar_carta_desarrollo(self):
        self.carta_desarrollo = self.banco.comprar_carta_desarrollo(self.jugador_actual)
        if self.carta_desarrollo:
            if self.carta_desarrollo.tipo == "punto_victoria":
                interfaz_network.send_command(self.jugador_actual.nombre,
                                              "open_victory_dialog",
                                              self.carta_desarrollo.ruta_label)
            elif self.carta_desarrollo.tipo == "monopolio":
                interfaz_network.send_command(self.jugador_actual.nombre,
                                              "open_monopoly_dialog",
                                              self.carta_desarrollo.ruta_label)
        else:
            interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")

    def activar_carta_desarrollo(self, materia_prima=None):
        if self.carta_desarrollo.tipo == "punto_victoria":
            self.carta_desarrollo.activar(self.jugador_actual)
        elif self.carta_desarrollo.tipo == "monopolio":
            self.carta_desarrollo.activar(self.jugador_actual, materia_prima, self.usuarios)
        self.carta_desarrollo = None
        self.event_accion_realizada.set()

    def pasar_turno(self):
        self.event_accion_realizada.set()

    def ganador(self):
        for usuario in self.cola_turnos:
            if usuario.puntos >= PARAMETROS["PUNTOS_VICTORIA_FINALES"]:
                print("Enviar comando notificar ganador")
                print("Enviar comando abrir popup de volver a jugar")
                return usuario.nombre
        return False
