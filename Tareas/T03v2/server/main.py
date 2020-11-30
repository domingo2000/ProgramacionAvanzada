from networking import net_server
from juego.juego import Juego
import time
net_server.encender()

time.sleep(5)
juego = Juego(net_server.nombres_usuarios)
while True:
    pass
