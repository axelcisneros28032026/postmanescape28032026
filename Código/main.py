"""
Integrantes:
24410663 Axel Rodrigo Cisneros Cano
24410206 Estrella Rodríguez Camacho
24410215 Karen Tatiana Romero Ramírez
"""


# Importaciones
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QAction, Qt, QPixmap, QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QStatusBar, QMenu, \
    QMenuBar, QMessageBox, QDialog, QVBoxLayout, QFrame, QSizePolicy, QStackedWidget

from config import fuente, fuente_nombre
from src.audio.sound import Sound
from src.components.navigationMenu import NavigationMenu
from src.config.rutas import *
from src.scenes.names_input import VentanaRegistro
from src.scenes.red_config import Ventanared

#   Nombres
APP_NOMBRE = "Postman Escape"
APP_NOMBRE_2 = ("Postman\n"
              "Escape")


# [A] Gestor de ventanas
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Disposición de ventana
        self.setWindowTitle(f"{APP_NOMBRE}")
        self.setWindowIcon(QIcon(APP_ICON))
        self.setGeometry(320, 180, 1280, 720)
        self.setContentsMargins(0, 0, 0, 0)

        # Definición de componentes
        self.action_1A = QAction(self)
        self.action_3A = QAction(self)
        self.action_3B = QAction(self)
        self.action_4A = QAction(self)
        self.action_4B = QAction(self)
        self.label_A1 = QLabel()
        self.label_A2 = QLabel()
        self.layout_A1 = QGridLayout()
        self.navigation_menu = NavigationMenu(
            ["Jugar", "Configuración", "Salir"],
            "*",
            0,
            f"color: magenta; qproperty-alignment: AlignCenter;",
            f"{fuente_nombre()}",
            50,
            "color: orange; border: none; text-align: center;",
            f"{fuente_nombre()}",
            50,
            True,
            15
        )
        self.menu_1 = QMenu("Archivo", self)
        self.menu_2 = QMenu("Editar", self)
        self.menu_3 = QMenu("Configuración", self)
        self.menu_4 = QMenu("Ayuda", self)
        self.menu_bar = QMenuBar()
        self.stacked_widget = QStackedWidget()
        self.stacked_widget_A1_page_1 = QWidget()
        self.status_bar = QStatusBar(self)
        self.widget_A = QWidget()
        self.widget_B = QWidget()

        # Edición de componentes
        # [A] Pantalla inicial
        #   Texto de título central
        self.label_A1.setAlignment(Qt.AlignCenter)
        self.label_A1.setFont(QFont(fuente(100)))
        self.label_A1.setText(f"{APP_NOMBRE_2}")
        self.label_A1.setStyleSheet("color: rgb(0, 64, 255); qproperty-alignment: AlignCenter;")

        #   Texto de créditos
        self.label_A2.setText("©2026 Canito's Co., Ltd.\n"
                               "Desde México")
        self.label_A2.setAlignment(Qt.AlignCenter)
        self.label_A2.setFont(QFont(fuente(40)))
        self.label_A2.setStyleSheet("color: white; qproperty-alignment: AlignCenter;")

        # Disposición de la pantalla inicial
        self.layout_A1.setContentsMargins(25, 25, 25, 25)
        self.layout_A1.setSpacing(15)
        self.layout_A1.setColumnStretch(0, 1)
        self.layout_A1.setRowStretch(0, 1)
        self.layout_A1.addWidget(self.label_A1, 1, 1, 1, 1)
        self.layout_A1.addWidget(self.navigation_menu, 2, 1, 1, 1)
        self.layout_A1.addWidget(self.label_A2, 3, 1, 1, 1)
        self.layout_A1.setColumnStretch(2, 1)
        self.layout_A1.setRowStretch(4, 1)

        self.widget_A.setLayout(self.layout_A1)

        # [B] Parte inicial para jugar
        # [BA] Pantalla para solicitud de nombres
        self.widget_B = VentanaRegistro()
        # [BB] Pantalla para configuración de conexión en red
        self.widget_BB = Ventanared()
        # [C] Pantalla de nivel
        self.widget_C = QWidget()

        # [-] Gestión de pantallas
        #   Menú principal
        #       Acciones
        self.action_1A.setText("Salir")
        self.action_1A.triggered.connect(self.exit_app)

        self.action_3A.setText("Pantalla completa")
        self.action_3A.setCheckable(True)
        self.action_3A.setChecked(False)
        self.action_3A.toggled.connect(self.toggle_fullscreen)

        self.action_3B.setText("Ver menú")
        self.action_3B.setCheckable(True)
        self.action_3B.setChecked(True)
        self.action_3B.toggled.connect(lambda state: self.menu_bar.setVisible(state))

        self.action_4A.setText(f"Ayuda de {APP_NOMBRE}")
        self.action_4A.triggered.connect(self.show_help_dialog)

        self.action_4B.setText(f"Acerca de {APP_NOMBRE}")
        self.action_4B.triggered.connect(self.show_about_dialog)

        #       Menús
        self.menu_1.addAction(self.action_1A)
        self.menu_3.addAction(self.action_3A)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_3B)
        self.menu_4.addAction(self.action_4A)
        self.menu_4.addAction(self.action_4B)

        #       Disposición
        self.menu_bar.addMenu(self.menu_1)
        self.menu_bar.addMenu(self.menu_2)
        self.menu_bar.addMenu(self.menu_3)
        self.menu_bar.addMenu(self.menu_4)

        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: black;
                color: white;
                border: 1px solid magenta;
            }
            QMenuBar::item:selected {
                background-color: magenta;
                color: white;
            }
            """)

        #   Barra de estado
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setStyleSheet("""background-color: black;""")

        # Disposición de pantallas
        self.stacked_widget.addWidget(self.widget_A)
        self.stacked_widget.addWidget(self.widget_B)
        self.stacked_widget.addWidget(self.widget_BB)
        self.stacked_widget.setStyleSheet("""background-color: black;""")
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)
        self.setCentralWidget(self.stacked_widget)

    # Eventos y Métodos
        self.navigation_menu.signalOpcionElegida.connect(self.navigation_menu_options)
        self.navigation_menu.signalOpcionElegida.connect(lambda: sound.click_button())
        self.widget_B.signalRegistro.connect(self.register_players)
        self.widget_B.signalRegistro.connect(lambda: sound.click_button())
        self.widget_B.signalVolver.connect(lambda: self.stacked_widget.setCurrentWidget(self.widget_A))
        self.widget_B.signalVolver.connect(lambda: sound.click_button())
        self.widget_BB.signalAjustesRed.connect(self.network_settings)
        self.widget_BB.signalAjustesRed.connect(lambda: sound.click_button())
        self.widget_BB.signalHostear.connect(self.host_game)
        self.widget_BB.signalHostear.connect(lambda: sound.click_button())
        self.widget_BB.signalVolver.connect(lambda: self.stacked_widget.setCurrentWidget(self.widget_B))
        self.widget_BB.signalVolver.connect(lambda: sound.click_button())
        self.widget_BB.signalVolverInicio.connect(lambda: self.stacked_widget.setCurrentWidget(self.widget_A))
        self.widget_BB.signalVolverInicio.connect(lambda: sound.click_button())

    def network_settings(self, ip, port):
        try:
            port = int(port)
        except ValueError:
            self.status_bar.showMessage("Puerto inválido")
            return

        self.ip = ip
        self.port = port
        self.status_bar.showMessage(
            f"Conectando a {ip}:{port}…"
        )

        QTimer.singleShot(
            500,
            lambda: self.start_game(
                rol="player",
                host=False,
                ip=ip,
                port=int(port)
            )
        )

    def host_game(self, port):
        self.ip = "127.0.0.1"
        self.port = int(port)
        self.status_bar.showMessage(f"Esperando jugador en puerto {port}…")
        self.start_game(
            rol="enemy",
            host=True,
            ip=self.ip,
            port=self.port
        )

    def _on_net_ready(self):
        self._net_ready = True
        self.timer.start(self.frequency)
        self._net_send_timer.start()
        print(f"[Red] Conexión lista. Rol: {self.rol}")

    def start_game(self, rol="player", host=False, ip="127.0.0.1", port=25565, round=1, prev_points=0,
                   prev_enemy_points=0):

        # Elegir nivel según ronda
        if round >= 3:
            from src.scenes.level2 import Level2 as LevelClass
        else:
            from src.scenes.level1 import Level1 as LevelClass

        if hasattr(self, "widget_C") and self.widget_C is not None:
            if hasattr(self.widget_C, "_server"):
                self.widget_C._server.stop()
            if hasattr(self.widget_C, "_client"):
                self.widget_C._client.stop()
            self.stacked_widget.removeWidget(self.widget_C)
            self.widget_C.deleteLater()

        self.widget_C = LevelClass(
            rol=rol, host=host, ip=ip, port=port,
            round=round, prev_points=prev_points,
            prev_enemy_points=prev_enemy_points
        )

        self.widget_C.setContentsMargins(0, 0, 0, 0)
        self.widget_C.signal_back.connect(
            lambda: self.stacked_widget.setCurrentWidget(
                self.widget_BB
            )
        )
        self.widget_C.signal_back_init.connect(
            lambda: self.stacked_widget.setCurrentWidget(
                self.widget_A
            )
        )

        self.widget_C.signal_next_level.connect(
            lambda: self.start_game(
                rol=self.widget_C._next_rol,
                host=hasattr(self.widget_C, "_server"),
                ip=self.ip,
                port=self.port,
                round=self.widget_C.round,
                prev_points=self.widget_C.player_points,
                prev_enemy_points=self.widget_C.enemy_points,
            )
        )

        if host:
            self.widget_C._server.client_connected.connect(
                lambda: self.status_bar.showMessage(
                    "Jugador conectado ✓"
                )
            )
        else:
            self.widget_C._client.connected.connect(
                lambda: self.status_bar.showMessage(
                    f"Conectado a {ip}:{port} ✓"
                )
            )
            self.widget_C._client.connection_failed.connect(
                lambda err: self.status_bar.showMessage(
                    f"Error de conexión: {err}"
                )
            )

        self.stacked_widget.addWidget(self.widget_C)
        self.stacked_widget.setCurrentWidget(self.widget_C)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.menu_bar.setVisible(True)
            self.action_3B.setChecked(True)
        if event.key() == Qt.Key.Key_F11:
            self.action_3A.toggle()
        else:
            super().keyPressEvent(event)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def read_ping(self):
        self.ping = 5
        print(self.ping)
        if self.ping >= 0 and self.ping <= 15:
            self.network_status = "Excelente"
        if self.ping >= 15 and self.ping <= 45:
            self.network_status = "Bueno"
        if self.ping >= 45 and self.ping <= 100:
            self.network_status = "Aceptable"
        if self.ping >= 100 and self.ping <= 250:
            self.network_status = "Acércate (al router)"
        if self.ping >= 250:
            self.network_status = "Desconéctate"
        return self.network_status

    # Sección "Ayuda"
    def show_help_dialog(self):
        self.dialog = QDialog(self)

        self.dialog.setWindowTitle(f"Ayuda de {APP_NOMBRE}")
        self.dialog.setWindowFlags(
            Qt.Window
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        self.dialog.setWindowModality(Qt.NonModal)

        self.pixmap = QPixmap(APP_ICON_PNG).scaled(
            64, 64,
            Qt.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        self.label_1 = QLabel()
        self.label_1.setPixmap(QPixmap(self.pixmap))
        self.label_1.setScaledContents(False)
        self.label_2 = QLabel(f"<b>{APP_NOMBRE}</b> > Ayuda")
        self.label_3 = QLabel(
            "<b>Navegación</b>"
            "<br><br>"
            "(↑) <b>Flecha arriba</b>. Mover hacia arriba."
            "<br><br>"
            "(↓) <b>Flecha abajo</b>. Mover hacia abajo."
            "<br><br>"
            "(↵) <b>Enter</b>. Seleccionar opción."
            "<br><br>"
            "(E) <b>PowerUp 1</b>"
            "<br><br>"
            "(R) <b>PowerUp 2</b>"
            "<br><br>"
            "(Ctrl) <b>PowerUp 3</b>"
        )
        self.label_4 = QLabel(f"<b>Atajos del teclado</b>"
                              f"<br><br>"
                              f"[<b>Esc</b>] Ver menú."
                              f"<br><br>"
                              f"[<b>F11</b>] Pantalla completa."
                              )

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.separator_2 = QFrame()
        self.separator_2.setFrameShape(QFrame.HLine)

        self.separator_3 = QFrame()
        self.separator_3.setFrameShape(QFrame.HLine)

        self.layout = QGridLayout()
        self.layout_A = QVBoxLayout()
        self.layout_B = QGridLayout()

        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.addLayout(self.layout_A, 1, 1, 2, 1)
        self.layout.addLayout(self.layout_B, 1, 2, 1, 1)
        self.layout.setColumnStretch(3, 1)
        self.layout.setRowStretch(2, 1)

        self.layout_A.addWidget(self.label_1)
        self.layout_A.addStretch(1)

        self.layout_B.addWidget(self.separator, 0, 0, 5, 1)
        self.layout_B.addWidget(self.label_2, 0, 1, 1, 1)
        self.layout_B.addWidget(self.separator_2, 1, 1, 1, 1)
        self.layout_B.addWidget(self.label_3, 2, 1, 1, 1)
        self.layout_B.addWidget(self.separator_3, 3, 1, 1, 1)
        self.layout_B.addWidget(self.label_4, 4, 1, 1, 1)
        self.layout_B.setColumnStretch(5, 1)

        self.dialog.setLayout(self.layout)

        self.dialog.setStyleSheet("""color: black;""")
        self.dialog.show()

    # Sección "Acerca de"
    def show_about_dialog(self):
        message_box = QMessageBox()

        message_box.setWindowTitle(f"Acerca de {APP_NOMBRE}")
        message_box.setWindowIcon(QIcon(APP_ICON))
        message_box.setText(
            f"<b>{APP_NOMBRE}</b>"
            f"<br><br>"
            f"{APP_NOMBRE} es un videojuego de plataformas basado en Donkey Kong (1981), el clásico arcade de Nintendo "
            f"desarrollado por Shigeru Miyamoto."
            f"<br><br>"
            f"Desarrollado por Axel C., Estrella R. y Karen R."
        )
        message_box.setStyleSheet("""color: black;""")

        pixmap = QPixmap(APP_ICON_PNG)
        pixmap = pixmap.scaled(
            64, 64,
            Qt.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        message_box.setIconPixmap(pixmap)
        message_box.setStandardButtons(QMessageBox.Ok)

        message_box.exec()

    def navigation_menu_options(self, index):
        if index == 0:
            self.stacked_widget.setCurrentWidget(self.widget_B)
        elif index == 1:
            self.stacked_widget.setCurrentWidget(self.widget_config)
        elif index == 2:
            self.exit_app()

    def register_players(self, p1):
        self.p1 = p1
        print("Registro:")
        print(f"Jugador 1: {p1}")
        self.stacked_widget.setCurrentWidget(self.widget_BB)

    def exit_app(self):
        sys.exit()

# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apariencia
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    app.setPalette(palette)

    # Música
    audio = Sound()
    audio.background()
    sound = Sound()

    # Ventana
    window = MainWindow()
    window.audio = audio
    window.show()
    app.exec()