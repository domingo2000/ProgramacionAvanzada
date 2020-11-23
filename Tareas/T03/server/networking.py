import socket
from threading import Thread
import json
import pickle
from faker import Faker


class ServerNet:
    def __init__(self):
        print("Inicializando Servidor")
        with open("parametros.json", "r") as file:
            data = json.loads(file.read())
        self.host = data["host"]
        self.port = data["port"]
        self.clientes = {}
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.thread_aceptar_clientes()

        # Print Inicio log
        self.inicio_log()

    def bind_and_listen(self):
        """
        Enlaza el socket creado con el host y puerto indicado.

        Primero, se enlaza el socket y luego queda esperando
        por conexiones entrantes.
        """
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")

    def thread_aceptar_clientes(self):
        self.thread_aceptar = Thread(target=self.target_aceptar_clientes)
        self.thread_aceptar.start()

    def target_aceptar_clientes(self):
        while True:
            socket_cliente, ip = self.socket_server.accept()
            usuario = self.crear_usuario(socket_cliente)
            self.log(nombre_usuario=usuario, evento="Conetarse")

    def crear_usuario(self, socket_cliente):
        fake = Faker()
        usuario = fake.name()
        self.clientes[usuario] = socket_cliente

        # Actualiza los usuarios de la sala de espera
        self.actualizar_usuarios()

        # Crea el thread de escucha
        thread_escucha = Thread(target=self.escuchar_cliente,
                                args=(usuario, ),
                                daemon=True)
        thread_escucha.start()
        return usuario

    def actualizar_usuarios(self):
        # Actualiza la interfaz de todos los usuario conectados
        nombres_usuarios = [usuario for usuario in self.clientes]
        for usuario in self.clientes:
            self.send_command("actualizar_usuarios",
                              [nombres_usuarios],
                              usuario)

    def escuchar_cliente(self, usuario):
        while True:
            try:
                # Protocolo de informacion
                data = bytearray()
                socket_cliente = self.clientes[usuario]
                bytes_largo = socket_cliente.recv(4)
                largo_bytes = int.from_bytes(bytes_largo, byteorder="big")
                numero_chunks = (largo_bytes // 60) + 1
                for i in range(numero_chunks):
                    numero_bloque = socket_cliente.recv(4)
                    data_bloque = socket_cliente.recv(60)
                    if i == (numero_chunks - 1):
                        data_bloque = data_bloque[0: (largo_bytes % 60)]
                    data.extend(data_bloque)

                data = data.decode("utf-8")
                self.log(nombre_usuario=usuario, evento="Request", detalles=data)
            except ConnectionError:
                desconectado = self.revisar_desconexion(usuario)
                if desconectado:
                    break

    def revisar_desconexion(self, usuario):
        bytes = "".encode("utf-8")
        desconectado = False
        try:
            self.send_bytes(bytes, usuario)
        except ConnectionError:
            desconectado = True
            self.log(usuario, "Desconectado")
            # Quita al usuario de los clientes conectados y actualiza los clientes
            self.clientes.pop(usuario)
            self.actualizar_usuarios()
        return desconectado

    def send_bytes(self, bytes, usuario):
        """
        Envía bytes con el protocolo del enunciado al socket dado

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
        socket_cliente.send(data)

    def send_command(self, comando, parametros, usuario):
        """
        Envia un comando serializado al usuario de la forma
        ("comando": (parametros))

        los parametros son recibidos como una lista de parametros
        """
        tupla = (comando, parametros)
        tupla_serializado = pickle.dumps(tupla)
        self.send_bytes(tupla_serializado, usuario)

    def log(self, nombre_usuario="-", evento="-", detalles="-"):
        print(f"{nombre_usuario: ^25} | {evento: ^25} | {detalles: ^25}")

    def inicio_log(self):
        usuario = "Usuario"
        evento = "Evento"
        detalles = "Detalles"
        print(f"{usuario:^25} | {evento:^25} | {detalles:^25}")
        char = ""
        print(f"{char:-^25} | {char:-^25} | {char:-^25}")


if __name__ == "__main__":
    server = ServerNet()
    while True:
        print(">>>")
        comando = input("Ingrese un comando para enviar al cliente: ")
        str_parametros = input("Ingrese parametros separados por comas: ")
        parametros = tuple(str_parametros.split(", "))
        for usuario in server.clientes:
            server.send_command(comando, parametros, usuario)
            server.log(usuario, evento="Instruccion", detalles=comando)
