from networking import net_server
from juego.juego import Juego
import time
net_server.encender()

try:
    while not net_server.lleno():
        pass

    net_server.send_command_to_all("msg_wait_room", "Comenzando Partida")
    time.sleep(2)
    juego = Juego(net_server.nombres_usuarios)

finally:
    net_server.socket_server.close()
