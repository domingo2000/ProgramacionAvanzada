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
    senal_actualizar_construcciones = pyqtSignal(dict)
    senal_actualizar_dados = pyqtSignal(QPixmap, QPixmap)
    senal_actualizar_puntos = pyqtSignal(dict)
    senal_actualizar_jugador_actual = pyqtSignal(str)
    senal_servidor_lleno = pyqtSignal(str)
    senal_cerrar_sala_espera = pyqtSignal()
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_abrir_sala_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()
    senal_cambiar_label_usuario = pyqtSignal(str, str)
    senal_realizar_monopolio = pyqtSignal()
    senal_mensaje_error = pyqtSignal(str)
    senal_actualizar_punto_victoria = pyqtSignal(int)

    senal_activar_boton_dados = pyqtSignal(bool)
    senal_activar_interfaz = pyqtSignal(bool)

    def __init__(self, host, port):
        super().__init__()
        self.net = ClientNet(host, port)
        self.usuario_propio = None
        self.accion_realizada = False
        self.dados_lanzados = False
        self.comandos = {
            "cargar_mapa": self.cargar_mapa,
            "cargar_usuarios": self.cargar_labels_usuarios,
            "test": self.test,
            "set_user": self.fijar_usuario,
            "actualizar_usuarios": self.actualizar_usuarios,
            "actualizar_materias_primas": self.actualizar_materias_primas,
            "actualizar_construcciones": self.actualizar_construcciones,
            "actualizar_puntos": self.actualizar_puntos,
            "actualizar_dados": self.actualizar_dados,
            "actualizar_jugador_actual": self.senal_actualizar_jugador_actual.emit,
            "servidor_lleno": self.alerta_servidor_lleno,
            "close_wait_room": self.senal_cerrar_sala_espera.emit,
            "close_game_room": self.senal_cerrar_ventana_juego.emit,
            "open_wait_room": self.senal_abrir_sala_espera.emit,
            "open_game_room": self.senal_abrir_ventana_juego.emit,
            "throw_dices": self.notificar_tirar_dados,
            "activar_interfaz": self.senal_activar_interfaz.emit,
            "realizar_monopolio": self.senal_realizar_monopolio.emit,
            "error_msg": self.senal_mensaje_error.emit,
            "actualizar_punto_victoria": self.senal_actualizar_punto_victoria.emit
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

    def fijar_usuario(self, usuario):
        self.usuario_propio = usuario

    def actualizar_materias_primas(self, dict_usuarios_materias):
        """
        Recibe un diccionario de la forma:
        {"usuario": {"madera": 0, "arcilla": 0, "trigo": 0},...}
        y actualiza los labels de los puntos
        """
        dict_id_materias = self.transformar_dict_usuario_id(dict_usuarios_materias)
        self.senal_actualizar_materias_primas.emit(dict_id_materias)

    def actualizar_construcciones(self, dict_nodo_construccion):
        """
        Recibe un diccionario de la forma
        {"id_nodo": [construccion, usuario], "id_nodo_2": [construccion, usuario]}
        y asigna los pixmaps a cada nodo.
        En caso de ser None el pixmap, esconde el label
        """

        for id_nodo in dict_nodo_construccion.copy():
            datos_nodo = dict_nodo_construccion[id_nodo]
            construccion = datos_nodo[0]
            if construccion:
                usuario = datos_nodo[1]
                id_usuario = self.usuarios_id[usuario]
                ruta = path.join(*data["rutas_sprites"][f"{construccion}_j{id_usuario}"])
                pixmap = QPixmap(ruta)
                dict_nodo_construccion[id_nodo] = pixmap
            else:
                dict_nodo_construccion[id_nodo] = None

        self.senal_actualizar_construcciones.emit(dict_nodo_construccion)

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

    def actualizar_puntos(self, dict_usuario_puntos):
        """
        Recibe un diccionario de la forma
        {"usuario": puntos, "usuario2": puntos2} y envia la señal para
        actualizar los puntos en la interfaz
        """
        dict_id_puntos = self.transformar_dict_usuario_id(dict_usuario_puntos)
        self.senal_actualizar_puntos.emit(dict_id_puntos)

    def actualizar_dados(self, num_dado_1, num_dado_2):
        ruta_pixmap_1 = path.join(*data["rutas_sprites"][f"dado_{num_dado_1}"])
        ruta_pixmap_2 = path.join(*data["rutas_sprites"][f"dado_{num_dado_2}"])
        pixmap_1 = QPixmap(ruta_pixmap_1)
        pixmap_2 = QPixmap(ruta_pixmap_2)
        self.senal_actualizar_dados.emit(pixmap_1, pixmap_2)

    def cargar_mapa(self, numeros, materias_primas):
        self.net.log("Cargando Mapa")
        for id_hexagono in range(len(numeros)):
            num_ficha = numeros[id_hexagono]
            materia_prima = materias_primas[id_hexagono]
            id_hexagono = str(id_hexagono)
            self.senal_actualizar_num_ficha.emit(id_hexagono, num_ficha)
            self.senal_actualizar_materia_prima_hexagono.emit(id_hexagono, materia_prima)

    def cargar_labels_usuarios(self):
        for usuario in self.usuarios_id:
            id = self.usuarios_id[usuario]
            self.senal_cambiar_label_usuario.emit(id, usuario)

    def lanzar_dados(self):
        self.net.send_command("lanzar_dados")
        self.dados_lanzados = True

    def notificar_tirar_dados(self):
        self.senal_activar_boton_dados.emit(True)

    def pasar_turno(self):
        self.enviar_accion_realizada("pasar")

    def alerta_servidor_lleno(self):
        mensaje = "El Servidor se encuentra lleno, espere a que haya terminado la partida"
        self.senal_servidor_lleno.emit(mensaje)

    def transformar_dict_usuario_id(self, dict_usuario_contenido):
        """
        Recibe un dict de la forma
        {"usuario": contenido, "usuario": contenido} y lo transforma en
        {"id_usuario": contenido, "usuario": contenido}
        """
        dict_id_contenido = {}
        for usuario in dict_usuario_contenido:
            id_usuario = self.usuarios_id[usuario]
            contenido = dict_usuario_contenido[usuario]
            dict_id_contenido[id_usuario] = contenido

        return dict_id_contenido

    def test(self):
        self.net.log("Test", "None")

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

    def enviar_accion_realizada(self, str_accion, id=None):
        self.net.send_command("realizar_accion", [str_accion, id])

    def comprar_carta_desarrollo(self):
        self.enviar_accion_realizada("carta_desarrollo")

    def enviar_info_monopolio(self, materia_prima):
        self.net.send_command("actualizar_materia_monopolio", [materia_prima])

    def manejar_casa_dropeada(self, id_nodo):
        self.enviar_accion_realizada("choza", id_nodo)


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
