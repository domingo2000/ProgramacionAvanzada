from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from backend.networking import ClientNet
from os import path
import json

with open("parametros.json") as file:
    data = json.load(file)


class BackVentanaJuego(QObject):
    senal_actualizar_num_ficha = pyqtSignal(str, int)
    senal_actualizar_materias_primas = pyqtSignal(dict)
    senal_actualizar_materia_prima_hexagono = pyqtSignal(str, str)
    senal_actualizar_usuarios = pyqtSignal(list)
    senal_servidor_lleno = pyqtSignal(str)
    senal_cerrar_sala_espera = pyqtSignal()
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_abrir_sala_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()
    senal_cambiar_label_usuario = pyqtSignal(str, str)
    senal_actualizar_dados = pyqtSignal(QPixmap, QPixmap)
    senal_activar_interfaz = pyqtSignal(bool)

    def __init__(self, host, port):
        super().__init__()
        self.net = ClientNet(host, port)
        self.usuario_propio = None
        self.comandos = {
            "cargar_mapa": self.cargar_mapa,
            "cargar_usuarios": self.cargar_labels_usuarios,
            "test": self.test,
            "set_user": self.fijar_usuario,
            "actualizar_usuarios": self.actualizar_usuarios,
            "actualizar_materias_primas": self.actualizar_materias_primas,
            "actualizar_dados": self.actualizar_dados,
            "servidor_lleno": self.alerta_servidor_lleno,
            "close_wait_room": self.senal_cerrar_sala_espera.emit,
            "close_game_room": self.senal_cerrar_ventana_juego.emit,
            "open_wait_room": self.senal_abrir_sala_espera.emit,
            "open_game_room": self.senal_abrir_ventana_juego.emit
        }
        self.usuarios_id = {
            "nombre_0": "0",
            "nombre_1": "1",
            "nombre_2": "2",
            "nombre_3": "3",
        }
        # Timer Que revisa los comandos Todo el tiempo
        self.timer_revisar_comando = QTimer()
        self.timer_revisar_comando.setInterval(0)
        self.timer_revisar_comando.timeout.connect(self.thread_revisar_comandos)
        self.timer_revisar_comando.start()

    def thread_revisar_comandos(self):
        if not self.net.comando_realizado:
            index_ultimo_comando = len(self.net.stack_comandos) - 1
            comando = self.net.stack_comandos[index_ultimo_comando]
            nombre_comando = comando[0]
            if nombre_comando in self.comandos:
                comando = self.net.stack_comandos.pop(index_ultimo_comando)
                self.realizar_comando(comando)
        else:
            pass

    def cargar_mapa(self, numeros, materias_primas):
        self.net.log("Cargando Mapa")
        for id_hexagono in range(len(numeros)):
            num_ficha = numeros[id_hexagono]
            materia_prima = materias_primas[id_hexagono]
            id_hexagono = str(id_hexagono)
            self.senal_actualizar_num_ficha.emit(id_hexagono, num_ficha)
            self.senal_actualizar_materia_prima_hexagono.emit(id_hexagono, materia_prima)

    def realizar_comando(self, tupla_comando):
        comando = tupla_comando[0]
        if comando != "":
            parametros = tupla_comando[1]
            if comando in self.comandos:
                metodo = self.comandos[comando]
                if parametros:
                    metodo(*parametros)
                else:
                    metodo()
                self.net.comando_realizado = True
                self.net.log("Comando Realizado", comando)

    def fijar_usuario(self, usuario):
        self.usuario_propio = usuario

    def actualizar_usuarios(self, usuarios):
        self.senal_actualizar_usuarios.emit(usuarios)
        self.net.log("Actualizando Usuarios")
        id = 1
        for usuario in usuarios:
            if usuario == self.usuario_propio:
                self.usuarios_id[usuario] = "0"
            else:
                self.usuarios_id[usuario] = str(id)
                id += 1

    def test(self):
        self.net.log("Test", "None")

    def alerta_servidor_lleno(self):
        mensaje = "El Servidor se encuentra lleno, espere a que haya terminado la partida"
        self.senal_servidor_lleno.emit(mensaje)

    def actualizar_materias_primas(self, dict_usuarios_materias):
        """
        Recibe un diccionario de la forma:
        {"usuario": {"madera": 0, "arcilla": 0, "trigo": 0},...}
        y actualiza los labels de los puntos
        """
        dict_id_materias = self.transformar_dict_usuario_id(dict_usuarios_materias)
        self.senal_actualizar_materias_primas.emit(dict_id_materias)

    def transformar_dict_usuario_id(self, dict_usuario_contenido):
        dict_id_contenido = {}
        for usuario in dict_usuario_contenido:
            id_usuario = self.usuarios_id[usuario]
            contenido = dict_usuario_contenido[usuario]
            dict_id_contenido[id_usuario] = contenido

        return dict_id_contenido

    def cargar_labels_usuarios(self):
        for usuario in self.usuarios_id:
            id = self.usuarios_id[usuario]
            self.senal_cambiar_label_usuario.emit(id, usuario)

    def actualizar_dados(self, num_dado_1, num_dado_2):
        ruta_pixmap_1 = path.join(*data["rutas_sprites"][f"dado_{num_dado_1}"])
        ruta_pixmap_2 = path.join(*data["rutas_sprites"][f"dado_{num_dado_2}"])
        pixmap_1 = QPixmap(ruta_pixmap_1)
        pixmap_2 = QPixmap(ruta_pixmap_2)
        self.senal_actualizar_dados.emit(pixmap_1, pixmap_2)

    def activar_interfaz(self, bool):
        self.senal_activar_interfaz.emit(bool)

    def actualizar_construcciones(self, dict_nodo_construccion):
        """
        Recibe un diccionario de la forma
        {"id_nodo": pixmap, "id_nodo_2": pixmap_2}
        y asigna los pixmaps a cada nodo.
        En caso de ser None el pixmap, esconde el label
        """
    def lanzar_dados(self):
        self.net.send_command("lanzar_dados")

if __name__ == "__main__":
    import json
    with open("parametros.json") as file:
        data = json.load(file)
    back_cliente = BackVentanaJuego(data["host"], data["port"])
    while True:
        comando = input("Ingrese el nombre del comando: ")
        parametros = []
        entrada = input("Ingrese un string para parametro: ")
        parametros.append(entrada)
        back_cliente.net.send_command(comando)
