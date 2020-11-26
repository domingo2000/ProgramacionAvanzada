from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from backend.networking import ClientNet


class BackVentanaJuego(QObject):
    senal_actualizar_num_ficha = pyqtSignal(str, int)
    senal_actualizar_materia_prima_hexagono = pyqtSignal(str, str)
    senal_actualizar_usuarios = pyqtSignal(list)
    senal_servidor_lleno = pyqtSignal(str)
    senal_cerrar_sala_espera = pyqtSignal()
    senal_cerrar_ventana_juego = pyqtSignal()
    senal_abrir_sala_espera = pyqtSignal()
    senal_abrir_ventana_juego = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.net = ClientNet(host, port)
        self.comandos = {
            "cargar_mapa": self.cargar_mapa,
            "test": self.test,
            "actualizar_usuarios": self.actualizar_usuarios,
            "servidor_lleno": self.alerta_servidor_lleno,
            "close_wait_room": self.senal_cerrar_sala_espera.emit,
            "close_game_room": self.senal_cerrar_ventana_juego.emit,
            "open_wait_room": self.senal_abrir_sala_espera.emit,
            "open_game_room": self.senal_abrir_ventana_juego.emit
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

    def actualizar_usuarios(self, usuarios):
        self.senal_actualizar_usuarios.emit(usuarios)
        self.net.log("Actualizando Usuarios")

    def test(self):
        self.net.log("Test", "None")

    def alerta_servidor_lleno(self):
        mensaje = "El Servidor se encuentra lleno, espere a que haya terminado la partida"
        self.senal_servidor_lleno.emit(mensaje)


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
