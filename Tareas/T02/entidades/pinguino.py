from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtCore import QRect, QMimeData, Qt, QPoint, QSize, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QDrag, QBitmap
import sys
from os import path
import parametros as p
from backend.funciones import sleep
import random


class Pinguino(QLabel):
    senal_pinguino_clickeado = pyqtSignal()
    senal_cambiar_frame = pyqtSignal(QLabel, QPixmap)

    def __init__(self, parent, color, ruta_imagen=None, qpoint=QPoint(0, 0), iscopy=False):
        super().__init__(parent=parent)
        # Atributos pinguino
        self.pinguino_comprable = False
        self.color = color
        self.iscopy = iscopy
        self.init_gui(qpoint)
        # atributos
        self.colider = QRect(self.pos(), self.size())
        self.ruta_imagen = ruta_imagen
        self.show()

    def init_gui(self, qpoint):
        ruta_imagen = path.join(*p.IMAGENES[f"pinguino_{self.color}_neutro"])
        self.pixmap_neutro = QPixmap(ruta_imagen)
        self.setStyleSheet("background-color: transparent;")
        self.setGeometry(qpoint.x(), qpoint.y(), 100, 100)
        self.setPixmap(self.pixmap_neutro)
        self.setScaledContents(True)

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
        if (event.pos() - self.drag_start_position).manhattanLength() \
           < QApplication.startDragDistance():
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

    def bailar(self, flechas_paso):
        if not(self.iscopy):
            return
        else:
            direcciones = {flecha.direccion for flecha in flechas_paso}
            if len(direcciones) == 4:
                ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_cuatro_flechas"]
                print("Cuatro Flechas")
            elif len(direcciones) == 3:
                ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_tres_flechas"]
                print("Tres Flechas")
            elif "arriba" in direcciones:
                if {"arriba", "derecha"}.issubset(direcciones):
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_arriba_derecha"]
                    print("arriba", "derecha")
                elif {"arriba", "izquierda"}.issubset(direcciones):
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_arriba_izquierda"]
                    print("arriba", "izquierda")
                else:
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_arriba"]
                    print("arriba")
            elif "abajo" in direcciones:
                if {"abajo", "derecha"}.issubset(direcciones):
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_abajo_derecha"]
                    print("abajo", "derecha")
                elif {"abajo", "izquierda"}.issubset(direcciones):
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_abajo_derecha"]
                    print("abajo", "izquierda")
                else:
                    ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_arriba"]
                    print("abajo")
            elif "derecha" in direcciones:
                ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_derecha"]
                print("derecha")
            elif "izquierda" in direcciones:
                ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_izquierda"]
                print("izquierda")
            else:
                ruta_pixmap_paso = p.IMAGENES[f"pinguino_{self.color}_cuatro_flechas"]
                print("Baile random")
            pixmap_paso = QPixmap(path.join(*ruta_pixmap_paso))
            self.realizar_paso(pixmap_paso)

    def realizar_paso(self, pixmap_paso):
        self.timer_paso_baile = QTimer()
        self.timer_paso_baile.setSingleShot(True)
        self.timer_paso_baile.setInterval(p.DELAY_PASO)
        self.timer_paso_baile.timeout.connect(self.cambiar_a_frame_neutral)
        self.senal_cambiar_frame.emit(self, pixmap_paso)
        self.timer_paso_baile.start()

    def cambiar_a_frame_neutral(self):
        self.senal_cambiar_frame.emit(self, self.pixmap_neutro)


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
