import socket
from threading import Thread
import json
import pickle


class ClientNet():

    def __init__(self, host, port):
        print("Inicializando Cliente")
        super().__init__()
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stack_comandos = []
        self.comando_realizado = True
        try:
            conexion_exitosa = self.connect_to_server()
            if conexion_exitosa:
                self.listen()
            else:
                self.socket_cliente.close()
                self.log("cerrando socket")
        except ConnectionError:
            print("No debería estar aquí")
            self.socket_cliente.close()
            self.log("Socket Cerrado", "inicializando Cliente")

    def connect_to_server(self):
        """
        Crea la conexion al servidor retorna un booleano
        True: En caso de ser exitosa
        False: En caso de estar lleno el servidor o no estar disponible el
        servidor
        """
        try:
            print("Tratando de conectar al servidor")
            self.socket_cliente.connect((self.host, self.port))

            # Revisa si se logro conectar
            respuesta = self.recive_message()
            print(respuesta)
            if respuesta == "aceptado":
                print("Cliente conectado exitosamente al servidor.")
                return True
            elif respuesta == "rechazado":
                print("Servidor Lleno")
                return True

        except ConnectionError:
            print("No se ha podido conectar al servidor")
            self.socket_cliente.close()
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
                data = self.recive_data()
                comando = pickle.loads(data)
                self.añadir_comando(comando)
            except ConnectionError:
                self.log("Servidor Desconectado", "listen_thread")
                self.socket_cliente.close()
                self.log("Socket Cerrado", "listen_thread")
                break

    def recive_data(self):
        # Protocolo de informacion
        data = bytearray()
        bytes_largo = self.socket_cliente.recv(4)
        largo_bytes = int.from_bytes(bytes_largo, byteorder="big")
        numero_chunks = (largo_bytes // 60) + 1
        for i in range(numero_chunks):
            numero_bloque = self.socket_cliente.recv(4)
            data_bloque = self.socket_cliente.recv(60)
            if i == (numero_chunks - 1):
                data_bloque = data_bloque[0: (largo_bytes % 60)]
            data.extend(data_bloque)

        if data == "":
            pass
        else:
            return data

    def añadir_comando(self, comando):
        if comando[0] != "":
            self.stack_comandos.append(comando)
            self.comando_realizado = False
            self.log("comando recibido", comando[0])

    def recive_message(self):
        data = self.recive_data()
        return data.decode("utf-8")

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

        self.socket_cliente.sendall(data)

    def send_command(self, comando, parametros=None):
        """
        Envia un comando serializado al usuario de la forma
        tupla: ("comando": (parametros))

        los parametros son recibidos como una lista de parametros
        """
        tupla = (comando, parametros)
        tupla_serializado = pickle.dumps(tupla)
        self.send_bytes(tupla_serializado)

        if comando != "":
            self.log("enviando comando", comando)

    def log(self, evento="-", detalles="-"):
            print(f"{evento: ^25} | {detalles: ^25}")


if __name__ == "__main__":
    import time
    cliente = ClientNet()
    while True:
        comando = input("Ingrese el nombre del comando: ")
        parametros = []
        entrada = input("Ingrese un string para parametro: ")
        parametros.append(entrada)
        cliente.send_command(comando, parametros)
