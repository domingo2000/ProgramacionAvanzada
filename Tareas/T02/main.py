import sys
from PyQt5.QtWidgets import QApplication
from frontend.front_inicio import VentanaInicio
from frontend.front_juego import VentanaJuego
from frontend.front_ranking import VentanaRanking
from frontend.front_resumen import VentanaResumen
from backend.back_inicio import BackInicio
from backend.back_juego import BackJuego
from backend.back_ranking import BackRanking
from entidades.pinguinos import Pinguino

if __name__ == "__main__":
    app = QApplication([])

    # Instancias front y back
    ventana_inicio = VentanaInicio()
    ventana_juego = VentanaJuego()
    ventana_ranking = VentanaRanking()
    ventana_resumen = VentanaResumen()
    back_inicio = BackInicio()
    back_juego = BackJuego()
    back_ranking = BackRanking()

    # Coneccion senales back front
    # Incio
    ventana_inicio.senal_verificar_usuario.connect(back_inicio.verificar_usuario)
    ventana_inicio.senal_abrir_ranking.connect(ventana_ranking.abrir)
    back_inicio.senal_cerrar_inicio.connect(ventana_inicio.hide)
    back_inicio.senal_usuario_incorrecto.connect(ventana_inicio.alerta_usuario_incorrecto)
    # Juego
    ventana_juego.senal_comenzar_juego.connect(back_juego.comenzar_juego)
    ventana_juego.senal_comenzar_ronda.connect(back_juego.comenzar_ronda)
    ventana_juego.senal_juego_terminado.connect(back_juego.terminar_juego)
    ventana_juego.senal_teclas_presionadas.connect(back_juego.ronda.revisar_teclas)
    ventana_juego.senal_teclas_presionadas.connect(back_juego.revisar_cheatcodes)
    ventana_juego.senal_pausar_juego.connect(back_juego.ronda.pausar)
    ventana_juego.senal_reanudar_juego.connect(back_juego.ronda.reanudar)
    ventana_juego.senal_pinguino_dropeado.connect(back_juego.manejar_dropeo)
    ventana_juego.senal_jugar_solo.connect(back_juego.jugar_solo)
    back_juego.ronda.senal_actualizar_combo.connect(ventana_juego.actualizar_combo)
    back_juego.ronda.senal_actualizar_combo_maximo.connect(ventana_juego.actualizar_combo_maximo)
    back_juego.ronda.senal_actualizar_progreso.connect(ventana_juego.actualizar_barra_progreso)
    back_juego.ronda.senal_actualizar_aprobacion.connect(ventana_juego.actualizar_barra_aprobacion)
    back_juego.ronda.senal_activar_boton_jugar_solo.connect(ventana_juego.activar_boton_jugar_solo)
    back_juego.ronda.senal_paso_correcto.connect(back_juego.hacer_bailar_pinguinos)
    back_juego.ronda.senal_despintar_zona_captura.connect(ventana_juego.despintar_zona_captura)
    back_juego.ronda.senal_pintar_tecla.connect(ventana_juego.actualizar_zona_captura)
    back_juego.senal_actualizar_dinero_tienda.connect(ventana_juego.actualizar_dinero_tienda)
    back_juego.senal_escribir_puntaje_ranking.connect(back_ranking.escribir_puntaje)
    back_juego.senal_juego_terminado.connect(ventana_juego.reiniciar_botones)
    back_juego.senal_activar_boton_comenzar.connect(ventana_juego.activar_boton_comenzar)
    back_juego.senal_mostrar_ventana_resumen.connect(ventana_resumen.actualizar)
    back_juego.ronda.senal_calcular_estadisticas.connect(back_juego.calcular_estadisticas)
    back_juego.senal_esconder_juego.connect(ventana_juego.hide)
    back_juego.senal_activar_boton_jugar_solo.connect(ventana_juego.activar_boton_jugar_solo)
    back_juego.senal_desactivar_boton_comenzar.connect(ventana_juego.desactivar_boton_comenzar)
    back_juego.ronda.senal_activar_boton_comenzar.connect(ventana_juego.activar_boton_comenzar)
    back_juego.senal_desactivar_opciones.connect(ventana_juego.activar_opciones)
    back_juego.ronda.senal_desactivar_opciones.connect(ventana_juego.activar_opciones)
    # Inicio y Juego
    ventana_juego.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    back_inicio.senal_abrir_juego.connect(ventana_juego.comenzar)
    back_inicio.senal_enviar_nombre_usario.connect(back_juego.set_usuario)

    # ranking
    ventana_ranking.senal_actualizar_puntajes.connect(back_ranking.ordenar_puntajes)
    back_ranking.senal_actualizar_puntaje.connect(ventana_ranking.actualizar_puntajes)

    # Resumen
    ventana_resumen.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    ventana_resumen.senal_abrir_ventana_juego.connect(ventana_juego.show)
    ventana_resumen.senal_abrir_ventana_juego.connect(ventana_juego.tienda.show)

    # Pinguinos Tienda
    pinguino_rojo = Pinguino("rojo", ventana_juego.tienda, pos=(0, 180))
    pinguino_amarillo = Pinguino("amarillo", ventana_juego.tienda, pos=(90, 180))
    pinguino_verde = Pinguino("verde", ventana_juego.tienda, pos=(0, 280))
    pinguino_celeste = Pinguino("celeste", ventana_juego.tienda, pos=(90, 280))
    pinguino_morado = Pinguino("morado", ventana_juego.tienda, pos=(45, 380))
    back_juego.pinguinos_tienda.add(pinguino_amarillo)
    back_juego.pinguinos_tienda.add(pinguino_celeste)
    back_juego.pinguinos_tienda.add(pinguino_rojo)
    back_juego.pinguinos_tienda.add(pinguino_verde)
    back_juego.pinguinos_tienda.add(pinguino_morado)

    for pinguino in back_juego.pinguinos_tienda:
        back_juego.senal_compra_valida.connect(pinguino.set_pinguino_comprable)
        pinguino.senal_pinguino_clickeado.connect(back_juego.chequear_compra)
    ventana_inicio.show()
    sys.exit(app.exec_())
