from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QObject, QUrl

class Objeto(QObject):

    def __init__(self):
        super().__init__()
        url = QUrl()
        url = url.fromLocalFile("cancion_1.wav")
        print(url)
        content = QMediaContent(url)
        print(content)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        print(self.player.supportedAudioRoles())

objeto = Objeto()