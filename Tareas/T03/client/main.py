import sys
from frontend.front_sala_espera import VentanaEspera
from frontend.front_ventana_juego import VentanaJuego
from backend.back_cliente import BackVentanaJuego
from networking import ClientNet
from PyQt5.QtWidgets import QApplication

# Instancia Front cliente y back

# Main thread
if __name__ == "__main__":
    app = QApplication([])
    ventana_espera = VentanaEspera()
    ventana_juego = VentanaJuego()
    back_juego = BackVentanaJuego()
    net_cliente = ClientNet()

    net_cliente.senal_comando.connect(back_juego.realizar_comando)
    net_cliente.senal_comando.connect(ventana_espera.realizar_comando)
    net_cliente.senal_comando.connect(ventana_juego.realizar_comando)

    back_juego.senal_actualizar_materia_prima_hexagono.connect(
        ventana_juego.actualizar_materia_prima_hexagono)
    back_juego.senal_actualizar_num_ficha.connect(ventana_juego.actualizar_num_ficha)

    ventana_espera.show()

    sys.exit(app.exec_())
