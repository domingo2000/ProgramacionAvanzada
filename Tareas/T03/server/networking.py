import socket
from threading import Thread
import json
import pickle
from faker import Faker


class ServerNet():

    def __init__(self, host, port):
        print("Inicializando Server")
        self.host = host
        self.port = port
        self.stack_comandos = []
        self.comando_realizado = True
        self.faker = Faker()
        self.clientes = {}
        # Crea el socket del servidor
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta el socket al puerto y host
        self.bind_and_listen()
        # Crea el thread de aceptar clientes
        self.crear_thread_aceptar_clientes()

    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")

    def aceptar_usuario(self, usuario, socket_cliente, booleano):
        print("Aceptando usuario")
        """
        Se encarga de aceptar o rechazar al usuario segun el booleano
        ademas le envia al usuario un mensaje por si se acepto o rechazo
        y crea el thread de escucha al usuario en caso de ser aceptado
        """
        self.clientes[usuario] = socket_cliente
        if booleano:
            self.send_message("aceptado", usuario)
            # Crea el thread de escucha
            thread_escucha = Thread(target=self.thread_escucha_usuario,
                                    args=(socket_cliente, usuario, ),
                                    daemon=True)
            thread_escucha.start()
            # Envia el log de conexion exitosa
            self.log(usuario, "conectado", "aceptado")
            self.send_command_to_all("actualizar_usuarios", [list(self.clientes.keys())])
        else:
            self.send_message("rechazado", usuario)
            self.send_command("servidor_lleno", usuario)
            # Remueve el usuario de la lista de clientes
            del self.clientes[usuario]
            self.log(usuario, "conectado", "rechazado")

    def lleno(self):
        if len(self.clientes) >= 1:
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
            socket_cliente, ip = self.socket_server.accept()
            print("Cliente aceptado")
            usuario = self.crear_usuario()
            servidor_lleno = self.lleno()
            if servidor_lleno:  # Rechaza al usuario
                self.aceptar_usuario(usuario, socket_cliente, False)
            else:  # Acepta al usuario
                self.aceptar_usuario(usuario, socket_cliente, True)

    def thread_escucha_usuario(self, socket_cliente, usuario):
        while True:
            try:
                data = self.recive_data(socket_cliente)
                comando = pickle.loads(data)
                self.añadir_comando(comando)
            except ConnectionError:
                self.desconectar_usuario(usuario)
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
        self.log(usuario, "mensaje", mensaje)

    def send_command(self, comando, usuario, parametros=None):
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

    def send_command_to_all(self, comando, parametros=None):
        """
        Envia un comando serializado a todos los usuarios
        parametros recibidos como lista [a, b, c]
        """
        for usuario in self.clientes.copy():
            self.send_command(comando, usuario, parametros)

    def añadir_comando(self, comando):
        self.stack_comandos.append(comando)
        self.comando_realizado = False
        self.log("Server", "Añadido Comando", comando[0])

    def recive_data(self, socket_cliente):
        """
        Recibe datos con el protocolo del enunciado, en caso de ser
        un byte vacio pasa, si otra cosa ejecuta el comando.
        """
        # Protocolo de informacion
        data = bytearray()
        bytes_largo = socket_cliente.recv(4)
        largo_bytes = int.from_bytes(bytes_largo, byteorder="big")
        numero_chunks = (largo_bytes // 60) + 1
        for i in range(numero_chunks):
            numero_bloque = socket_cliente.recv(4)
            data_bloque = socket_cliente.recv(60)
            if i == (numero_chunks - 1):
                data_bloque = data_bloque[0: (largo_bytes % 60)]
            data.extend(data_bloque)

        if data == "":
            pass
        else:
            return data

    def desconectar_usuario(self, usuario):
        socket_cliente = self.clientes.pop(usuario)
        socket_cliente.close()
        self.log(usuario, "Desconectado", usuario)
        self.send_command_to_all("actualizar_usuarios", [list(self.clientes.keys())])


if __name__ == "__main__":
    with open("parametros.json") as file:
        data = json.load(file)
    import time
    import random
    host = data["host"]
    port = data["port"]
    server = ServerNet(host, port)
    while True:
        comando = input("Ingrese el nombre del comando: ")
        parametros = []
        entrada = input("Ingrese un string para parametro: ")
        parametros.append(entrada)
        server.send_command_to_all(comando, parametros)
