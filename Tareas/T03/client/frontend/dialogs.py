from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QPushButton
from PyQt5 import uic
import sys

window_name, base_class = uic.loadUiType("monopolio.ui")


class DialogoMonopolio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


window_name, base_class = uic.loadUiType("punto_victoria.ui")


class DialogPuntoVictoria(window_name, base_class):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication([])
    ventana = QWidget()
    ventana.setGeometry(50, 50, 500, 500)
    ventana.show()
    dialog = DialogPuntoVictoria(ventana)
    dialog.exec()
    sys.exit(app.exec_())