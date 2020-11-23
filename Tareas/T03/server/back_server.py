from PyQt5.QtCore import pyqtSignal, QObject


class BackServer(QObject):
    senal_enviar_comando = pyqtSignal(str, tuple, str)
    senal_enviar_log = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        pass

    def enviar_comando(self, comando, parametros, usuario):
        self.senal_comando.emit(comando, parametros, usuario)

    def enviar_log(self, nombre_usuario="-", evento="-", detalles="-"):
        self.senal_log.emit(nombre_usuario, evento, detalles)
