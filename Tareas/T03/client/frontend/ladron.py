from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import QMimeData, QPoint, Qt
import json
from os import path

with open("parametros.json") as file:
    data = json.load(file)
    rutas = data["rutas_sprites"]


class Ladron(QLabel):

    def __init__(self, pos_x, pos_y, parent):
        super().__init__(parent)
        self.setGeometry(pos_x, pos_y, 50, 50)
        self.pixmap = QPixmap(path.join(*rutas["ladron"]))
        self.setPixmap(self.pixmap)
        self.setScaledContents(True)
        self.setMaximumSize(31, 31)
        self.setStyleSheet("background-color: transparent;")
        self.tipo = "ladron"
        self.movible = False

    def mouseMoveEvent(self, event):
        if not self.movible:
            return
        # Drag and Drop
        drag = QDrag(self)
        mimedata = QMimeData()
        drag.setMimeData(mimedata)
        drag.setPixmap(self.grab())
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QWidget, QApplication
    import sys
    app = QApplication([])
    ventana = QWidget()
    ventana.setGeometry(50, 50, 500, 500)
    ladron = Ladron(50, 50, ventana)
    ladron.show()
    ventana.show()
    sys.exit(app.exec_())
