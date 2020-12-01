import socket
import json
import pickle
from threading import Thread, Lock
from collections import deque
from faker import Faker
from comando import Comando
with open("parametros.json") as file:
    PARAMETROS = json.load(file)


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

    def encender(self):
        # Conecta el socket al puerto y host
        self.bind_and_listen()
        # Crea el thread para aceptar clientes
        thread_aceptar_clientes = Thread(name="thread_aceptar_clientes",
                                         target=self.thread_aceptar_clientes,
                                         daemon=True)
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
        # Envia el comando para darle el nombre de usuario al cliente
        self.send_command(nombre_usuario, "set_user", nombre_usuario)

        # Envia el comando para anadir el usuario en la sala de espera
        self.send_command_to_all("update_users", self.nombres_usuarios)

        self.log("Server", "aceptando_cliente", nombre_usuario)
        # Crea el thread de escucha de comandos para el cliente
        thread_escucha = Thread(name=f"thread_escucha_usuario {nombre_usuario}",
                                target=self.thread_escucha_cliente,
                                args=(socket_cliente, nombre_usuario, ),
                                daemon=True)
        thread_escucha.start()

    def thread_escucha_cliente(self, socket_cliente, nombre_usuario):
        self.log("server", "escuchando_usuario", nombre_usuario)
        while True:
            try:
                data = self.recive_data(socket_cliente)
                comando = pickle.loads(data)
                self.anadir_comando(comando, nombre_usuario)
            except ConnectionError:
                self.desconectar_usuario(nombre_usuario)
                break

    def rechazar_cliente(self, nombre_usuario, socket_cliente):
        self.clientes[nombre_usuario] = socket_cliente
        self.send_command(nombre_usuario, "msg_wait_room",
                          "Servidor LLeno, Cierre el programa y intente mas tarde")
        self.send_command(nombre_usuario, "rechazar_cliente", "lleno")

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
        self.nombres_usuarios.remove(nombre_usuario)
        self.log("server", "desconectando usuario", nombre_usuario)
        # Completar comando actualizar usuarios
        self.send_command_to_all("update_users", self.nombres_usuarios)
        # Completar comando quitar de la cola del juego

    def send_command(self, nombre_usuario, nombre_comando, *args):
        """
        Envia un comando serializado con un nombre al usuario especificado,
        *args recibe los parametros necesarios para realizar dicho comando
        y se envia un comando de la forma
        tupla: ("comando": (parametros))
        """
        comando = Comando(nombre_comando, *args)
        comando_serializado = pickle.dumps(comando)
        self.send_bytes(comando_serializado, nombre_usuario)

        if comando.nombre != "":
            self.log("Server", f"enviando comando: {comando}", nombre_usuario)

    def send_command_to_all(self, nombre_comando, *args):
        """
        Envia un comando serializado con un nombre a todos los clientes conectados,
        *args recibe los parametros necesarios para realizar dicho comando
        y se envia un comando de la forma
        tupla: ("comando": (parametros))
        """
        for nombre_usuario in self.clientes:
            self.send_command(nombre_usuario, nombre_comando, *args)

    def anadir_comando(self, comando, nombre_usuario):
        self.cola_comandos.append(comando)
        self.log("server", "anadiendo comando", f"{comando}, {nombre_usuario}")

    def log(self, nombre_usuario="-", evento="-", detalles="-"):
        with self.lock_log:
            print(f"{nombre_usuario: ^20} | {evento: ^50} | {detalles: ^50}")

    def lleno(self):
        if len(self.clientes) >= self.cantidad_usuarios_permitidos:
            return True
        else:
            return False


net_server = ServerNet()


class InterfazServerNet:
    lock_envio_comandos = Lock()
    lock_sacar_comandos = Lock()
    lock_anadir_comandos = Lock()
    network = net_server

    def __init__(self):
        pass

    def send_command(self, nombre_usuario, nombre_comando, *args):
        with self.lock_envio_comandos:
            self.network.send_command(nombre_usuario, nombre_comando, *args)

    def send_command_to_all(self, nombre_comando, *args):
        with self.lock_envio_comandos:
            self.network.send_command_to_all(nombre_comando, *args)

    def revisar_comando(self, dict_comandos):
        with self.lock_sacar_comandos:
            if len(self.network.cola_comandos) > 0:
                comando = self.network.cola_comandos[0]
                nombre_comando = comando.nombre
                if nombre_comando in dict_comandos:
                    comando = self.network.cola_comandos.popleft()
                    funcion = dict_comandos[nombre_comando]
                    self.realizar_comando(comando, funcion)
                    self.network.log("server", "realizado comando", nombre_comando)

    def anadir_comando(self, comando, nombre_usuario):
        with self.lock_anadir_comandos:
            self.network.anadir_comando(comando, nombre_usuario)

    def realizar_comando(self, comando, funcion):
        if comando.parametros is None:
            funcion()
        else:
            parametros = comando.parametros
            funcion(*parametros)


interfaz_network = InterfazServerNet()


def thread_revisar_comandos(dict_comandos):
    while True:
        interfaz_network.revisar_comando(dict_comandos)


if __name__ == "__main__":
    import time
    comando = Comando("sumar", 1, 2, 3, 4)
    comando_none = Comando("none")
    interfaz_network.anadir_comando(comando, "pepito")
    interfaz_network.anadir_comando(comando_none, "pepito")

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
