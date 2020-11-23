from back_server import BackServer
from networking import ServerNet

if __name__ == "__main__":
    back_server = BackServer()
    net_server = ServerNet()

    # Conexion señales
    back_server.senal_enviar_comando.connect(net_server.send_command)
    back_server.senal_enviar_log.connect(net_server.log)
