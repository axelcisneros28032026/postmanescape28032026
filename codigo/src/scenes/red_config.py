import socket

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QLabel,
                               QGridLayout, QSizePolicy, QFrame)

from config import fuente_nombre


def get_local_ip() -> str:
    """Obtiene la IP local de la máquina en la red LAN."""
    try:
        # Se conecta a una IP pública (sin enviar datos) para detectar la interfaz activa
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def is_port_available(port: int) -> bool:
    """Devuelve True si el puerto está libre para usar como servidor."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.close()
        return True
    except OSError:
        return False


class Ventanared(QWidget):

    signalAjustesRed = Signal(str, str)   # ip, puerto  → Cliente
    signalHostear    = Signal(str)        # puerto      → Servidor
    signalVolver = Signal()
    signalVolverInicio = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conexión de red")

        layout = QGridLayout()

        # ── Título ────────────────────────────────────────────────────────────
        self.label_titulo = QLabel("Configuración de red")

        # ── Puerto ────────────────────────────────────────────────────────────
        self.label_puerto = QLabel("Puerto:")
        self.input_puerto = QLineEdit()
        self.input_puerto.setPlaceholderText("ej. 25565")
        self.input_puerto.setText("25565")

        # ── Separador ─────────────────────────────────────────────────────────
        self.separador = QFrame()
        self.separador.setFrameShape(QFrame.HLine)
        self.separador.setStyleSheet("color: #444;")

        # ── Sección HOSTEAR ───────────────────────────────────────────────────
        self.label_host_titulo = QLabel("[ Hostear partida ]")
        self.label_host_titulo.setStyleSheet("color: #aaa; font-size: 30px;")

        self.label_tu_ip = QLabel("Tu IP en la red:")
        self.label_tu_ip.setStyleSheet("font-size: 30px; color: #aaa;")

        self.label_ip_valor = QLabel(get_local_ip())
        self.label_ip_valor.setStyleSheet(
            "color: cyan; font-size: 40px; letter-spacing: 2px;"
        )
        self.label_ip_valor.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.label_info_host = QLabel("")
        self.label_info_host.setStyleSheet("color: #888; font-size: 25px;")
        self.label_info_host.setAlignment(Qt.AlignCenter)

        self.pushButton_Host = QPushButton("Hostear  ▶")

        # ── Separador 2 ───────────────────────────────────────────────────────
        self.separador2 = QFrame()
        self.separador2.setFrameShape(QFrame.HLine)
        self.separador2.setStyleSheet("color: #444;")

        # ── Sección CONECTAR ──────────────────────────────────────────────────
        self.label_cliente_titulo = QLabel("[ Unirse a partida ]")
        self.label_cliente_titulo.setStyleSheet("color: #aaa; font-size: 30px;")

        self.label_ip = QLabel("IP del host:")
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("ej. 192.168.1.5")
        self.input_ip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: red; font-size: 25px;")
        self.label_error.setAlignment(Qt.AlignCenter)

        self.boton = QPushButton("Conectar  ▶")

        # ── Botones de navegación ─────────────────────────────────────────────
        self.pushButton_Volver = QPushButton("←")
        self.pushButton_Volver.setFixedSize(64, 64)
        self.pushButton_VolverInicio = QPushButton("🏠")
        self.pushButton_VolverInicio.setFixedSize(64, 64)

        # ── Layout ────────────────────────────────────────────────────────────
        layout.setSpacing(12)
        layout.setColumnStretch(0, 1)
        layout.setRowStretch(0, 1)

        row = 1
        layout.addWidget(self.pushButton_Volver,       row, 1, 1, 1)
        layout.addWidget(self.pushButton_VolverInicio, row, 2, 1, 1)
        layout.addWidget(self.label_titulo,            row, 3, 1, 2)

        row += 1
        layout.addWidget(self.label_puerto,            row, 3, 1, 1)
        layout.addWidget(self.input_puerto,            row, 4, 1, 1)

        row += 1
        layout.addWidget(self.separador,               row, 3, 1, 2)

        row += 1
        layout.addWidget(self.label_host_titulo,       row, 3, 1, 2)

        row += 1
        layout.addWidget(self.label_tu_ip,             row, 3, 1, 1)
        layout.addWidget(self.label_ip_valor,          row, 4, 1, 1)

        row += 1
        layout.addWidget(self.label_info_host,         row, 3, 1, 2)

        row += 1
        layout.addWidget(self.pushButton_Host,         row, 3, 1, 2)

        row += 1
        layout.addWidget(self.separador2,              row, 3, 1, 2)

        row += 1
        layout.addWidget(self.label_cliente_titulo,    row, 3, 1, 2)

        row += 1
        layout.addWidget(self.label_ip,                row, 3, 1, 1)
        layout.addWidget(self.input_ip,                row, 4, 1, 1)

        row += 1
        layout.addWidget(self.label_error,             row, 3, 1, 2)

        row += 1
        layout.addWidget(self.boton,                   row, 3, 1, 2)

        layout.setColumnStretch(10, 1)
        layout.setRowStretch(row + 1, 1)

        # ── Estilo ────────────────────────────────────────────────────────────
        self.setStyleSheet(f"""
            QWidget {{
                background-color: black;
            }}
            QLabel {{
                color: yellow;
                font-family: '{fuente_nombre()}';
                font-size: 40px;
            }}
            QLineEdit {{
                background-color: #222;
                color: yellow;
                border: 1px solid yellow;
                height: 64px;
                font-family: '{fuente_nombre()}';
                font-size: 40px;
            }}
            QPushButton {{
                background-color: black;
                color: yellow;
                border: 1px solid yellow;
                height: 64px;
                font-family: '{fuente_nombre()}';
                font-size: 40px;
            }}
            QPushButton:hover {{
                background-color: #333;
                height: 64px;
            }}
        """)

        self.setLayout(layout)

        # ── Conexiones ────────────────────────────────────────────────────────
        self.boton.clicked.connect(self._emit_conectar)
        self.pushButton_Host.clicked.connect(self._emit_hostear)
        self.pushButton_Volver.clicked.connect(lambda: self.signalVolver.emit())
        self.pushButton_VolverInicio.clicked.connect(lambda: self.signalVolverInicio.emit())

        # Actualiza la info de host en tiempo real cuando cambia el puerto
        self.input_puerto.textChanged.connect(self._actualizar_info_host)
        self._actualizar_info_host()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_puerto(self) -> int | None:
        """Devuelve el puerto como int o None si es inválido."""
        texto = self.input_puerto.text().strip() or "25565"
        try:
            p = int(texto)
            if 1024 <= p <= 65535:
                return p
        except ValueError:
            pass
        return None

    def _actualizar_info_host(self):
        """Muestra si el puerto está libre o no."""
        puerto = self._get_puerto()
        if puerto is None:
            self.label_info_host.setText("Puerto inválido (usa 1024–65535)")
            self.label_info_host.setStyleSheet("color: red; font-size: 25px;")
            return

        if is_port_available(puerto):
            self.label_info_host.setText(f"Puerto {puerto} disponible ✓")
            self.label_info_host.setStyleSheet("color: #00cc66; font-size: 25px;")
        else:
            self.label_info_host.setText(f"Puerto {puerto} ocupado — elige otro")
            self.label_info_host.setStyleSheet("color: orange; font-size: 25px;")

    # ── Emisores de señales ───────────────────────────────────────────────────

    def _emit_conectar(self):
        self.label_error.setText("")
        ip = self.input_ip.text().strip()
        if not ip:
            self.label_error.setText("Escribe la IP del host")
            return

        puerto = self._get_puerto()
        if puerto is None:
            self.label_error.setText("Puerto inválido (usa 1024–65535)")
            return

        self.signalAjustesRed.emit(ip, str(puerto))

    def _emit_hostear(self):
        self.label_error.setText("")
        puerto = self._get_puerto()
        if puerto is None:
            self.label_error.setText("Puerto inválido (usa 1024–65535)")
            return

        if not is_port_available(puerto):
            self.label_error.setText(f"Puerto {puerto} ocupado — elige otro")
            return

        # Actualiza el label para que se vea bien qué IP+puerto compartir
        ip_local = get_local_ip()
        self.label_ip_valor.setText(ip_local)
        self.label_info_host.setText(
            f"Esperando en {ip_local}:{puerto}…"
        )
        self.label_info_host.setStyleSheet("color: cyan; font-size: 25px;")

        self.signalHostear.emit(str(puerto))


if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventanared()
    ventana.show()
    app.exec()