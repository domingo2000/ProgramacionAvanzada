from PyQt5.QtCore import pyqtSignal, QObject


class BackInicio(QObject):
    senal_usuario_incorrecto = pyqtSignal()
    senal_cerrar_inicio = pyqtSignal()
    senal_abrir_juego = pyqtSignal()
    senal_enviar_nombre_usario = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def verificar_usuario(self, nombre_usuario):
        if nombre_usuario.isalnum():
            self.senal_cerrar_inicio.emit()
            self.senal_abrir_juego.emit()
            self.senal_enviar_nombre_usario.emit(nombre_usuario)
        else:
            self.senal_usuario_incorrecto.emit()
