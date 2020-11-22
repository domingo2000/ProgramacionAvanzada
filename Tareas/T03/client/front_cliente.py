import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QApplication

window_name, base_class = uic.loadUiType("sala_espera.ui")


class VentanaEspera(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def añadir_usuario(self, nombre_usuario):
        label = QLabel(nombre_usuario)
        self.layout_usuarios.addWidget(label)


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaEspera()
    for _ in range(4):
        usuario = input("Ingrese un usuario")
        ventana.añadir_usuario(usuario)
    sys.exit(app.exec_())
