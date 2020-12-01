from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import QMimeData, QPoint, Qt
import json
from os import path

with open("parametros.json") as file:
    data = json.load(file)
    rutas = data["rutas_sprites"]


class Casa(QLabel):

    def __init__(self, pos_x, pos_y, parent):
        super().__init__(parent)
        self.setGeometry(pos_x, pos_y, 50, 50)
        self.pixmap = QPixmap(path.join(*rutas["choza_j0"]))
        self.setPixmap(self.pixmap)
        self.setScaledContents(True)
        self.setMaximumSize(50, 50)
        self.setStyleSheet("background-color: transparent;")
        self.tipo = "choza"
        self.movible = False

    def mouseMoveEvent(self, event):
        if not self.movible:
            return
        # Drag and Drop
        drag = QDrag(self)
        mimedata = QMimeData()
        drag.setMimeData(mimedata)
        drag.setPixmap(self.grab())
        drag.setHotSpot(QPoint(0, 0))
        drag.exec_(Qt.CopyAction | Qt.MoveAction)