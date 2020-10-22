from PyQt5.QtCore import QTimer, QEventLoop


def sleep(tiempo, milisec=False):
    if milisec:
        multiplicador = 1
    else:
        multiplicador = 1000
    loop = QEventLoop()
    QTimer.singleShot(multiplicador * tiempo, loop.quit)
    loop.exec_()
