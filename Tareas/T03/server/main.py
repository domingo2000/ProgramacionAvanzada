from server import Server
from networking import ServerNet
import json
import time

if __name__ == "__main__":
    with open("parametros.json") as file:
        data = json.load(file)
    server = Server(data["host"], data["port"])

