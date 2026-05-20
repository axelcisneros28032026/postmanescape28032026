from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                               QGridLayout, QSizePolicy)

from config import fuente_nombre


class Ventanared(QWidget):

    signalAjustesRed = Signal(str, str)
    signalVolver = Signal()
    signalVolverInicio = Signal()

    def __init__(self):
        super().__init__()
        # Posicionamos el titulo a la ventana
        self.setWindowTitle("Conexión de red")

        layout = QGridLayout()

        self.label_ip=QLabel("Dirección IP:")
        self.input_ip=QLineEdit()
        self.input_ip.setPlaceholderText("ej. 192.168.1.2")
        self.input_ip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_puerto=QLabel("Puerto:")
        self.input_puerto=QLineEdit()
        self.input_puerto.setPlaceholderText("ej. 25565")

        self.boton=QPushButton("Conectar")
        self.pushButton_Volver = QPushButton("←")
        self.pushButton_Volver.setFixedSize(64, 64)
        self.pushButton_VolverInicio = QPushButton("🏠")
        self.pushButton_VolverInicio.setFixedSize(64, 64)

        # Agregamos al layout
        layout.setSpacing(16)
        layout.setColumnStretch(0, 1)
        layout.setRowStretch(0, 1)
        layout.addWidget(self.pushButton_Volver, 1, 1, 1, 1)
        layout.addWidget(self.pushButton_VolverInicio, 1, 2, 1, 1)
        layout.addWidget(QLabel("Configuración de red"), 1, 3, 1, 1)
        layout.addWidget(self.label_ip, 2, 3, 1, 1)
        layout.addWidget(self.input_ip, 3, 3, 1, 1)
        layout.addWidget(self.label_puerto, 4, 3, 1, 1)
        layout.addWidget(self.input_puerto, 5, 3, 1, 1)
        layout.addWidget(self.boton, 6, 3, 1, 1)
        layout.setColumnStretch(10, 1)
        layout.setRowStretch(10, 1)

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

        self.setLayout(layout)

        # Eventos y Métodos
        self.boton.clicked.connect(self.signalAjustesRed_emitir)
        self.pushButton_Volver.clicked.connect(lambda: self.signalVolver.emit())
        self.pushButton_VolverInicio.clicked.connect(lambda: self.signalVolverInicio.emit())

    def signalAjustesRed_emitir(self):
        ip = self.input_ip.text()
        puerto = self.input_puerto.text()
        self.signalAjustesRed.emit(ip, puerto)


if __name__ == "__main__":
    app = QApplication()
    ventana = Ventanared()
    ventana.show()
    app.exec()