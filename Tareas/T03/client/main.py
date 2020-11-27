import sys
from frontend.front_sala_espera import VentanaEspera
from frontend.front_ventana_juego import VentanaJuego
from backend.back_cliente import BackVentanaJuego
from PyQt5.QtWidgets import QApplication
import json
import time
# Instancia Front cliente y back

# Main thread
if __name__ == "__main__":
    with open("parametros.json") as file:
        data = json.load(file)

    app = QApplication([])
    ventana_espera = VentanaEspera()
    ventana_juego = VentanaJuego()
    back_juego = BackVentanaJuego(data["host"], data["port"])

    #  CONEXIONES FRONT BACK
    #  De back a ventanas
    back_juego.senal_abrir_sala_espera.connect(ventana_espera.show)
    back_juego.senal_abrir_ventana_juego.connect(ventana_juego.show)
    back_juego.senal_cerrar_sala_espera.connect(ventana_espera.hide)
    back_juego.senal_cerrar_ventana_juego.connect(ventana_juego.hide)

    back_juego.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)
    back_juego.senal_actualizar_materias_primas.connect(ventana_juego.actualizar_materias_primas)
    back_juego.senal_actualizar_puntos.connect(ventana_juego.actualizar_labels_puntos)
    back_juego.senal_actualizar_jugador_actual.connect(
        ventana_juego.actualizar_label_jugador_actual)
    back_juego.senal_servidor_lleno.connect(ventana_espera.actualizar_label_sala_espera)

    back_juego.senal_actualizar_num_ficha.connect(ventana_juego.actualizar_num_ficha)
    back_juego.senal_actualizar_materia_prima_hexagono.connect(
        ventana_juego.actualizar_materia_prima_hexagono)
    back_juego.senal_actualizar_construcciones.connect(ventana_juego.actualizar_construcciones)
    back_juego.senal_cambiar_label_usuario.connect(ventana_juego.actualizar_label_usuario)
    back_juego.senal_actualizar_dados.connect(ventana_juego.actualizar_dados)

    back_juego.senal_activar_interfaz.connect(ventana_juego.activar_interfaz)
    back_juego.senal_activar_boton_dados.connect(ventana_juego.activar_interfaz_dados)
    back_juego.senal_realizar_monopolio.connect(ventana_juego.realizar_monopolio)

    #  De ventana a back6
    ventana_juego.senal_lanzar_dados.connect(back_juego.lanzar_dados)
    ventana_juego.senal_comprar_carta_desarrollo.connect(back_juego.comprar_carta_desarrollo)
    ventana_juego.senal_monopolio_realizado.connect(back_juego.enviar_info_monopolio)
    ventana_espera.show()
    sys.exit(app.exec_())
