from PyQt5.QtWidgets import QApplication
from backend.back_cliente import BackCliente
from frontend.front_sala_espera import VentanaEspera
from frontend.front_ventana_juego import VentanaJuego
from frontend.front_sala_termino import VentanaTermino
from backend.networking import net_cliente
import sys
import time


if __name__ == "__main__":
    app = QApplication([])
    ventana_espera = VentanaEspera()
    ventana_juego = VentanaJuego()
    ventana_termino = VentanaTermino()
    back_cliente = BackCliente()

    # Conexion senales de back a front sala espera
    back_cliente.senal_abrir_sala_espera.connect(ventana_espera.show)
    back_cliente.senal_cerrar_sala_espera.connect(ventana_espera.hide)
    back_cliente.senal_anadir_usuario.connect(ventana_espera.anadir_usuario)
    back_cliente.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)
    back_cliente.senal_mensaje_sala_espera.connect(ventana_espera.actualizar_label_sala_espera)
    # Conexion back a front ventana juego
    back_cliente.senal_cerrar_ventana_juego.connect(ventana_juego.hide)
    back_cliente.senal_abrir_ventana_juego.connect(ventana_juego.show)
    back_cliente.senal_alerta.connect(ventana_juego.alerta)
    back_cliente.senal_abrir_dialogo_punto_victoria.connect(
        ventana_juego.activar_dialogo_puntos_victoria
    )
    back_cliente.senal_abrir_dialogo_monopolio.connect(ventana_juego.activar_dialogo_monopolio)

    # Senales de carga de juego
    back_cliente.senal_cargar_hexagono.connect(ventana_juego.actualizar_materia_prima_hexagono)
    back_cliente.senal_cargar_num_ficha.connect(ventana_juego.actualizar_num_ficha)
    back_cliente.senal_cargar_nombre_usuario.connect(ventana_juego.actualizar_label_usuario)

    # Senales actualizar datos juego
    back_cliente.senal_actualizar_materia_prima.connect(ventana_juego.actualizar_materia_prima)
    back_cliente.senal_actualizar_puntos_usuario.connect(ventana_juego.actualizar_puntos_usuario)
    back_cliente.senal_actualizar_puntos_victoria_usuario.connect(
        ventana_juego.actualizar_puntos_victoria_usuario)
    back_cliente.senal_actualizar_jugador_actual.connect(
        ventana_juego.actualizar_label_jugador_actual)
    back_cliente.senal_actualizar_dados.connect(ventana_juego.actualizar_dados)
    # Senales construccion
    back_cliente.senal_eliminar_construccion.connect(ventana_juego.eliminar_construccion)
    back_cliente.senal_anadir_construccion.connect(ventana_juego.anadir_construccion)

    # Senales habilitar interfaz
    back_cliente.senal_habilitar_dados.connect(ventana_juego.habilitar_boton_dados)
    back_cliente.senal_habilitar_interfaz.connect(ventana_juego.habilitar_interfaz)
    back_cliente.senal_dar_usuarios_intercambio.connect(ventana_juego.abrir_ventana_intercambio_1)
    back_cliente.senal_abrir_dialogo_intercambio_2.connect(
        ventana_juego.abrir_ventana_intercambio_2)
    # senales front a back
    ventana_juego.senal_lanzar_dados.connect(back_cliente.lanzar_dados)
    ventana_juego.senal_comprar_carta_desarrollo.connect(back_cliente.comprar_carta_desarrollo)
    ventana_juego.senal_activar_carta_desarrollo.connect(back_cliente.activar_carta_desarrollo)
    ventana_juego.senal_pasar_turno.connect(back_cliente.pasar_turno)
    ventana_juego.senal_casa_dropeada.connect(back_cliente.enviar_choza_dropeada)
    ventana_juego.senal_pedir_usuarios_intercambio.connect(back_cliente.dar_usuarios_intercambio)
    ventana_juego.senal_proponer_intercambio.connect(back_cliente.proponer_intercambio)
    ventana_juego.senal_realizar_intercambio.connect(back_cliente.realizar_intercambio)
    # Senales back ventana termino
    back_cliente.senal_anadir_jugador_sala_termino.connect(ventana_termino.anadir_usuario)
    back_cliente.senal_actualizar_label_ganador.connect(ventana_termino.actualizar_label_ganador)
    back_cliente.senal_abrir_ventana_termino.connect(ventana_termino.show)

    net_cliente.encender()
    ventana_espera.show()
    sys.exit(app.exec_())
