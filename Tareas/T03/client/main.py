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
    back_juego.senal_actualizar_usuarios.connect(ventana_espera.actualizar_usuarios)
    back_juego.senal_servidor_lleno.connect(ventana_espera.actualizar_label_sala_espera)
    ventana_espera.show()
    sys.exit(app.exec_())
