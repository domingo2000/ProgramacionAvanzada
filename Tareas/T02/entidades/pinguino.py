from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtCore import QRect, QMimeData, Qt, QPoint, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QDrag, QBitmap
import sys


class Pinguino(QLabel):
    senal_pinguino_clickeado = pyqtSignal()

    def __init__(self, parent, ruta_imagen=None, qpoint=QPoint(0, 0), iscopy=False):
        super().__init__(parent=parent)
        pixmap = QPixmap(ruta_imagen)
        # Atributos pinguino
        self.pinguino_comprable = False

        self.pixmap = pixmap
        self.setStyleSheet("background-color: transparent;")
        self.setGeometry(qpoint.x(), qpoint.y(), 100, 100)
        self.setScaledContents(True)
        self.setPixmap(pixmap)
        self.iscopy = iscopy

        # atributos
        self.colider = QRect(self.pos(), self.size())
        self.ruta_imagen = ruta_imagen
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.senal_pinguino_clickeado.emit()

    def mouseMoveEvent(self, event):
        if self.iscopy:
            return
        if not(self.pinguino_comprable):
            return
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        # Drag and Drop
        drag = QDrag(self)
        mimedata = QMimeData()
        drag.setMimeData(mimedata)
        drag.setPixmap(self.grab())
        painter = QPainter()
        drag.setHotSpot(QPoint(0, 0))
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def set_pinguino_comprable(self, bool):
        self.pinguino_comprable = bool


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
