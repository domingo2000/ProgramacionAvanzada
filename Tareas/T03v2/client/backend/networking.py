import socket
import json
import pickle
from threading import Thread, Lock, Event
from collections import deque
from comando import Comando
import time


with open("parametros.json") as file:
    PARAMETROS = json.load(file)


class ClientNet:

    def __init__(self):
        self.host = PARAMETROS["host"]
        self.port = PARAMETROS["port"]
        self.cola_comandos = deque()
        self.lock_log = Lock()
        self.comandos = {
            "aceptar_cliente": self.notificar_conexion_exitosa,
            "rechazar_cliente": self.desconectarse
        }
        # Crea el socket del servidor
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def encender(self):
        self.log("Inicializando")
        self.connect()

    def connect(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            #  Comienza a escuchar al servidor
            thread_escucha = Thread(target=self.thread_escucha_servidor,
                                    daemon=True)
            thread_escucha.start()
            # Comienza a revisar los comandos de su misma cola
            thread_revisar_comandos = Thread(target=self.thread_revisar_comandos,
                                             daemon=True)
            thread_revisar_comandos.start()
        except ConnectionError:
            self.desconectarse(msg="Servidor no disponible")

    def thread_escucha_servidor(self):
        self.log("escuchando Servidor", f"{self.host};{self.port}")
        while True:
            try:
                data = self.recive_data()
                comando = pickle.loads(data)
                self.anadir_comando(comando)
            except ConnectionError:
                self.desconectarse(msg="El servidor se ha cerrado abruptamente")
                break
            except OSError:
                print("El Socket ya habia sido desconectado")
                break
                pass

    def desconectarse(self, msg=None):
        self.socket_cliente.close()
        if msg is not None:
            self.log("rechazado por el server", msg)
        else:
            self.log("desconectandose")

    def notificar_conexion_exitosa(self):
        self.log("Cliente aceptado por el servidor")

    def send_bytes(self, bytes):
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

        try:
            self.socket_cliente.sendall(data)
        except ConnectionError:
            self.desconectarse(msg="Servidor cerrado abruptamente")
        except OSError:
            print("El socket ya habia sido desconectado")

    def recive_data(self):
        try:
            """
            Recibe datos con el protocolo del enunciado, en caso de ser
            un byte vacio pasa, si otra cosa ejecuta el comando.
            """
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
        except ConnectionError:
            pass

    def send_command(self, nombre_comando, *args):
        """
        Envia un comando serializado con un nombre,
        *args recibe los parametros necesarios para realizar dicho comando
        y se envia un comando de la forma
        tupla: ("comando": (parametros))
        """
        comando = Comando(nombre_comando, *args)
        comando_serializado = pickle.dumps(comando)
        self.send_bytes(comando_serializado)

        if comando.nombre != "":
            self.log(f"enviando comando: {comando}")

    def anadir_comando(self, comando):
        self.cola_comandos.append(comando)
        self.log("anadiendo comando", f"{comando}")

    def log(self, evento="-", detalles="-"):
        with self.lock_log:
            print(f"{evento: ^25} | {detalles: ^25}")

    def thread_revisar_comandos(self):
        while True:
            interfaz_network.revisar_comando(self.comandos)
            time.sleep(0)


net_cliente = ClientNet()


class InterfazClientNet:
    lock_envio_comandos = Lock()
    lock_sacar_comandos = Lock()
    lock_anadir_comandos = Lock()
    network = net_cliente

    def __init__(self):
        pass

    def send_command(self, nombre_comando, *args):
        with self.lock_envio_comandos:
            self.network.send_command(nombre_comando, *args)

    def revisar_comando(self, dict_comandos):
        with self.lock_sacar_comandos:
            if len(self.network.cola_comandos) > 0:
                comando = self.network.cola_comandos[0]
                nombre_comando = comando.nombre
                if nombre_comando in dict_comandos:
                    comando = self.network.cola_comandos.popleft()
                    funcion = dict_comandos[nombre_comando]
                    self.realizar_comando(comando, funcion)
                    self.network.log("realizado comando", nombre_comando)

    def anadir_comando(self, comando):
        with self.lock_anadir_comandos:
            self.network.anadir_comando(comando)

    def realizar_comando(self, comando, funcion):
        if comando.parametros is None:
            funcion()
        else:
            parametros = comando.parametros
            funcion(*parametros)


interfaz_network = InterfazClientNet()


def thread_revisar_comandos(dict_comandos):
    while True:
        interfaz_network.revisar_comando(dict_comandos)


def revisar_comando(dict_comandos):
    interfaz_network.revisar_comando(dict_comandos)


if __name__ == "__main__":
    import time
    comando = Comando("sumar", 1, 2, 3, 4)
    comando_none = Comando("none")
    interfaz_network.anadir_comando(comando)
    interfaz_network.anadir_comando(comando_none)

    class A:

        def __init__(self):
            self.comandos = {
                "sumar": self.sumar,
                "none": self.none
            }
            self.thread_revisar_comandos()

        def none(self):
            print("nonees")

        def sumar(self, *args):
            suma = 0
            for i in args:
                suma += 1
            print(suma)

        def thread_revisar_comandos(self):
            a = 0
            while True:
                print("Revisando comandos")
                interfaz_network.revisar_comando(self.comandos)
                if a == 5:
                    break
                a += 1
    a = A()
    time.sleep(1)
    net_cliente.socket_cliente.close()
