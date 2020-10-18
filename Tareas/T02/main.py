import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ranking import VentanaRanking

if __name__ == "__main__":
    app = QApplication([])
    # Instancia ventanas que se van a usar
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()

    # Coneccion señales entre ventanas
    ventana_inicio.senal_abrir_ventana_ranking.connect(ventana_ranking.senal_abrir_ventana_ranking)
    ventana_ranking.senal_abrir_ventana_inicio.connect(ventana_inicio.show)

    sys.exit(app.exec_())
