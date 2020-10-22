import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class Nivel(QWidget):

    def __init__(self):
        self.combo = 0
        self.combo_maximo = 0


class NivelPrincipiante(Nivel):
    pass


class NivelAficionado(Nivel):
    pass


class NivelMaestroCumbia(Nivel):
    pass
