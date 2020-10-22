import sys
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import QTimer, QObject


class Timer(QObject):

    def _init__(self, tiempo, funcion):
        super().__init__()
        self.timer = QTimer()
        self.tiempo = tiempo
        self.timer.setInterval(self.tiempo)
        self.timer.timeout.connect(funcion)


class Animacion(QObject):

    def __init__(self, label, delay, lista_pixmaps):
        super().__init__()
        self.frames = lista_pixmaps
        self.timer = QTimer()
        self.delay = delay
        self.duracion = self.delay * len(self.frames)
        self.label = label
        self.frame_actual = -1
        self.timer.setInterval(self.delay)
        self.timer.timeout.connect(self.actualizar_frame)
        self.infinito = False

    def actualizar_frame(self):
        print(self.frames)
        if self.frame_actual == (len(self.frames) - 1):
            if not(self.infinito):
                self.label.setVisible(False)
                self.timer.stop()
            self.frame_actual = 0
        else:
            self.frame_actual += 1

        print(self.frame_actual)
        imagen = self.frames[self.frame_actual]
        self.label.setPixmap(imagen)
        self.label.repaint()

    def comenzar(self):
        print("Animando")
        self.timer.start()


if __name__ == "__main__":
    app = QApplication([])
    label = QLabel()
    animacion = Animacion(label, 100, [i for i in range(4)])
    animacion.timer.start()
    sys.exit(app.exec_())
