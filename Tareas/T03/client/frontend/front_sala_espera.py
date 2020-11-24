import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QApplication

window_name, base_class = uic.loadUiType("sala_espera.ui")


class VentanaEspera(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.labels_usuarios = []
        self.comandos = {
            "close_window_wait": self.hide,
            "añadir_usuario": self.añadir_usuario,
            "actualizar_usuarios": self.actualizar_usuarios
        }

    def añadir_usuario(self, nombre_usuario):
        label = QLabel(nombre_usuario)
        self.labels_usuarios.append(label)
        self.layout_usuarios.addWidget(label)

    def actualizar_usuarios(self, nombres_usuarios):
        for label_usuario in self.labels_usuarios:
            label_usuario.hide()
            label_usuario.setParent(None)
        for nombre_usuario in nombres_usuarios:
            self.añadir_usuario(nombre_usuario)

    def realizar_comando(self, tupla_comando):
        comando = tupla_comando[0]
        parametros = tupla_comando[1]
        if comando in self.comandos:
            metodo = self.comandos[comando]
            if parametros[0] is not None:
                metodo(*parametros)
            else:
                metodo()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaEspera()
    for _ in range(4):
        usuario = input("Ingrese un usuario")
        ventana.añadir_usuario(usuario)
    sys.exit(app.exec_())
