import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_resumen import VentanaResumen
from backend.back_ranking import BackRanking
from backend.backend_juego import BackJuego
from backend.backend_inicio import BackInicio
from entidades.nivel import Nivel

if __name__ == "__main__":
    app = QApplication([])
    # Instancia ventanas que se van a usar
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_juego = VentanaJuego()
    ventana_resumen = VentanaResumen()
    # Instancia procesadores back end
    back_ranking = BackRanking()
    back_inicio = BackInicio()
    # Instancia un nivel que sera usado en la clase juego
    nivel = Nivel(ventana_juego)
    juego = BackJuego(nivel)

    # Coneccion senales ventana Juego con nivel
    ventana_juego.senal_teclas_presionadas.connect(juego.nivel.manejar_teclas)
    nivel.senal_actualizar_combo.connect(ventana_juego.actualizar_label_combo)
    nivel.senal_actualizar_combo_maximo.connect(ventana_juego.actualizar_label_combo_maximo)
    nivel.senal_actualizar_progreso.connect(ventana_juego.actualizar_progressbar_progreso)
    nivel.senal_actualizar_aprobacion.connect(ventana_juego.actualizar_progressbar_aprobacion)
    nivel.senal_esconder_juego.connect(ventana_juego.hide)
    nivel.senal_juego_terminado.connect(juego.borrar_juego)
    nivel.senal_escribir_puntaje_en_ranking.connect(juego.escribir_puntaje_en_ranking)
    ventana_juego.senal_cargar_nivel.connect(juego.generar_nivel)

    # Coneccion señales entre ventanas
    # Inicio y ranking
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    # Inicio y Ventana Juego
    back_inicio.senal_abrir_ventana_juego.connect(ventana_juego.comenzar_nuevo_juego)
    juego.senal_abrir_inicio.connect(ventana_inicio.show)
    # Nivel con Ventana Resumen
    nivel.senal_abrir_ventana_resumen.connect(ventana_resumen.actualizar)
    # Ventana Resumen con Juego
    ventana_resumen.senal_abrir_ventana_juego.connect(ventana_juego.show)
    ventana_resumen.senal_abrir_ventana_inicio.connect(ventana_inicio.show)

    # Coneccion señales back-front ranking
    # Ventana Inicio
    ventana_inicio.senal_revisar_usuario.connect(back_inicio.chequear_usuario)
    back_inicio.senal_cerrar_ventana_inicio.connect(ventana_inicio.hide)
    back_inicio.senal_usuario_incorrecto.connect(ventana_inicio.alerta_usuario_incorrecto)
    # Ventana Ranking
    ventana_ranking.senal_procesar_puntajes = back_ranking.senal_procesar_puntajes
    back_ranking.senal_actualizar_puntaje = ventana_ranking.senal_actualizar_puntajes
    # Ventana Juego
    ventana_juego.senal_salir_juego.connect(juego.salir)
    ventana_juego.senal_fijar_usuario.connect(juego.fijar_usuario)
    juego.senal_nivel_cargado.connect(nivel.setear_nivel_cargado)

    sys.exit(app.exec_())
