from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5 import uic

window_name, base_class = uic.loadUiType("ventana_juego.ui")


class VentanaJuego(window_name, base_class):

    def __init__(self):
        super().__init__()

    def añadir_label(label, pos):
        label = QLabel()