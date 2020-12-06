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
        self.ganador = None
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
            "pass_turn": self.pasar_turno,
            "buy_house": self.comprar_choza,
            "propose_exchange": self.proponer_intercambio,
            "do_exchange": self.realizar_intercambio
        }
        self.thread_comandos = Thread(name="thread_revisar_comandos",
                                      target=thread_revisar_comandos,
                                      args=(self.comandos, ),
                                      daemon=True)
        self.thread_comandos.start()
        self.fase_inicio()
        self.fase_juego()
        self.fase_termino()

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
        while not self.ganador:
            self.comenzar_turno()
        print("TERMINANDO PARTIDA")

    def comenzar_turno(self):
        self.jugador_actual = self.cola_turnos.popleft()
        interfaz_network.send_command_to_all("update_current_player", self.jugador_actual.nombre)
        interfaz_network.send_command(self.jugador_actual.nombre, "enable_dice_throw")
        # Espera a que se lanzen los dados y resetea el evento
        self.event_dados_lanzados.wait()
        self.event_dados_lanzados.clear()
        # Reparte las cartas y lo deja jugar
        if self.suma_dados() == 7:
            self.quitar_materias_primas()
        else:
            self.banco.repartir_cartas(self.mapa, self.suma_dados())
        interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")
        self.event_accion_realizada.wait()
        self.event_accion_realizada.clear()
        self.chequear_ganador(self.jugador_actual)
        self.cola_turnos.append(self.jugador_actual)

    def lanzar_dados(self):
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.dados[0] = dado_1
        self.dados[1] = dado_2
        interfaz_network.send_command_to_all("update_dices", dado_1, dado_2)
        self.event_dados_lanzados.set()

    def quitar_materias_primas(self):
        tipo_materia = ["madera", "arcilla", "trigo"]
        for usuario in self.usuarios:
            cantidad_madera = usuario.mazo["madera"]
            cantidad_trigo = usuario.mazo["trigo"]
            cantidad_arcilla = usuario.mazo["arcilla"]
            cantidad_cartas = cantidad_arcilla + cantidad_madera + cantidad_trigo
            if cantidad_cartas >= 7:
                cantidad_botadas = int(cantidad_cartas / 2)
                for _ in range(cantidad_botadas):
                    materia = random.choice(tipo_materia)
                    while usuario.mazo[materia] <= 0:
                        materia = random.choice(tipo_materia)
                    usuario.mazo[materia] -= 1
                msg = "Has perdido la mitad de tus cartas"
                interfaz_network.send_command(usuario.nombre, "pop_up", msg)

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

    def comprar_choza(self, id_nodo):
        choza = self.banco.comprar_choza(self.jugador_actual)
        if choza:
            if self.mapa.anadir_construccion(choza, id_nodo):  # Chequea los adyacentes
                msg = f"{self.jugador_actual.nombre} ha construido una choza"
                interfaz_network.send_command_to_all("pop_up", msg)
                self.event_accion_realizada.set()
            else:  # Si no se pudo construir se activa la interfaz
                interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")    
        else: # Si no se pudo comprar se activa la itnerfaz
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
                #interfaz_network.send_command_to_all("open_winner_window")
                print("Enviar comando notificar ganador")
                print("Enviar comando abrir popup de volver a jugar")
                return usuario.nombre
        return False

    def chequear_ganador(self, usuario):
        if usuario.puntos >= PARAMETROS["PUNTOS_VICTORIA_FINALES"]:
            self.ganador = usuario

    def fase_termino(self):
        lista_nombres_puntos = [(usuario.nombre, usuario.puntos) for usuario in self.usuarios]
        lista_nombres_puntos.sort(key=lambda tupla: tupla[1], reverse=True)
        interfaz_network.send_command_to_all("update_winner_window", lista_nombres_puntos)
        interfaz_network.send_command_to_all("close_game_window")
        interfaz_network.send_command_to_all("open_winner_window")

    def proponer_intercambio(self, materia_ofrecida, materia_pedida,
                             cant_materia_ofrecida, cant_materia_pedida, jugador_elegido):
        for usuario in self.usuarios:
            if usuario.nombre == jugador_elegido:
                usuario_jugador_elegido = usuario
        mazo_jugador = self.jugador_actual.mazo
        mazo_jugador_elegido = usuario_jugador_elegido.mazo
        if mazo_jugador[materia_ofrecida] < cant_materia_ofrecida:
            msg = "No tienes materias primas para realizar dicho intercambio!"
            interfaz_network.send_command(self.jugador_actual.nombre, "pop_up", msg)
            interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")
        elif mazo_jugador_elegido[materia_pedida] < cant_materia_pedida:
            msg = "El jugador solicitado no tiene la cantidad de materias primas pedidas"
            interfaz_network.send_command(self.jugador_actual.nombre, "pop_up", msg)
            interfaz_network.send_command(self.jugador_actual.nombre, "enable_interface")
        else:
            interfaz_network.send_command(usuario_jugador_elegido.nombre, "see_exchange", 
                                          materia_ofrecida, materia_pedida, cant_materia_ofrecida,
                                          cant_materia_pedida, self.jugador_actual.nombre)
            self.jugador_oferente_intercambio = self.jugador_actual
            self.jugador_elegido_intercambio = usuario_jugador_elegido
            self.materia_ofrecida = materia_ofrecida
            self.materia_pedida = materia_pedida
            self.cant_materia_ofrecida = cant_materia_ofrecida
            self.cant_materia_pedida = cant_materia_pedida

    def realizar_intercambio(self, aceptado):
        if aceptado:
            # Da la materia ofrecida
            self.jugador_oferente_intercambio.mazo[self.materia_ofrecida]\
                -= self.cant_materia_ofrecida
            self.jugador_elegido_intercambio.mazo[self.materia_ofrecida]\
                += self.cant_materia_ofrecida
            # Quita la materia pedida
            self.jugador_oferente_intercambio.mazo[self.materia_pedida]\
                += self.cant_materia_pedida
            self.jugador_elegido_intercambio.mazo[self.materia_pedida]\
                -= self.cant_materia_pedida
            # Notifica el intercambio
            msg = f"Se ha realizado un intercambio entre\
                {self.jugador_oferente_intercambio.nombre} \
                    y {self.jugador_elegido_intercambio.nombre}"
            interfaz_network.send_command_to_all("pop_up", msg)
            # setea none todos los datos del intercambio
            self.jugador_oferente_intercambio = None
            self.jugador_elegido_intercambio = None
            self.materia_ofrecida = None
            self.materia_pedida = None
            self.cant_materia_ofrecida = None
            self.cant_materia_pedida = None
        else:
            msg = "Se ha rechazado el intercambio"
            interfaz_network.send_command(self.jugador_oferente_intercambio.nombre, 
                                          "pop_up", msg)
        self.event_accion_realizada.set()