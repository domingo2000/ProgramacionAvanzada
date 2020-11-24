import socket
from threading import Thread
import sys
import json
import pickle
from PyQt5.QtCore import pyqtSignal, QObject


class ClientNet(QObject):
    senal_comando = pyqtSignal(tuple)

    def __init__(self):
        print("Inicializando Cliente")
        super().__init__()
        with open("parametros.json", "r") as file:
            data = json.loads(file.read())
        self.host = data["host"]
        self.port = data["port"]
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            conexion_exitosa = self.connect_to_server()
            if conexion_exitosa:
                self.listen()
        except ConnectionError:
            print("No debería estar aquí")
            print("Conexión terminada.")
            self.socket_client.close()
            sys.exit()

    def connect_to_server(self):
        """
        Crea la conexion al servidor retorna un booleano
        True: En caso de ser exitosa
        False: En caso de estar lleno el servidor o no estar disponible el
        servidor
        """
        try:
            print("Tratando de conectar al servidor")
            self.socket_client.connect((self.host, self.port))

            # Revisa si se logro conectar
            respuesta = self.recive_message()
            print(respuesta)
            if respuesta == "aceptado":
                print("Cliente conectado exitosamente al servidor.")
                return True
            elif respuesta == "rechazado":
                print("Servidor Lleno")
                self.socket_client.close()
                print("cerrando Socket")
                return False

        except ConnectionError:
            print("No se ha podido conectar al servidor")
            self.socket_client.close()
            return False

    def listen(self):
        """ Inicializa el thread que escucha datos desde el servidor """
        thread = Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        """
        Crea un thread que espera los datos del servidor en forma de
        comandos
        """
        while True:
            try:
                self.recive_command()
            except ConnectionError:
                print("Servidor Desconectado")
                self.socket_client.close()
                print("Socket cerrado")

    def recive_data(self):
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
            return data

    def recive_command(self):
        data = self.recive_data()
        comando = pickle.loads(data)
        self.realizar_comando(comando)

    def recive_message(self):
        data = self.recive_data()
        return data.decode("utf-8")

    def realizar_comando(self, comando):
        self.senal_comando.emit(comando)

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
    import time
    cliente = ClientNet()
    while True:
        time.sleep(4)
        print("main thread")
        pass
