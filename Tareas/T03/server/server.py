import socket
from threading import Thread
import json
import pickle
from faker import Faker
from banco import Banco
from mapa.mapa import Mapa
import time


class Server():

    def __init__(self, host, port):
        print("Inicializando Servidor")
        super().__init__()
        self.init_net(host, port)
        # Atributos del juego
        self.usuarios = []
        self.banco = Banco()
        self.mapa = Mapa()

        self.comandos = {
            "comprar_choza": self.banco.comprar_choza,
            "comprar_carretera": self.banco.comprar_carretera,
            "comprar_desarrollo": self.banco.comprar_desarrollo
        }

    def init_net(self, host, port):
        print("Inicializando Net Server")
        super().__init__()
        self.host = host
        self.port = port
        self.faker = Faker()
        self.clientes = {}
        # Crea el socket del servidor
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta el socket al puerto y host
        self.bind_and_listen()
        # Crea el thread de aceptar clientes
        self.crear_thread_aceptar_clientes()

    # METODOS DE NETWORKING ###

    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")

    def aceptar_usuario(self, usuario, client_socket, booleano):
        print("Aceptando usuario")
        """
        Se encarga de aceptar o rechazar al usuario segun el booleano
        ademas le envia al usuario un mensaje por si se acepto o rechazo
        y crea el thread de escucha al usuario en caso de ser aceptado
        """
        self.clientes[usuario] = client_socket
        if booleano:
            self.send_message("aceptado", usuario)
            # Crea el thread de escucha
            thread_escucha = Thread(target=self.thread_escucha_usuario,
                                    args=(client_socket, ),
                                    daemon=True)
            thread_conexion = Thread(target=self.thread_verificar_conexion,
                                     args=(usuario, ),
                                     daemon=True)
            thread_escucha.start()
            thread_conexion.start()
            # Envia el log de conexion exitosa
            self.log(usuario, "conectado", "aceptado")
            self.actualizar_usuarios()
        else:
            self.send_message("rechazado", usuario)
            # Remueve el usuario de la lista de clientes
            del self.clientes[usuario]
            self.log(usuario, "conectado", "rechazado")

    def lleno(self):
        if len(self.clientes) >= 4:
            return True
        else:
            return False

    def crear_usuario(self):
        print("Creando usuario")
        usuario = self.faker.name()
        print(usuario)
        return usuario

    def crear_comando(self, string, list):
        comando = (string, list)
        return comando

    def crear_thread_aceptar_clientes(self):
        print("Creando Thread Aceptar Clientes")
        thread = Thread(target=self.thread_aceptar_clientes)
        thread.start()

    def thread_aceptar_clientes(self):
        while True:
            print("Aceptando Clientes")
            client_socket, ip = self.socket_server.accept()
            print("Cliente aceptado")
            usuario = self.crear_usuario()
            servidor_lleno = self.lleno()
            if servidor_lleno:  # Rechaza al usuario
                self.aceptar_usuario(usuario, client_socket, False)
                # Codigo Comenzar Juego
                self.log("Server", "Comenzando Juego")
            else:  # Acepta al usuario
                self.aceptar_usuario(usuario, client_socket, True)
                # Si se lleno con el nuevo usuario inicial la partida
                if self.lleno():
                    self.iniciar_partida()

    def thread_escucha_usuario(self, socket_cliente):
        # Completar thread de escucha de usuario
        pass

    def thread_verificar_conexion(self, usuario):
        while True:
            time.sleep(1)
            try:
                self.send_command("", [None], usuario)
            except KeyError:
                break

    def log(self, nombre_usuario="-", evento="-", detalles="-"):
        print(f"{nombre_usuario: ^25} | {evento: ^25} | {detalles: ^25}")

    def send_bytes(self, bytes, usuario):
        """
        Envía bytes con el protocolo del enunciado al usuario dado

        """
        bytes = bytes
        largo_mensaje = len(bytes)
        # Rellena con ceros
        ceros = bytearray(60 - (largo_mensaje % 60))
        bytes += ceros
        data = bytearray()
        # Primeros 4 bytes
        data.extend(largo_mensaje.to_bytes(4, byteorder="big"))

        num_chunks = (largo_mensaje // 60) + 1
        for i in range(num_chunks):
            # Numero del bloque
            n = i.to_bytes(4, byteorder="little")
            data.extend(n)
            # Chunk de informacion
            chunk_bytes = bytes[i * 60: (i + 1) * 60]
            data.extend(chunk_bytes)

        socket_cliente = self.clientes[usuario]

        try:
            socket_cliente.sendall(data)
        except ConnectionError:
            self.desconectar_usuario(usuario)

    def send_message(self, mensaje, usuario):
        self.send_bytes(mensaje.encode("utf-8"), usuario)
        if mensaje != "":
            self.log(usuario, "mensaje", mensaje)

    def send_command(self, comando, parametros, usuario):
        """
        Envia un comando serializado al usuario de la forma
        tupla: ("comando": (parametros))

        los parametros son recibidos como una lista de parametros
        """
        tupla = (comando, parametros)
        tupla_serializado = pickle.dumps(tupla)
        self.send_bytes(tupla_serializado, usuario)
        if comando != "":
            self.log("Server", "enviar_comando", usuario)

    def send_command_to_all(self, comando, parametros):
        """
        Envia un comando serializado a todos los usuarios
        parametros recibidos como lista [a, b, c]
        """
        for usuario in self.clientes.copy():
            self.send_command(comando, parametros, usuario)

    def realizar_comando(self, tupla_comando):
        comando = tupla_comando[0]
        print(f"Realizando comando: {comando}")
        parametros = tupla_comando[1]
        if comando in self.comandos:
            metodo = self.comandos[comando]
            print(parametros)
            metodo(*parametros)
            print(f"Comando Realizado: {comando}")

    def recive_data(self):
        """
        Recibe datos con el protocolo del enunciado, en caso de ser
        un byte vacio pasa, si otra cosa ejecuta el comando.
        """
        # Protocolo de informacion
        data = bytearray()
        bytes_largo = self.socket_client.recv(4)
        largo_bytes = int.from_bytes(bytes_largo, byteorder="big")
        numero_chunks = (largo_bytes // 60) + 1
        for i in range(numero_chunks):
            numero_bloque = self.socket_client.recv(4)
            data_bloque = self.socket_client.recv(60)
            if i == (numero_chunks - 1):
                data_bloque = data_bloque[0: (largo_bytes % 60)]
            data.extend(data_bloque)

        if data == "":
            pass
        else:
            # Completar ejecutar comando
            pass

    def desconectar_usuario(self, usuario):
        socket_cliente = self.clientes.pop(usuario)
        self.send_command_to_all("actualizar_usuarios", [list(self.clientes.copy().keys())])
        socket_cliente.close()
        self.log(usuario, "Desconectado")

    #  METODOS DEL JUEGO ###

    def iniciar_partida(self):
        self.mapa.cargar_mapa()
        self.send_command_to_all("close_window_wait", [None])
        self.send_command_to_all("open_window_game", [None])
        self.send_command_to_all("cargar_mapa", [self.mapa])

    def actualizar_usuarios(self):
        usuarios = list(self.clientes.keys())
        for usuario in self.clientes:
            self.send_command("actualizar_usuarios", [usuarios], usuario)
