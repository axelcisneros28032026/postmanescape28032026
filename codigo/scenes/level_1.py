import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QApplication, QGraphicsPixmapItem, \
    QHBoxLayout, QLabel, QPushButton

from config import fuente_nombre

from src.config.rutas import *

class Level1(QWidget):

    signalVolver = Signal()
    signalVolverInicio = Signal()

    def __init__(self):
        super().__init__()

        # Definición de componentes
        self.layout = QGridLayout()
        self.layout_2 = QHBoxLayout()

        # Visualización de puntuaciones altas
        self.player_points = 1000
        self.players_top = 10000
        self.player2_points = 1000

        self.label = QLabel(f"I - {self.player_points}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(f"Top - {self.players_top}")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(f"II - {self.player2_points}")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.escenaAncho = 1280
        self.escenaAlto = 720
        self.escena = QGraphicsScene(0, 0, self.escenaAncho, self.escenaAlto)
        self.vista = QGraphicsView(self.escena)

        self.block1_n = 6 # Número de plataformas (Par)

        self.pushButton_Volver = QPushButton("←")
        self.pushButton_Volver.setFixedSize(64, 64)
        self.pushButton_VolverInicio = QPushButton("🏠")
        self.pushButton_VolverInicio.setFixedSize(64, 64)

        self.enemy = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_IMAGES, "sprites", "enemy", "standard",
                                                              "idle", "left", "1.png")))
        self.victim = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_IMAGES, "sprites", "victim", "standard",
                                                               "idle", "left", "1.png")))
        self.player = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_IMAGES, "sprites", "player", "standard",
                                                               "idle", "right", "1.png")))

        # Edición de componentes
        self.escena.setBackgroundBrush(QColor("black"))

        #   Agregar plataformas
        for i in range(self.block1_n):
            n = self.block1_n
            n += 1

            self.plataforma = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_TILES, "1A.png")))
            self.plataforma_ancho = int((self.escenaAncho / 2) - self.plataforma.pixmap().width() / 2)

            self.escalera = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_TILES, "2.png")))

            if i == 0:
                self.plataforma.setPos(self.plataforma_ancho, int(self.escenaAlto / n * 2 - self.plataforma.pixmap().height()))

                self.enemy.setPos(self.plataforma.pos().x(), int(self.plataforma.pos().y() - 16))

                self.victim.setPos(int(self.plataforma.pos().x() + 64), int(self.plataforma.pos().y() - 16))
                self.escena.addItem(self.enemy)
                self.escena.addItem(self.victim)
            elif i < (n):
                self.plataforma.setPos(self.plataforma_ancho, int(self.plataforma_ultPosicion +
                                                                  self.plataforma.pixmap().height()) + 16)
                if i == (n-2):
                    self.player.setPos(self.plataforma.pos().x(), int(self.plataforma.pos().y() - 16))
                    self.escena.addItem(self.player)
                if i % 2 == 0:
                    self.escalera.setPos(self.plataforma.pos().x(), int(self.plataforma.pos().y() - 16))
                    self.escena.addItem(self.escalera)
                else:
                    self.escalera.setPos(int(self.plataforma.pos().x() + self.plataforma.pixmap().width() -
                                             self.escalera.pixmap().width()), int(self.plataforma.pos().y() - 16))
                    self.escena.addItem(self.escalera)

                print(self.escalera.pos())
                print (f"I - 1 = {i - 1}")
            else:
                print("xd")

            for i in range(5):
                self.coin = QGraphicsPixmapItem(QPixmap(os.path.join(DIR_IMAGES, "sprites", "coin", "1.png")))
                self.coin.setPos(int(self.plataforma.pos().x() * 2 + (64 * i * 3)), int(self.plataforma.pos().y() - 16))
                self.escena.addItem(self.coin)

            self.escena.addItem(self.plataforma)
            self.plataforma_ultPosicion = self.plataforma.pos().y()

        self.vista.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vista.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setColumnStretch(0, 1)
        self.layout.setSpacing(25)
        self.layout.setRowStretch(0, 1)
        self.layout.addLayout(self.layout_2, 1, 1, 1, 1)
        self.layout.addWidget(self.vista, 2, 1, 1, 1)
        self.layout.setColumnStretch(10, 1)
        self.layout.setRowStretch(10, 1)

        self.layout_2.addWidget(self.pushButton_Volver)
        self.layout_2.addWidget(self.pushButton_VolverInicio)
        self.layout_2.addWidget(self.label)
        self.layout_2.addWidget(self.label_2)
        self.layout_2.addWidget(self.label_3)

        # Disposición del widget
        self.setLayout(self.layout)
        self.setMinimumSize(int(self.escena.width()), int(self.escena.height()))
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

        # Eventos y Métodos
        self.pushButton_Volver.clicked.connect(lambda: self.signalVolver.emit())
        self.pushButton_VolverInicio.clicked.connect(lambda: self.signalVolverInicio.emit())

# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Level1()
    window.show()
    app.exec()