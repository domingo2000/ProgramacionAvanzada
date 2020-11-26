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
    back_juego.senal_abrir_sala_espera.connect(ventana_espera.show)
    back_juego.senal_abrir_ventana_juego.connect(ventana_juego.show)
    back_juego.senal_cerrar_sala_espera.connect(ventana_espera.hide)
    back_juego.senal_cerrar_ventana_juego.connect(ventana_juego.hide)

    back_juego.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)
    back_juego.senal_servidor_lleno.connect(ventana_espera.actualizar_label_sala_espera)

    back_juego.senal_actualizar_num_ficha.connect(ventana_juego.actualizar_num_ficha)
    back_juego.senal_actualizar_materia_prima_hexagono.connect(
        ventana_juego.actualizar_materia_prima_hexagono)
    back_juego.senal_cambiar_label_usuario.connect(ventana_juego.actualizar_label_usuario)
    ventana_espera.show()
    sys.exit(app.exec_())
