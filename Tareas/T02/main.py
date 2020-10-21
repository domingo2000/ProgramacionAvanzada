import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_juego import VentanaJuego
from backend.back_ranking import ProcesadorRanking

if __name__ == "__main__":
    app = QApplication([])
    # Instancia ventanas que se van a usar
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_juego = VentanaJuego()

    # Instancia procesadores back end
    procesador_ranking = ProcesadorRanking()
    # Coneccion señales entre ventanas
    # Inicio y ranking
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    # Inicio y Juego
    ventana_inicio.senal_abrir_ventana_juego.connect(ventana_juego.show)

    # Coneccion señales back-front ranking
    ventana_ranking.senal_procesar_puntajes = procesador_ranking.senal_procesar_puntajes
    procesador_ranking.senal_actualizar_puntaje = ventana_ranking.senal_actualizar_puntajes

    sys.exit(app.exec_())
