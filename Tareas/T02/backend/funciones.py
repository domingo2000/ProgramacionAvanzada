from PyQt5.QtCore import QTimer, QEventLoop


def sleep(tiempo, milisec=False):
    if milisec:
        multiplicador = 1
    else:
        multiplicador = 1000
    loop = QEventLoop()
    QTimer.singleShot(multiplicador * tiempo, loop.quit)
    loop.exec_()


class Cronometro(QTimer):

    def __init__(self):
        super().__init__()
        self.segundo = 0
        self.setInterval(1)
        self.timeout.connect(self.anadir_segundo)

    def anadir_segundo(self):
        self.segundo += 0.001
