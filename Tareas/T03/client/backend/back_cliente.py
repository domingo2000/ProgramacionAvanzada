from PyQt5.QtCore import pyqtSignal, QObject


class BackVentanaJuego(QObject):
    senal_actualizar_num_ficha = pyqtSignal(str, int)
    senal_actualizar_materia_prima_hexagono = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.comandos = {
            "cargar_mapa": self.cargar_mapa
        }

    def cargar_mapa(self, mapa):
        print("Cargando Mapa")
        print(mapa)
        for id_hexagono in mapa.hexagonos:
            hexagono = mapa.hexagonos[id_hexagono]
            num_ficha = hexagono.num_ficha
            materia_prima = hexagono.materia_prima
            self.senal_actualizar_num_ficha.emit(id_hexagono, num_ficha)
            self.senal_actualizar_materia_prima_hexagono.emit(id_hexagono, materia_prima)

    def realizar_comando(self, tupla_comando):
        comando = tupla_comando[0]
        if comando != "":
            print(f"Realizando comando: {comando}")
            parametros = tupla_comando[1]
            if comando in self.comandos:
                metodo = self.comandos[comando]
                print(parametros)
                metodo(*parametros)
                print(f"Comando Realizado: {comando}")
