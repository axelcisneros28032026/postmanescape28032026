# ======================================================================================================================
# Importaciones
import sys

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QPen, QPolygonF
from PySide6.QtWidgets import (QWidget, QApplication, QLabel, QPushButton, QGraphicsScene, QGraphicsView,
                               QGraphicsPixmapItem, QGraphicsPolygonItem, QGridLayout, QHBoxLayout, QVBoxLayout)

from config import fuente_nombre
from src.audio.sound import Sound
from src.entities.NPC.victim.victim1 import Victim
from src.entities.blocks.ladders import Ladders
from src.entities.blocks.plataforms import Platforms
from src.entities.enemy.enemy1 import Enemy
from src.entities.items.coins import Coins
from src.entities.player.player1 import Player

sound = Sound()
# ======================================================================================================================

# ======================================================================================================================
# Nivel 1
class Level1(QWidget):

    # Señales
    signal_back = Signal() # Señal para volver a la pantalla anterior
    signal_back_init = Signal() # Señal para volver a la pantalla inicial

    # Lógica inicial
    def __init__(self):
        super().__init__()

        # Definición de componentes
        self.layout = QGridLayout()
        self.layout_2 = QHBoxLayout()
        self.layout_2A = QGridLayout()
        self.layout_2A1 = QVBoxLayout()
        self.layout_2A2 = QVBoxLayout()

        self.pushButton_back = QPushButton("←")
        self.pushButton_back_init = QPushButton("🏠")

        # Otros:
        self.frequency = 8  # Frecuencia del hilo principal en milisegundos
        self.multiple_keys = set() # Conjunto de teclas presionadas
        self.iterator_show_collisions = 0 # Iterador auxiliar para el visor de colisiones
        self.show_collisions_toggle = False # Interruptor para mostrar colisiones

        # Rol de juego
        self.rol = "player" # Rol establecido en jugador
        #self.rol = "enemy" # Rol establecido en enemigo

        # ==============================================================================================================
        # Jugador
        self.player_anim_speed = 4 # Velocidad de animaciones
        self.player_life_initial = 10 # Vida inicial (unidades)
        self.player_life_current = self.player_life_initial # Vida actual

        # --------------------------------------------------------------------------------------------------------------
        # Daños
        self.player_damage_receiving_status = False # Estado de daño recibido
        self.player_damage_fall_accumulated = 0 # Daño acumulado por caída del jugador
        self.i_player_damage_fall_accumulated = 0 # Iterador auxiliar que contabiliza los píxeles que ha caído el jugador
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Potenciadores:
        # Aceleración
        self.player_run_initial = 5 # Tiempo de aceleración inicial
        self.player_run_current = self.player_run_initial # Tiempo de aceleración actual (segundos)
        self.player_run_cooldown = 8  # Tiempo de espera para reactivar la aceleración (segundos)
        self.player_run_counter = 0 # Contador de la aceleración
        self.player_run_status = False # Estado de aceleración
        self.player_run_toggle = False # Interruptor de aceleración
        self.player_run_lock = False # Bloqueo de aceleración
        self.player_run_timer = QTimer(timeout = self.power_up_run) # Contador de aceleración

        # Regeneración
        self.player_regeneration_initial = 3 # Tiempo de regeneración inicial (segundos)
        self.player_regeneration_current = self.player_regeneration_initial # Tiempo de regeneración actual
        self.player_regeneration_cooldown = 5 # Tiempo de espera para reactivar la regeneración (segundos)
        self.player_regeneration_counter = 0  # Contador de la regeneración
        self.player_regeneration_status = False # Estado de regeneración
        self.player_regeneration_lock = False # Bloqueo de regeneración
        self.player_regeneration_timer = QTimer(timeout = self.power_up_regeneration)  # Contador de regeneración

        # Inmunidad
        self.player_immunity_initial = 3  # Tiempo de inmunidad inicial (segundos)
        self.player_immunity_current = self.player_immunity_initial  # Tiempo de inmunidad actual
        self.player_immunity_cooldown = 5  # Tiempo de espera para reactivar la inmunidad (segundos)
        self.player_immunity_counter = 0 # Contador de la inmunidad
        self.player_immunity_status = False  # Estado de inmunidad
        self.player_immunity_lock = False  # Bloqueo de inmunidad
        self.player_immunity_timer = QTimer(timeout=self.power_up_immunity)  # Contador de inmunidad
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Movimiento
        self.player_speed = 3  # Velocidad del jugador

        #   Gravedad
        self.player_gravity_toggle = True # Interruptor de gravedad
        self.player_gravity_speed_initial = 5 # Velocidad de gravedad inicial
        self.player_gravity_speed = self.player_gravity_speed_initial # Velocidad de gravedad
        self.player_gravity_jump_speed_initial = self.player_gravity_speed_initial # Velocidad de la gravedad de salto inicial
        self.player_gravity_jump_speed = self.player_gravity_jump_speed_initial # Velocidad de la gravedad de salto

        #   Horizontal
        self.player_move_horizontal_lock = False # Bloqueo de movimiento horizontal general
        self.player_move_walk_left_lock = False # Bloqueo de movimiento horizontal a la izquierda
        self.player_move_walk_right_lock = False # Bloqueo de movimiento horizontal a la derecha

        self.player_move_walk_left = False # Movimiento horizontal a la izquierda
        self.player_move_walk_right = False # Movimiento horizontal a la derecha

        #   Saltar
        self.player_move_jump_lock = False # Bloqueo de salto general
        self.player_move_jump_up_lock = False # Bloqueo de salto vertical

        self.player_move_jump_up = False # Salto vertical
        self.player_move_jump_left = False # Salto vertical a la izquierda
        self.player_move_jump_right = False # Salto vertical a la derecha

        self.player_move_jump_last = None # Tipo último de salto

        #   Escalar
        self.player_move_climb_lock = True  # Bloqueo de escalado general
        self.player_move_climb_up_lock = True # Bloqueo de escalado hacia arriba
        self.player_move_climb_down_lock = False # Bloqueo de escalado hacia abajo

        self.player_move_climb_up = False # Escalado hacia arriba
        self.player_move_climb_down = False # Escalado hacia abajo

        #   Estados
        self.player_scaling_state = False # Estado de escalado
        self.player_jumping_state = False # Estado de salto

        # Colisiones
        self.player_coll_escalera = False # Estado de colisión con escalera
        self.player_coll_platform = False # Estado de colisión con platform
        # --------------------------------------------------------------------------------------------------------------
        # ==============================================================================================================

        # --------------------------------------------------------------------------------------------------------------
        # Temporizadores

        # Hilo principal
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(self.frequency)

        # Administrador de daño
        self.player_damage_timer = QTimer()
        self.player_damage_timer.setSingleShot(True)
        self.player_damage_timer.timeout.connect(self.damage_management_aux)
        # --------------------------------------------------------------------------------------------------------------

        # Puntuaciones altas
        self.player_points = 0 # Puntos del jugador
        self.players_top = 0 # Puntos top del rol actual
        self.enemy_points = 0 # Puntos del enemigo

        # Visualización de datos
        self.label = QLabel(f"I - {self.player_points}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(f"Top - {self.players_top}")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(f"II - {self.enemy_points}")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_life = QLabel(f"❤️ {self.player_life_current}")
        self.label_life.setAlignment(Qt.AlignLeft)
        self.label_regeneration = QLabel(f"️⚕️ {self.player_regeneration_current} s")
        self.label_regeneration.setAlignment(Qt.AlignLeft)
        self.label_immunity = QLabel(f"️🛡️ {self.player_immunity_current} s")
        self.label_immunity.setAlignment(Qt.AlignLeft)
        self.label_run = QLabel(f"️🏃 {self.player_run_current} s")
        self.label_run.setAlignment(Qt.AlignLeft)

        # Construcción de escena
        self.scene_width = 1280
        self.scene_height = 720
        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view = QGraphicsView(self.scene)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.block1_n = 6  # Número de platforms (Par)

        self.enemy = Enemy(speed = 5, anim_speed = int(1000 / self.frequency * 0.075))
        self.victim = Victim(speed = 5, anim_speed = int(1000 / self.frequency * 0.075))
        self.player = Player(speed = self.player_speed, anim_speed = int(1000 / self.frequency * 0.075))

        # Edición de componentes
        self.victim.setZValue(8)
        self.enemy.setZValue(9)
        self.player.setZValue(10)
        self.scene.setBackgroundBrush(QColor("black"))

        # Agregar platforms
        for i in range(self.block1_n):
            n = self.block1_n
            n += 1

            self.platform = Platforms()
            self.platform_y_tolerance = 8
            self.platform_y_tolerance = 2

            self.ladder = Ladders()

            if i == 0:
                self.platform.setPos(int((self.scene_width / 2) - self.platform.pixmap().width() / 2),
                                     int(self.scene_height / n * 2 - self.platform.pixmap().height()))
                self.platform_separation = self.platform.pixmap().height() + 16

                self.enemy.setPos(self.platform.pos().x(), int(self.platform.pos().y() - 16))

                self.victim.setPos(int(self.platform.pos().x() + 64), int(self.platform.pos().y() - 16))
            elif i < n:
                self.platform.setPos(int((self.scene_width / 2) - self.platform.pixmap().width() / 2),
                                     int(self.platform_last_position + self.platform_separation))
                if i == (n - 2):
                    self.player.setPos(self.platform.pos().x(), int(self.platform.pos().y() - 16)) # REMOVER EXCESO DE POSICION EN X

                if i % 2 == 0:
                    self.ladder.setPos(self.platform.pos().x(), int(self.platform.pos().y() - 16))
                    self.scene.addItem(self.ladder)
                else:
                    self.ladder.setPos(int(self.platform.pos().x() + self.platform.pixmap().width() -
                                           self.ladder.pixmap().width()), int(self.platform.pos().y() - 16))
                    self.scene.addItem(self.ladder)

            self.scene.addItem(self.victim)
            self.scene.addItem(self.player)
            self.scene.addItem(self.enemy)

            for i in range(5):
                self.coin = Coins()
                self.coin.setPos(int(self.platform.pos().x() * 2 + (64 * i * 3)), int(self.platform.pos().y() - 16))
                self.scene.addItem(self.coin)

            self.scene.addItem(self.platform)
            self.platform_last_position = self.platform.pos().y()

        self.view.setFocusPolicy(Qt.NoFocus)
        self.setFocusPolicy(Qt.StrongFocus)
        self.view.setInteractive(False)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Edición de componentes de ventana
        # Botones de retorno
        self.pushButton_back.setFixedSize(64, 64)
        self.pushButton_back_init.setFixedSize(64, 64)

        # Contenedor principal
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setColumnStretch(0, 1)
        self.layout.setSpacing(25)
        self.layout.setRowStretch(0, 1)
        self.layout.addLayout(self.layout_2, 1, 1, 1, 1)
        self.layout.addWidget(self.view, 2, 1, 1, 1)
        self.layout.setColumnStretch(10, 1)
        self.layout.setRowStretch(10, 1)

        # Contenedor 2 (Botones de retorno, estadísticas y datos)
        self.layout_2A1.addWidget(self.label_life)
        self.layout_2A1.addWidget(self.label_regeneration)
        self.layout_2A2.addWidget(self.label_immunity)
        self.layout_2A2.addWidget(self.label_run)
        self.layout_2A.addLayout(self.layout_2A1, 0, 0, 1, 1)
        self.layout_2A.addLayout(self.layout_2A2, 0, 1, 1, 1)
        self.layout_2.addWidget(self.pushButton_back)
        self.layout_2.addWidget(self.pushButton_back_init)
        self.layout_2.addWidget(self.label)
        self.layout_2.addWidget(self.label_2)
        self.layout_2.addWidget(self.label_3)
        self.layout_2.addLayout(self.layout_2A)

        # Disposición del widget
        self.setLayout(self.layout)
        self.setMinimumSize(int(self.scene.width()), int(self.scene.height()))
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

        # Eventos y señales
        self.pushButton_back.clicked.connect(lambda: self.signal_back.emit())
        self.pushButton_back.clicked.connect(lambda: sound.click_button())
        self.pushButton_back_init.clicked.connect(lambda: self.signal_back_init.emit())
        self.pushButton_back_init.clicked.connect(lambda: sound.click_button())