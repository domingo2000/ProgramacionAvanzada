import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_juego import VentanaJuego
from backend.back_ranking import ProcesadorRanking
from backend.backend_juego import BackJuego
from entidades.nivel import Nivel

if __name__ == "__main__":
    app = QApplication([])
    # Instancia ventanas que se van a usar
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_juego = VentanaJuego()
    # Instancia procesadores back end
    procesador_ranking = ProcesadorRanking()
    # Instancia un nivel que sera usado en la clase juego
    nivel = Nivel(ventana_juego)
    juego = BackJuego(nivel)

    # Coneccion senales ventana Juego con nivel
    ventana_juego.senal_teclas_presionadas.connect(juego.nivel.manejar_teclas)
    nivel.senal_actualizar_combo.connect(ventana_juego.actualizar_label_combo)
    nivel.senal_actualizar_combo_maximo.connect(ventana_juego.actualizar_label_combo_maximo)
    nivel.senal_actualizar_progreso.connect(ventana_juego.actualizar_progressbar_progreso)
    nivel.senal_actualizar_aprobacion.connect(ventana_juego.actualizar_progressbar_aprobacion)
    ventana_juego.senal_cargar_nivel.connect(juego.generar_nivel)

    # Coneccion señales entre ventanas
    # Inicio y ranking
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    # Inicio y Ventana Juego
    ventana_inicio.senal_abrir_ventana_juego.connect(ventana_juego.show)

    # Coneccion señales back-front ranking
    ventana_ranking.senal_procesar_puntajes = procesador_ranking.senal_procesar_puntajes
    procesador_ranking.senal_actualizar_puntaje = ventana_ranking.senal_actualizar_puntajes

    sys.exit(app.exec_())
