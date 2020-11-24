import sys
from frontend.front_sala_espera import VentanaEspera
from networking import ClientNet
from PyQt5.QtWidgets import QApplication

# Instancia Front cliente y back

# Main thread
if __name__ == "__main__":
    app = QApplication([])
    ventana_espera = VentanaEspera()
    net_cliente = ClientNet()

    net_cliente.senal_comando.connect(ventana_espera.realizar_comando)
    ventana_espera.show()

    sys.exit(app.exec_())
