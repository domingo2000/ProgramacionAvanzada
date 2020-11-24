from server import Server
from networking import ServerNet
import json
import time

if __name__ == "__main__":
    with open("parametros.json") as file:
        data = json.load(file)
    server = Server(data["host"], data["port"])

    """
    while True:
        time.sleep(10)
        server.net.send_command_to_all("cargar_mapa", [server.mapa])
        server.net.send_command_to_all("hola", [1, 2, 3])
    """
