from PyQt5.QtCore import QTimer, QEventLoop


def sleep(tiempo):
    loop = QEventLoop()
    QTimer.singleShot(1000 * tiempo, loop.quit)
    loop.exec_()
