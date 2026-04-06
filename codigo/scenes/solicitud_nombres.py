import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QApplication, QPushButton, QGridLayout
)

from config import fuente_nombre


class VentanaRegistro(QWidget):

    signalRegistro = Signal(str)
    signalVolver = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Jugadores")

        layout = QGridLayout(self)

        self.fuentes = fuente_nombre()

        # Estilos (fondo negro, texto amarillo)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: black;
            }}
            QLabel {{
                color: yellow;
                font-family: '{fuente_nombre()}';
                font-size: 50px;
            }}
            QLineEdit {{
                background-color: #222;
                color: yellow;
                border: 1px solid yellow;
                height: 64px;
                font-family: '{fuente_nombre()}';
                font-size: 50px;
            }}
            QPushButton {{
                background-color: black;
                color: yellow;
                border: 1px solid yellow;
                height: 64px;
                font-family: '{fuente_nombre()}';
                font-size: 50px;
            }}
            QPushButton:hover {{
                background-color: #333;
                font-family: '{fuente_nombre()}';
                font-size: 50px;
                height: 64px;
            }}
        """)

        titulo = QLabel("Registro")

        titulo.setAlignment(Qt.AlignCenter)

        label_j1 = QLabel("Jugador")
        self.input_j1 = QLineEdit()

        # Botón guardar (no hace nada)
        boton_guardar = QPushButton("Guardar")
        pushButton_Volver = QPushButton("←")
        pushButton_Volver.setFixedSize(64, 64)

        layout.setSpacing(16)
        layout.setColumnStretch(0, 1)
        layout.setRowStretch(0, 1)
        layout.addWidget(pushButton_Volver, 1, 1, 1, 1)
        layout.addWidget(titulo, 1, 2, 1, 1)
        layout.addWidget(label_j1, 2, 2, 1, 1)
        layout.addWidget(self.input_j1, 3, 2, 1, 1)
        layout.addWidget(boton_guardar, 6, 2, 1, 1)
        layout.setColumnStretch(10, 1)
        layout.setRowStretch(10, 1)

        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

    # Eventos y Métodos
        boton_guardar.clicked.connect(self.signalRegistro_emitir)
        pushButton_Volver.clicked.connect(self.signalVolver_emitir)

    def signalVolver_emitir(self):
        estadoVolver = True
        self.signalVolver.emit(estadoVolver)

    def signalRegistro_emitir(self):
        j1 = self.input_j1.text()

        self.signalRegistro.emit(j1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec())