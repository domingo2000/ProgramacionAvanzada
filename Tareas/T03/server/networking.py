import socket
from threading import Thread
import json
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
            print("Se Ha conectado un nuevo cliente")
            print(self.clientes)
            self.crear_usuario(socket_cliente)

    def crear_usuario(self, socket_cliente):
        fake = Faker()
        usuario = fake.name()
        self.clientes[usuario] = socket_cliente
        thread_escucha = Thread(target=self.escuchar_cliente,
                                args=(usuario, ),
                                daemon=True)
        thread_escucha.start()

    def escuchar_cliente(self, usuario):
        print("Inicializando thread de escucha cliente")
        while True:
            try:
                print("debug")
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
                print(f"Se ha recibido datos:\n{data}")
            except ConnectionError:
                desconectado = self.revisar_desconexion(usuario)
                if desconectado:
                    break

    def revisar_desconexion(self, usuario):
        socket_cliente = self.clientes[usuario]
        bytes = "".encode("utf-8")
        desconectado = False
        try:
            self.send_bytes(bytes, socket_cliente)
        except ConnectionError:
            desconectado = True
            print(f"Se ha desconectado el usuario: {usuario}")
            # Quita al usuario de los clientes conectados
            self.clientes.pop(usuario)
        return desconectado

    def send_bytes(self, bytes, socket_cliente):
        """
        Envía mensajes al cliente.

        Implementa el protocolo del enunciado
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

        socket_cliente.send(data)


if __name__ == "__main__":
    server = ServerNet()
    print("hola")
