"""
Integrantes:
24410663 Axel Rodrigo Cisneros Cano
24410206 Estrella Rodríguez Camacho
24410215 Karen Tatiana Romero Ramírez
"""

import sys

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QFont, QIcon, QAction, QPixmap, QPalette, QColor
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout,
                               QStatusBar, QMenu, QMenuBar, QMessageBox, QDialog,
                               QVBoxLayout, QFrame, QSizePolicy, QStackedWidget)

from config import fuente, fuente_nombre
from src.audio.sound import Sound
from src.components.navigationMenu import NavigationMenu
from src.config.rutas import *

# Componentes y Escenas del Juego
from src.scenes.red_config import Ventanared
from src.scenes.names_input import VentanaRegistro
from src.scenes.level1 import Level1

# Gestor de Red asíncrono
from network_manager import NetworkManager

APP_NOMBRE = "Postman Escape"
APP_NOMBRE_2 = ("sepa\n"
                "Escape")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración Básica de la Ventana
        self.setWindowTitle(f"{APP_NOMBRE}")
        self.setWindowIcon(QIcon(APP_ICON))
        self.setGeometry(320, 180, 1280, 720)

        # Inicializar Administrador de Red (Control de Sockets en hilos)
        self.network_manager = NetworkManager()
        self.mi_rol_de_juego = "player"  # Por defecto actuar como jugador local

        # Contenedor Stacked Widget (Manejador de Pantallas del juego)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Instanciar las Pantallas
        self.widget_BB = VentanaRegistro()  # Registro de nombres (Pantalla Inicial)
        self.ventana_red = Ventanared()  # Configuración de Red IP/Puerto
        self.level1 = Level1()  # El mapa del juego real

        # Agregarlas al stacked_widget
        self.stacked_widget.addWidget(self.widget_BB)  # Índice 0
        self.stacked_widget.addWidget(self.ventana_red)  # Índice 1
        self.stacked_widget.addWidget(self.level1)  # Índice 2

        # Barra de Estado (Status Bar)
        self.statusBar().setStyleSheet("background-color: black; color: yellow;")
        self.statusBar().showMessage("Esperando registro de jugador...")

        # -----------------------------------------------------------------
        # CONEXIONES DE FLUJO Y NAVEGACIÓN
        # -----------------------------------------------------------------
        # Nombres -> Va a configuración de Red
        self.widget_BB.signalRegistro.connect(self.register_players)

        # Volver desde Configuración de Red -> Va a Registro de Nombres
        self.ventana_red.signalVolver.connect(self.ir_a_registro)

        # Conectar botones de la interfaz de red
        self.ventana_red.signalAjustesRed.connect(self.solicitar_conexion_cliente)
        self.ventana_red.boton_server.clicked.connect(self.solicitar_crear_servidor)

        # Escuchar las respuestas internas asíncronas del NetworkManager
        self.network_manager.connected.connect(self.on_network_connected)
        self.network_manager.disconnected.connect(self.on_network_disconnected)
        self.network_manager.message_received.connect(self.on_message_received)

    # ==========================================================
    # FLUJOS DE PANTALLA
    # ==========================================================
    def ir_a_registro(self):
        self.stacked_widget.setCurrentWidget(self.widget_BB)

    def register_players(self, p1):
        self.p1 = p1
        print("Registro Exitoso:")
        print(f"Jugador local: {p1}")
        self.statusBar().showMessage(f"Jugador: {p1} | Configura la conexión de red")
        self.stacked_widget.setCurrentWidget(self.ventana_red)

    # ==========================================================
    # PROCESAMIENTO DE SOCKETS (EVENTOS DE BOTÓN)
    # ==========================================================
    @Slot(str, str)
    def solicitar_conexion_cliente(self, ip, puerto):
        if not ip or not puerto:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor introduce una Dirección IP y un Puerto.")
            return

        print(f"[CLIENTE] Solicitando unirse a {ip}:{puerto}...")
        self.statusBar().showMessage(f"Conectando a {ip}:{puerto}...")
        try:
            self.mi_rol_de_juego = "player"  # Quien se conecta controla al personaje principal
            self.network_manager.start_client(ip, int(puerto))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo inicializar el Socket Cliente: {e}")

    @Slot()
    def solicitar_crear_servidor(self):
        puerto = self.ventana_red.input_puerto.text().strip()
        if not puerto:
            QMessageBox.warning(self, "Puerto Vacío", "Por favor introduce un Puerto válido.")
            return

        print(f"[SERVIDOR] Abriendo Socket en puerto local: {puerto}...")
        self.statusBar().showMessage(f"Servidor escuchando en puerto {puerto}...")
        try:
            self.mi_rol_de_juego = "server"  # El host actúa como el entorno del servidor
            self.network_manager.start_server(int(puerto))
            QMessageBox.information(self, "Servidor Creado",
                                    f"Servidor activo en el puerto {puerto}.\nEsperando al contrincante local...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el Servidor: {e}")

    # ==========================================================
    # CALLBACKS ASÍNCRONOS DE RED (SEÑALES RECIBIDAS DEL HILO)
    # ==========================================================
    def on_network_connected(self):
        print("[SISTEMA DE RED] Conexión establecida con éxito en ambos extremos.")
        self.statusBar().showMessage("¡Partida de red En Línea Local activa!")
        QMessageBox.information(self, "¡Conectado!", "¡El segundo jugador se ha unido con éxito!\nComienza el juego.")

        # Le inyectamos el rol asignado a la pantalla de juego antes de cambiarla
        self.level1.rol = self.mi_rol_de_juego
        print(f"[JUEGO] Rol configurado en el mapa: {self.level1.rol}")

        # Cambiamos la vista del StackedWidget hacia el Nivel 1 para iniciar la partida
        self.stacked_widget.setCurrentWidget(self.level1)

    def on_network_disconnected(self):
        print("[SISTEMA DE RED] Conexión cerrada.")
        self.statusBar().showMessage("Desconectado.")
        QMessageBox.warning(self, "Desconectado", "Se cerró o se perdió la comunicación con el otro jugador.")
        self.stacked_widget.setCurrentWidget(self.ventana_red)

    def on_message_received(self, mensaje):
        # Aquí procesarás los strings que envíe el cliente o servidor remoto
        print(f"[DATOS RED ENTRANTE]: {mensaje}")

    # ==========================================================
    # OTROS COMPONENTES
    # ==========================================================
    def custom_message_box(self, titulo, mensaje):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(titulo)
        message_box.setText(mensaje)
        message_box.setStyleSheet("QMessageBox { background-color: black; } QLabel { color: yellow; }")

        pixmap = QPixmap(APP_ICON_PNG)
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        message_box.setIconPixmap(pixmap)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def navigation_menu_options(self, index):
        if index == 0:
            print(f"[Navegación] Opción {index}")
        elif index == 2:
            self.exit_app()

    def exit_app(self):
        if hasattr(self, 'network_manager'):
            self.network_manager.close()
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())