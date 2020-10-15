import os
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap


class VentanaInicial(QWidget):

    senal_comparar_codigo = pyqtSignal(str)
    senal_abrir_menu_principal = pyqtSignal()

    def __init__(self, ancho, alto, ruta_logo):
        """Es el init de la ventana del menú de inicio. Puedes ignorarlo."""
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.init_gui(ruta_logo)

    def init_gui(self, ruta_logo):
        # Logo
        self.label_logo = QLabel()
        self.label_logo.size = (self.size)
        imagen_logo = QPixmap(ruta_logo)
        self.label_logo.setPixmap(imagen_logo)
        self.label_logo.setScaledContents(True)

        # Campo de texto
        label_texto = QLabel("Ingrese el codigo de su partida:")
        self.input_codigo = QLineEdit()
        hbox_entrada = QHBoxLayout()
        hbox_entrada.addStretch(1)
        hbox_entrada.addWidget(label_texto)
        hbox_entrada.addWidget(self.input_codigo)
        hbox_entrada.addStretch(1)

        # Boton
        hbox_boton = QHBoxLayout()
        boton_ingesar = QPushButton("Ingresar")
        hbox_boton.addWidget(boton_ingesar)
        boton_ingesar.clicked.connect(self.comparar_codigo)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_logo)
        vbox.addLayout(hbox_entrada)
        vbox.addLayout(hbox_boton)
        self.setLayout(vbox)
        pass

    def comparar_codigo(self):
        """Método que emite la señal para comparar el código. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        codigo = self.input_codigo.text()
        self.senal_comparar_codigo.emit(codigo)

    def recibir_comparacion(self, son_iguales):
        """Método que recibe el resultado de la comparación. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        if not son_iguales:
            self.input_codigo.clear()
            self.input_codigo.setPlaceholderText("¡Inválido! Debe ser un código existente.")
        else:
            self.hide()
            self.senal_abrir_menu_principal.emit()
