from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QPushButton
from PyQt5 import uic

window_name, base_class = uic.loadUiType("monopolio.ui")


class DialogoMonopolio(window_name, base_class):

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    dialog = DialogoMonopolio()
    dialog.exec()