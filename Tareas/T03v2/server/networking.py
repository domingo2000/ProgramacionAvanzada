import socket
import json
import pickle
from threading import Thread, Lock
from collections import deque
from faker import Faker

with open("parametros.json") as file:
    PARAMETROS = json.load(file)


class Comando:

    def __init__(self, nombre_comando, *args):
        self.nombre = nombre_comando
        if len(args) > 0:
            self.parametros = args
        else:
            self.parametros = None

    def __repr__(self):

        return f"({self.nombre}: {self.parametros})"


class ServerNet:

    def __init__(self):
        self.host = PARAMETROS["host"]
        self.port = PARAMETROS["port"]
        self.cantidad_usuarios_permitidos = PARAMETROS["CANTIDAD_JUGADORES_PARTIDA"]
        self.cola_comandos = deque()
        self.faker = Faker()
        self.clientes = {}  # nombre_usuario, socket_cliente
        self.nombres_usuarios = []
        self.lock_log = Lock()
        # Crea el socket del servidor
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta el socket al puerto y host
        self.bind_and_listen()
        # Crea el thread para aceptar clientes
        thread_aceptar_clientes = Thread(target=self.thread_aceptar_clientes, daemon=True)
        thread_aceptar_clientes.start()

    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")

    def thread_aceptar_clientes(self):
        self.log("server", "aceptando clientes")
        while True:
            socket_cliente, ip_cliente = self.socket_server.accept()
            nombre_usuario = self.crear_nombre_usuario()
            if self.lleno():
                self.rechazar_cliente(nombre_usuario, socket_cliente)
            else:
                self.aceptar_cliente(nombre_usuario, socket_cliente)

    def aceptar_cliente(self, nombre_usuario, socket_cliente):
        self.clientes[nombre_usuario] = socket_cliente
        self.send_command(nombre_usuario, "aceptar_cliente")
        # Crea el thread de escucha de comandos para el cliente
        thread_escucha = Thread(target=self.thread_escucha_cliente,
                                args=(socket_cliente, nombre_usuario, ),
                                daemon=True)
        thread_escucha.start()
        self.log("Server", "aceptando_cliente", nombre_usuario)

    def thread_escucha_cliente(self, socket_cliente, nombre_usuario):
        self.log("server", "escuchando_usuario", nombre_usuario)
        while True:
            try:
                data = self.recive_data(socket_cliente)
                comando = pickle.loads(data)
                self.añadir_comando(comando, nombre_usuario)
            except ConnectionError:
                print("NO DEBERIA ESTAR AQUI")
                self.desconectar_usuario(nombre_usuario)
                break

    def rechazar_cliente(self, nombre_usuario, socket_cliente):
        self.clientes[nombre_usuario] = socket_cliente
        self.send_command(nombre_usuario, "rechazar_cliente")
        self.desconectar_usuario(nombre_usuario)
        self.log("Server", "rechazando_cliente", nombre_usuario)

    def crear_nombre_usuario(self):
        nombre_usuario = self.faker.name()
        while nombre_usuario in self.nombres_usuarios:
            nombre_usuario = self.faker.name()
        self.nombres_usuarios.append(nombre_usuario)
        return nombre_usuario

    def send_bytes(self, bytes, nombre_usuario):
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

        socket_cliente = self.clientes[nombre_usuario]

        try:
            socket_cliente.sendall(data)
        except ConnectionError:
            self.desconectar_usuario(usuario)

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

    def desconectar_usuario(self, nombre_usuario):
        del self.clientes[nombre_usuario]
        self.nombres_usuarios.remove[nombre_usuario]
        # Completar comando actualizar usuarios

    def send_command(self, nombre_usuario, nombre_comando, *args):
        """
        Envia un comando serializado con un nombre,
        *args recibe los parametros necesarios para realizar dicho comando
        y se envia un comando de la forma
        tupla: ("comando": (parametros))
        """
        comando = Comando(nombre_comando, *args)
        comando_serializado = pickle.dumps(comando)
        self.send_bytes(comando_serializado, nombre_usuario)

        if comando.nombre != "":
            self.log("Server", f"comando: {comando}", nombre_usuario)

    def añadir_comando(self, comando, nombre_usuario):
        self.cola_comandos.append(comando)
        self.log("server", "añadiendo comando", f"{comando}, {nombre_usuario}")

    def log(self, nombre_usuario="-", evento="-", detalles="-"):
        with self.lock_log:
            print(f"{nombre_usuario: ^25} | {evento: ^25} | {detalles: ^25}")

    def lleno(self):
        if len(self.clientes) >= self.cantidad_usuarios_permitidos:
            return True
        else:
            return False


net_server = ServerNet()


class InterfazServerNet:
    lock_envio_comandos = Lock()
    lock_sacar_comandos = Lock()
    lock_añadir_comandos = Lock()
    network = net_server

    def __init__(self):
        pass

    def send_command(self, nombre_usuario, comando, *args):
        with self.lock_envio_comandos:
            self.network.send_command(nombre_usuario, comando, *args)

    def revisar_comando(self, dict_comandos):
        with self.lock_sacar_comandos:
            if len(self.network.cola_comandos) > 0:
                comando = self.network.cola_comandos[0]
                nombre_comando = comando.nombre
                if nombre_comando in dict_comandos:
                    comando = self.network.cola_comandos.popleft()
                    funcion = dict_comandos[nombre_comando]
                    self.realizar_comando(comando, funcion)

    def añadir_comando(self, comando, nombre_usuario):
        with self.lock_añadir_comandos:
            self.network.añadir_comando(comando, nombre_usuario)

    def realizar_comando(self, comando, funcion):
        if comando.parametros is None:
            funcion()
        else:
            parametros = comando.parametros
            funcion(*parametros)


interfaz_network = InterfazServerNet()


if __name__ == "__main__":
    import time
    comando = Comando("sumar", 1, 2, 3, 4)
    comando_none = Comando("none")
    interfaz_network.añadir_comando(comando, "pepito")
    interfaz_network.añadir_comando(comando_none, "pepito")

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
    net_server.socket_server.close()
