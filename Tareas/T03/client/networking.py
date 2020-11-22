import socket
from threading import Thread
import sys
import json


class ClientNet():
    def __init__(self):
        with open("parametros.json", "r") as file:
            data = json.loads(file.read())
        self.host = data["host"]
        self.port = data["port"]
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connect_to_server()
            self.listen()
        except ConnectionError:
            print("Conexión terminada.")
            self.socket_client.close()
            sys.exit()

    def listen(self):
        """ Inicializa el thread que escucha datos desde el servidor """
        thread = Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        "Crea un thread que espera los datos del servidor"
        while True:
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

            data = data.decode("utf-8")
            if data == "":
                pass
            else:
                print(data)

    def connect_to_server(self):
        """Crea la conexión al servidor."""

        self.socket_client.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor.")

    def send_bytes(self, bytes):
        """
        Envía mensajes al servidor.

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

        self.socket_client.sendall(data)


if __name__ == "__main__":
    cliente = ClientNet()
    mensaje = "Hola como estás"
    cliente.send_bytes(mensaje.encode("utf-8"))
    while True:
        pass
