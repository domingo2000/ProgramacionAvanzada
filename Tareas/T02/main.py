import sys
from os import path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_resumen import VentanaResumen
from backend.back_ranking import BackRanking
from backend.backend_juego import BackJuego
from backend.backend_inicio import BackInicio
from entidades.nivel import Nivel
from entidades.pinguino import Pinguino
import parametros as p
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
    back_juego = BackJuego(nivel)

    # Pinguinos de la tienda
    pos_pinguino_amarillo = QPoint(0, 180)
    pos_pinguino_celeste = QPoint(90, 180)
    pos_pinguino_morado = QPoint(0, 280)
    pos_pinguino_verde = QPoint(90, 280)
    pos_pinguino_rojo = QPoint(45, 380)
    pinguino_morado = Pinguino(ventana_juego.tienda, "morado",
                               path.join(*p.IMAGENES["pinguino_morado_neutro"]),
                               qpoint=pos_pinguino_morado)
    pinguino_verde = Pinguino(ventana_juego.tienda, "verde",
                              path.join(*p.IMAGENES["pinguino_verde_neutro"]),
                              qpoint=pos_pinguino_verde)
    pinguino_rojo = Pinguino(ventana_juego.tienda, "rojo",
                             path.join(*p.IMAGENES["pinguino_rojo_neutro"]),
                             qpoint=pos_pinguino_rojo)
    pinguino_celeste = Pinguino(ventana_juego.tienda, "celeste",
                                path.join(*p.IMAGENES["pinguino_celeste_neutro"]),
                                qpoint=pos_pinguino_celeste)
    pinguino_amarillo = Pinguino(ventana_juego.tienda, "amarillo",
                                 path.join(*p.IMAGENES["pinguino_amarillo_neutro"]),
                                 qpoint=pos_pinguino_amarillo)
    pinguinos_creados = [pinguino_verde, pinguino_rojo, pinguino_morado,
                         pinguino_celeste, pinguino_amarillo]
    back_juego.pinguinos_tienda = pinguinos_creados

    # Coneccion senales ventana Juego con nivel
    ventana_juego.senal_teclas_presionadas.connect(back_juego.nivel.manejar_teclas)
    nivel.senal_actualizar_combo.connect(ventana_juego.actualizar_label_combo)
    nivel.senal_actualizar_combo_maximo.connect(ventana_juego.actualizar_label_combo_maximo)
    nivel.senal_actualizar_progreso.connect(ventana_juego.actualizar_progressbar_progreso)
    nivel.senal_actualizar_aprobacion.connect(ventana_juego.actualizar_progressbar_aprobacion)
    nivel.senal_esconder_juego.connect(ventana_juego.hide)
    nivel.senal_juego_terminado.connect(back_juego.borrar_juego)
    nivel.senal_escribir_puntaje_en_ranking.connect(back_juego.escribir_puntaje_en_ranking)
    nivel.senal_enviar_dinero.connect(back_juego.actualizar_dinero_tienda)
    nivel.senal_nivel_comenzado.connect(ventana_juego.manejar_nivel_comenzado)
    nivel.senal_nivel_terminado.connect(ventana_juego.manejar_nivel_terminado)
    nivel.senal_paso_correcto.connect(back_juego.hacer_bailar_pinguinos)
    ventana_juego.senal_cargar_nivel.connect(back_juego.generar_nivel)

    # Coneccion señales entre ventanas
    # Inicio y ranking
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)
    # Inicio y Ventana Juego
    back_inicio.senal_abrir_ventana_juego.connect(ventana_juego.comenzar_nuevo_juego)
    back_juego.senal_abrir_inicio.connect(ventana_inicio.show)
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
    ventana_juego.senal_salir_juego.connect(back_juego.salir)
    ventana_juego.senal_fijar_usuario.connect(back_juego.fijar_usuario)
    ventana_juego.senal_compra_realizada.connect(back_juego.realizar_compra)
    back_juego.senal_nivel_cargado.connect(nivel.setear_nivel_cargado)
    ventana_juego.senal_pinguinos_creados.connect(back_juego.setear_pinguinos_tienda)
    back_juego.senal_cambiar_dinero_tienda.connect(ventana_juego.actualizar_label_dinero_tienda)
    for pinguino in back_juego.pinguinos_tienda:
        back_juego.senal_compra_valida.connect(pinguino.set_pinguino_comprable)
        pinguino.senal_pinguino_clickeado.connect(back_juego.chequear_compra)
    sys.exit(app.exec_())
