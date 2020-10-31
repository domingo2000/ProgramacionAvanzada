from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, Qt, QPoint, QRect
from PyQt5.QtGui import QDrag, QPixmap
from parametros import IMAGENES_PINGUINO, DELAY_PASO
from os import path


class Pinguino(QLabel):
    senal_cambiar_frame = pyqtSignal(QLabel, QPixmap)
    senal_pinguino_clickeado = pyqtSignal()

    def __init__(self, color, parent, iscopy=False, pos=(0, 0)):
        super().__init__(parent)
        self.iscopy = iscopy
        self.pinguino_comprable = False
        self.color = color
        ruta_imagen = path.join(*IMAGENES_PINGUINO[f"{color}_neutro"])
        self.setGeometry(pos[0], pos[1], 100, 100)
        self.pixmap_neutro = QPixmap(ruta_imagen)
        self.setPixmap(self.pixmap_neutro)
        self.setScaledContents(True)
        self.setStyleSheet("background-color: transparent;")
        self.colider = QRect(self.pos(), self.size())
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
        if not (event.buttons() and Qt.LeftButton):
            return
        # Drag and Drop
        drag = QDrag(self)
        mimedata = QMimeData()
        drag.setMimeData(mimedata)
        drag.setPixmap(self.grab())
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
                ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_cuatro_flechas"]
                print("Cuatro Flechas")
            elif len(direcciones) == 3:
                ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_tres_flechas"]
                print("Tres Flechas")
            elif ("arriba" in direcciones) and not ("abajo" in direcciones):
                if {"arriba", "derecha"}.issubset(direcciones):
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_arriba_derecha"]
                    print("arriba", "derecha")
                elif {"arriba", "izquierda"}.issubset(direcciones):
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_arriba_izquierda"]
                    print("arriba", "izquierda")
                else:
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_arriba"]
                    print("arriba")
            elif ("abajo" in direcciones) and not ("arriba" in direcciones):
                if {"abajo", "derecha"}.issubset(direcciones):
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_abajo_derecha"]
                    print("abajo", "derecha")
                elif {"abajo", "izquierda"}.issubset(direcciones):
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_abajo_derecha"]
                    print("abajo", "izquierda")
                else:
                    ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_abajo"]
                    print("abajo")
            elif "derecha" in direcciones:
                ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_derecha"]
                print("derecha")
            elif "izquierda" in direcciones:
                ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_izquierda"]
                print("izquierda")
            else:
                ruta_pixmap_paso = IMAGENES_PINGUINO[f"{self.color}_cuatro_flechas"]
                print("Baile random")
            pixmap_paso = QPixmap(path.join(*ruta_pixmap_paso))
            self.realizar_paso(pixmap_paso)

    def realizar_paso(self, pixmap_paso):
        self.timer_paso_baile = QTimer()
        self.timer_paso_baile.setSingleShot(True)
        self.timer_paso_baile.setInterval(DELAY_PASO)
        self.timer_paso_baile.timeout.connect(self.cambiar_a_frame_neutral)
        self.senal_cambiar_frame.emit(self, pixmap_paso)
        self.timer_paso_baile.start()

    def cambiar_a_frame_neutral(self):
        self.senal_cambiar_frame.emit(self, self.pixmap_neutro)
