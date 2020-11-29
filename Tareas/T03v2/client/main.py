from PyQt5.QtWidgets import QApplication
from backend.back_cliente import BackCliente
from frontend.front_sala_espera import VentanaEspera
from backend.networking import net_cliente
import sys

if __name__ == "__main__":
    app = QApplication([])
    ventana_espera = VentanaEspera()
    back_cliente = BackCliente()

    # Conexion senales de back a front sala espera
    back_cliente.senal_abrir_sala_espera.connect(ventana_espera.show)
    back_cliente.senal_cerrar_sala_espera.connect(ventana_espera.hide)
    back_cliente.senal_anadir_usuario.connect(ventana_espera.anadir_usuario)
    back_cliente.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)

    # Conexion back a front ventana juego
    """
    back_cliente.senal_cerrar_ventana_juego.connect(ventana_juego.hide)
    back_cliente.senal_abrir_ventana_juego.connect(ventana_juego.show)
    """
    net_cliente.encender()
    ventana_espera.show()
    sys.exit(app.exec_())
