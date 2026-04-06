"""
Integrantes:
24410663 Axel Rodrigo Cisneros Cano
24410206 Estrella Rodríguez Camacho
24410215 Karen Tatiana Romero Ramírez
"""
import os
# Importaciones
import sys

from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QFont, QIcon, QAction, Qt, QPixmap, QPalette, QColor
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QStatusBar, QMenu, \
    QMenuBar, QMessageBox, QDialog, QVBoxLayout, QFrame, QSizePolicy, QStackedWidget

from config import fuente, fuente_nombre
from scenes.configuracion_red import Ventanared
from scenes.solicitud_nombres import VentanaRegistro
from src.components.navigationMenu import NavigationMenu
from src.config.rutas import *

# Constantes globales
#   Nombres
APP_NOMBRE = "Postman Escape"
APP_NOMBRE_2 = ("Postman\n"
              "Escape")

#   Audio
player = QMediaPlayer()
audio_output = QAudioOutput()
player.setAudioOutput(audio_output)

player.setSource(QUrl.fromLocalFile(os.path.join(DIR_BASE, "assets", "music", "background.mp3")))
audio_output.setVolume(0.1)
player.play()

# [A] Gestor de ventanas
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Disposición de ventana
        self.setWindowTitle(f"{APP_NOMBRE}")
        self.setWindowIcon(QIcon(os.path.join(APP_ICON)))
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
        self.navigationMenu = NavigationMenu(
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
        self.menuBar = QMenuBar()
        self.stackedWidget = QStackedWidget()
        self.stackedWidget_A1_page_1 = QWidget()
        self.statusBar = QStatusBar(self)
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
        self.layout_A1.addWidget(self.navigationMenu, 2, 1, 1, 1)
        self.layout_A1.addWidget(self.label_A2, 3, 1, 1, 1)
        self.layout_A1.setColumnStretch(2, 1)
        self.layout_A1.setRowStretch(4, 1)

        self.widget_A.setLayout(self.layout_A1)

        # [B] Parte inicial para jugar
        # [BA] Pantalla para solicitud de nombres
        self.widget_B = VentanaRegistro()
        # [BB] Pantalla para configuración de conexión en red
        self.widget_BB = Ventanared()
        # [C] Pantalla estática
        self.widget_C = QWidget()

        # [-] Gestión de pantallas
        #   Menú principal
        #       Acciones
        self.action_1A.setText("Salir")
        self.action_1A.triggered.connect(self.salir)

        self.action_3A.setText("Pantalla completa")
        self.action_3A.setCheckable(True)
        self.action_3A.setChecked(False)
        self.action_3A.toggled.connect(self.verPantallaCompleta)

        self.action_3B.setText("Ver menú")
        self.action_3B.setCheckable(True)
        self.action_3B.setChecked(True)
        self.action_3B.toggled.connect(lambda estado: self.menuBar.setVisible(estado))

        self.action_4A.setText(f"Ayuda de {APP_NOMBRE}")
        self.action_4A.triggered.connect(self.metodo_action_4A)

        self.action_4B.setText(f"Acerca de {APP_NOMBRE}")
        self.action_4B.triggered.connect(self.metodo_action_4B)

        #       Menús
        self.menu_1.addAction(self.action_1A)
        self.menu_3.addAction(self.action_3A)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_3B)
        self.menu_4.addAction(self.action_4A)
        self.menu_4.addAction(self.action_4B)

        #       Disposición
        self.menuBar.addMenu(self.menu_1)
        self.menuBar.addMenu(self.menu_2)
        self.menuBar.addMenu(self.menu_3)
        self.menuBar.addMenu(self.menu_4)

        self.menuBar.setStyleSheet("""
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
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setStyleSheet("""background-color: black;""")

        # Disposición de pantallas
        self.stackedWidget.addWidget(self.widget_A)
        self.stackedWidget.addWidget(self.widget_B)
        self.stackedWidget.addWidget(self.widget_BB)
        self.stackedWidget.setStyleSheet("""background-color: black;""")
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.setMenuBar(self.menuBar)
        self.setStatusBar(self.statusBar)
        self.setCentralWidget(self.stackedWidget)

        # self.iniciarJuego()
    # Eventos y Métodos
        self.navigationMenu.signalOpcionElegida.connect(self.navigationMenuOptions)
        self.widget_B.signalRegistro.connect(self.registroJugadores)
        self.widget_B.signalVolver.connect(lambda: self.stackedWidget.setCurrentWidget(self.widget_A))
        self.widget_BB.signalAjustesRed.connect(self.ajustesRed)
        self.widget_BB.signalVolver.connect(lambda: self.stackedWidget.setCurrentWidget(self.widget_B))
        self.widget_BB.signalVolverInicio.connect(lambda: self.stackedWidget.setCurrentWidget(self.widget_A))

    def ajustesRed(self, ip, port):
        self.ip = ip
        self.port = port
        self.statusBar.showMessage(f"Conectando a {ip}:{port}")
        QTimer.singleShot(1000, lambda: self.statusBar.showMessage(f"Conectado a {ip}:{port}"))
        QTimer.singleShot(2000, lambda: self.statusBar.showMessage(f"Ping: {self.leerPing()}"))
        QTimer.singleShot(2500, self.iniciarJuego)

    def iniciarJuego(self):
        from scenes.level_1 import Level1
        self.widget_C = Level1()
        self.widget_C.setContentsMargins(0, 0, 0, 0)
        self.widget_C.signalVolver.connect(lambda: self.stackedWidget.setCurrentWidget(self.widget_BB))
        self.widget_C.signalVolverInicio.connect(lambda: self.stackedWidget.setCurrentWidget(self.widget_A))

        self.stackedWidget.addWidget(self.widget_C)
        self.stackedWidget.setCurrentWidget(self.widget_C)
        print("xd")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.menuBar.setVisible(True)
            self.action_3B.setChecked(True)
        if event.key() == Qt.Key.Key_F11:
            self.action_3A.toggle()
        else:
            super().keyPressEvent(event)

    def verPantallaCompleta(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def leerPing(self):
# TODO: METODO SIMULADO FALTA COMPLETAR ================================================================================
        self.ping = 5
        print(self.ping)
        if self.ping >= 0 and self.ping <= 15:
            self.estadoRed = "Excelente"
        if self.ping >= 15 and self.ping <= 45:
            self.estadoRed = "Bueno"
        if self.ping >= 45 and self.ping <= 100:
            self.estadoRed = "Aceptable"
        if self.ping >= 100 and self.ping <= 250:
            self.estadoRed = "Acércate (al router)"
        if self.ping >= 250:
            self.estadoRed = "Desconéctate"
        return self.estadoRed

    # Sección "Ayuda"
    def metodo_action_4A(self):
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

        self.label_3 = QLabel(f"<b>Navegación</b>"
                              f"<br><br>"
                              f"(↑) <b>Flecha arriba</b>. Mover hacia arriba"
                              f"<br><br>"
                              f"(↓) <b>Flecha abajo</b>. Mover hacia abajo"
                              f"<br><br>"
                              f"(↵) <b>Enter</b>. Seleccionar opción"
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
    def metodo_action_4B(self):
        messageBox = QMessageBox()

        messageBox.setWindowTitle(f"Acerca de {APP_NOMBRE}")
        messageBox.setWindowIcon(QIcon(APP_ICON))
        messageBox.setText(
            f"<b>{APP_NOMBRE}</b>"
            f"<br><br>"
            f"{APP_NOMBRE} es un videojuego de plataformas basado en Donkey Kong (1981), el clásico arcade de Nintendo "
            f"desarrollado por Shigeru Miyamoto."
            f"<br><br>"
            f"Desarrollado por Axel C., Estrella R. y Karen R."
        )
        messageBox.setStyleSheet("""color: black;""")

        pixmap = QPixmap(APP_ICON_PNG)
        pixmap = pixmap.scaled(
            64, 64,
            Qt.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        messageBox.setIconPixmap(pixmap)
        messageBox.setStandardButtons(QMessageBox.Ok)

        messageBox.exec()

    def navigationMenuOptions(self, indice):
        if indice == 0:
            self.stackedWidget.setCurrentWidget(self.widget_B)
            print(f"[Alerta] Falta el método de la opción {indice}")
        elif indice == 1:
            #self.stackedWidget.setCurrentIndex(self.widget_C)
            print(f"[Alerta] Falta el método de la opción {indice}")
        elif indice == 2:
            self.salir()

    def registroJugadores(self, j1):
        self.j1 = j1
        print("Registro:")
        print(f"Jugador 1: {j1}")
        self.stackedWidget.setCurrentWidget(self.widget_BB)

    def salir(self):
        # TODO: FALTA CERRAR DE FORMA SEGURA (GUARDAR/DESCARTAR CAMBIOS) ===============================================
        sys.exit()

# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = app.palette()
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    app.exec()
