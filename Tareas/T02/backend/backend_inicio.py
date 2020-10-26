from PyQt5.QtCore import pyqtSignal, QObject


class BackInicio(QObject):
    senal_abrir_ventana_juego = pyqtSignal(str)
    senal_usuario_incorrecto = pyqtSignal()
    senal_cerrar_ventana_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        pass

    def chequear_usuario(self, nombre_usuario):
        if nombre_usuario.isalnum():
            self.senal_abrir_ventana_juego.emit(nombre_usuario)
            self.senal_cerrar_ventana_inicio.emit()
        else:
            self.senal_usuario_incorrecto.emit()
            print("Usuario Incorrecto")
