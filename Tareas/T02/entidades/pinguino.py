from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtCore import QRect, QMimeData, Qt, QPoint, QSize
from PyQt5.QtGui import QPixmap, QPainter, QDrag, QBitmap
import sys


class Pinguino(QLabel):

    def __init__(self, parent, ruta_imagen=None, qpoint=None):
        super().__init__(parent=parent)
        pixmap = QPixmap(ruta_imagen)
        self.setStyleSheet("background-color: transparent;")
        self.setGeometry(qpoint.x(), qpoint.y(), pixmap.width(), pixmap.height())
        self.setPixmap(pixmap)

        # atributos
        self.colider = QRect(self.pos(), self.size())
        self.ruta_imagen = ruta_imagen
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        # Drag and Drop
        drag = QDrag(self)
        mimedata = QMimeData()  # Debe tener todos los datos para crear un pinguino
        # Crea los datos necesarios para hacer un pinguino
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


if __name__ == '__main__':
    class Ventana(QWidget):
        def __init__(self):
            super().__init__()
            self.setGeometry(50, 50, 500, 500)
            self.setStyleSheet("background-color: black")
            self.show()

    app = QApplication(sys.argv)
    ventana = Ventana()
    pinguino = Pinguino(ventana, datos="sprites\\pinguirin_amarillo\\amarillo_neutro.png, 50, 50")
    ventana.show()
    sys.exit(app.exec_())
