from PyQt5.QtWidgets import QApplication
from backend.back_cliente import BackCliente
from frontend.front_sala_espera import VentanaEspera
from frontend.front_ventana_juego import VentanaJuego
from backend.networking import net_cliente
import sys
import time


if __name__ == "__main__":
    app = QApplication([])
    ventana_espera = VentanaEspera()
    a = time.time()
    ventana_juego = VentanaJuego()
    print(time.time() - a)
    back_cliente = BackCliente()

    # Conexion senales de back a front sala espera
    back_cliente.senal_abrir_sala_espera.connect(ventana_espera.show)
    back_cliente.senal_cerrar_sala_espera.connect(ventana_espera.hide)
    back_cliente.senal_anadir_usuario.connect(ventana_espera.anadir_usuario)
    back_cliente.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)

    # Conexion back a front ventana juego
    back_cliente.senal_cerrar_ventana_juego.connect(ventana_juego.hide)
    back_cliente.senal_abrir_ventana_juego.connect(ventana_juego.show)

    # Senales de carga de juego
    back_cliente.senal_cargar_hexagono.connect(ventana_juego.actualizar_materia_prima_hexagono)
    back_cliente.senal_cargar_num_ficha.connect(ventana_juego.actualizar_num_ficha)
    back_cliente.senal_cargar_nombre_usuario.connect(ventana_juego.actualizar_label_usuario)

    # Senales actualizar datos juego
    back_cliente.senal_actualizar_materia_prima.connect(ventana_juego.actualizar_materia_prima)
    back_cliente.senal_actualizar_puntos_usuario.connect(ventana_juego.actualizar_puntos_usuario)
    net_cliente.encender()
    ventana_espera.show()
    ventana_juego.show()
    sys.exit(app.exec_())
