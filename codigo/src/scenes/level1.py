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


# ======================================================================================================================
# Hilo principal
    def game_loop(self):
        self.player_gravity_speed = self.player_gravity_speed_initial

        self.player_speed = self.player.speed

        self.player_coll_escalera = None
        self.player_coll_platform = None
        self.player_move_horizontal_lock = False
        self.player_move_walk_left_lock = False
        self.player_move_walk_right_lock = False

        if not self.player_scaling_state:
            self.player_move_climb_lock = True
            self.player_move_climb_up_lock = True
            self.player_move_climb_down_lock = True

        if not self.player_scaling_state and not self.player_jumping_state:
            self.player_gravity_toggle = True

        # Rectángulo del jugador en coordenadas de escena
        player_rect = self.player.mapToScene(self.player.boundingRect()).boundingRect()

        self.player_x = player_rect.left()
        self.player_x2 = player_rect.right()
        self.player_y = player_rect.top()
        self.player_y2 = player_rect.bottom()


        # Rectángulo del enemigo en coordenadas de escena
        enemy_rect = self.enemy.mapToScene(self.enemy.boundingRect()).boundingRect()

        self.enemy_x = enemy_rect.left()
        self.enemy_x2 = enemy_rect.right()
        self.enemy_y = enemy_rect.top()
        self.enemy_y2 = enemy_rect.bottom()

        self.camera_x = self.scene_width / 2

# ======================================================================================================================
# Lógica del jugador
        if self.rol == "player":
            self.view.centerOn(self.camera_x, self.player.scenePos().y())
    # Colisiones
        # Detección
            for item in self.player.collidingItems():
                if isinstance(item, Ladders):
                    self.player_coll_escalera = item
                    escalera_rect = item.mapToScene(item.boundingRect()).boundingRect()

                    self.escalera_x = escalera_rect.left()
                    self.escalera_x2 = escalera_rect.right()
                    self.escalera_y = escalera_rect.top()
                    self.escalera_y2 = escalera_rect.bottom()

                if isinstance(item, Platforms):
                    self.player_coll_platform = item
                    platform_rect = item.mapToScene(item.boundingRect()).boundingRect()

                    self.platform_x = platform_rect.left()
                    self.platform_x2 = platform_rect.right()
                    self.platform_y = platform_rect.top()
                    self.platform_y2 = platform_rect.bottom()

            for platform in self.scene.items():
                if isinstance(platform, Platforms):
                    platform_area1 = platform.mapToScene(QPolygonF(platform.area1())).boundingRect()
                    self.platform_area1_x = platform_area1.left()
                    self.platform_area1_x2 = platform_area1.right()
                    self.platform_area1_y = platform_area1.top()
                    self.platform_area1_y2 = platform_area1.bottom()

                    if platform_area1.intersects(player_rect):
                        self.player_coll_platform_area1 = True
                        if self.player_y2 <= self.platform_area1_y2:
                            self.player_gravity_speed = 1
                    else:
                        self.player_coll_platform_area1 = False

        # 1.1 Colisión con platforms
            if self.player_coll_platform:
                if (self.platform_y + self.platform_y_tolerance >= self.player_y2 >= self.platform_y -
                        self.platform_y_tolerance):
                    self.player_move_jump_lock = False

                # Salto
                if self.player_y >= self.platform_y2:
                    self.player_gravity_jump_speed = 0
                    self.player_jumping_state = False
                # Plataforma debajo del jugador
                if self.player_y2 <= self.platform_y + self.platform_y_tolerance and self.player_y < self.platform_y:
                    self.player_gravity_toggle = False
                    self.player_jumping_state = False
                    self.player_gravity_jump_speed = self.player_gravity_jump_speed_initial
                    if not self.player_move_walk_left and not self.player_move_walk_right:
                        self.player.set_direction("idle")
                # Plataforma lateral al jugador
                elif self.player_y2 > self.platform_y2:
                    if self.player_y2 > self.platform_y2 + self.platform_y_tolerance:
                        if self.player_x2 >= self.platform_x:
                            self.player_move_walk_right_lock = True
                        if self.player_x <= self.platform_x2:
                            self.player_move_walk_left_lock = True

        # 1.2 Colisión con escaleras
            if self.player_coll_escalera:
                self.player_move_climb_lock = False
                if self.player_move_climb_up or self.player_move_climb_down:
                    self.player_scaling_state = True
                    self.player_gravity_toggle = False
            else:
                self.player_move_climb_lock = True
                self.player_scaling_state = False

        # 2. Colisión con platforms y escaleras
            if self.player_coll_platform and self.player_coll_escalera:
                self.player_move_climb_lock = False
                if self.player_y2 <= self.escalera_y:
                    self.player_move_climb_up_lock = True
                else:
                    self.player_move_climb_up_lock = False
                if self.player_y2 > self.escalera_y + 1 and self.player_y < self.escalera_y:
                    self.player_move_horizontal_lock = True
                else:
                    self.player_move_horizontal_lock = False

                if self.player_y2 >= self.escalera_y2:
                    self.player_move_climb_down_lock = True
                    self.player_jumping_state = False
                else:
                    self.player_move_climb_down_lock = False

# ----------------------------------------------------------------------------------------------------------------------
# PowerUps
    # Regeneración
    # Inmunidad
            self.label_life.setText(f"❤️ {self.player_life_current}")
            self.label_regeneration.setText(f"️⚕️ {self.player_regeneration_current} s")
            self.label_immunity.setText(f"️🛡️ {self.player_immunity_current} s")
            self.label_run.setText(f"️🏃 {self.player_run_current} s")

# ----------------------------------------------------------------------------------------------------------------------
# Movimientos
    # Movimiento horizontal
            if not self.player_move_horizontal_lock:
        # Izquierda
                if self.player_move_walk_left and self.player_move_walk_left_lock == False:
                    if self.player_run_status and self.player_run_toggle:
                        # PowerUp Velocidad
                        self.player.moveBy(-self.player_speed * 2, 0)
                        self.player.set_direction("run_left")
                    else:
                        self.player.moveBy(-self.player_speed, 0)
                        self.player.set_direction("left")
        # Derecha
                if self.player_move_walk_right and self.player_move_walk_right_lock == False:
                    if self.player_run_status and self.player_run_toggle:
                        # PowerUp Velocidad
                        self.player.moveBy(self.player_speed * 2, 0)
                        self.player.set_direction("run_right")
                    else:
                        self.player.moveBy(self.player_speed, 0)
                        self.player.set_direction("right")

    # Escalado
            if not self.player_move_climb_lock:
        # Ascendente
                if not self.player_move_climb_up_lock:
                    if self.player_move_climb_up:
                        self.player.moveBy(0, -self.player_speed)
                        self.player.set_direction("climb_up")
        # Descendente
                if not self.player_move_climb_down_lock:
                    if self.player_move_climb_down:
                        self.player.moveBy(0, self.player_speed)
                        self.player.set_direction("climb_down")
            if self.player_scaling_state:
                self.player_gravity_toggle = False

    # Salto
            if not self.player_move_jump_lock and not self.player_scaling_state:
                tipo = None
                if self.player_move_jump_left:
                    tipo = "left"
                elif self.player_move_jump_right:
                    tipo = "right"
                elif self.player_move_jump_up:
                    tipo = "up"

                if tipo:
                    self.player_move_jump_last = tipo
                    self.player_move_jump_up = False
                    self.player_move_jump_left = False
                    self.player_move_jump_right = False
                    self.player_jumping_state = True
                    self.player_move_jump_lock = True
                    self.player_gravity_jump_speed = self.player_gravity_jump_speed_initial
                    self.player_gravity_toggle = False

            if self.player_jumping_state:
                if self.player_move_jump_last == "up":
                    self.player.set_direction("jump_up")
                    self.player.moveBy(0, -self.player_gravity_jump_speed)
                elif self.player_move_jump_last == "left":
                    self.player.set_direction("jump_left")
                    self.player.moveBy(-self.player_gravity_jump_speed * 1.25, -self.player_gravity_jump_speed * 0.75)
                elif self.player_move_jump_last == "right":
                    self.player.set_direction("jump_right")
                    self.player.moveBy(self.player_gravity_jump_speed * 1.25, -self.player_gravity_jump_speed * 0.75)

                # Ajuste para que dure más
                self.player_gravity_jump_speed -= 0.25  # antes era 1

                self.player._anim_speed = int(self.player_gravity_jump_speed * 0.01)

                if self.player_gravity_jump_speed <= 0:
                    self.player_jumping_state = False
                    self.player_gravity_toggle = True
                    self.player._anim_speed = 4

# ----------------------------------------------------------------------------------------------------------------------
# Gravedad
        if self.player_gravity_toggle:
            if self.player_jumping_state:
                self.i_player_damage_fall_accumulated -= self.player_gravity_jump_speed * 0.75
            if not self.player_jumping_state:
                print("NO ESTA SALTANDO")
                self.player.moveBy(0, self.player_gravity_speed)
                self.i_player_damage_fall_accumulated += self.player_gravity_speed
                if self.i_player_damage_fall_accumulated >= self.platform_separation:
                    self.i_player_damage_fall_accumulated = 0
                    self.player_damage_fall_accumulated += 1

        else:
            if self.player_damage_fall_accumulated >= 0:
                self.damage_management(player_damage_fall_accumulated_arg = self.player_damage_fall_accumulated)
            self.i_player_damage_fall_accumulated = 0


        if self.player_life_current <= 0:
            print("JUGADOR MUERTO (FALTA MÉTODO PARA EL ESTADO DE MUERTE DEL JUGADOR)")

# ----------------------------------------------------------------------------------------------------------------------
# Debug
        if self.show_collisions_toggle:
            self.show_collisions_dynamic()
# ======================================================================================================================

# ======================================================================================================================
# Controles
    def keyPressEvent(self, event):
        key = event.key()
        self.multiple_keys.add(key)

        if key == Qt.Key_D:
            print("self.platforms_separation", self.platform_separation)
            print("self.i_player_damage_fall_accumulated", self.i_player_damage_fall_accumulated)
            pass

        if key == Qt.Key_H:
            if self.rol == "player":
                self.player.moveBy(0, -256)

        if key == Qt.Key_Left:
            if self.rol == "player":
                self.player_move_walk_left = True

        if key == Qt.Key_Right:
            if self.rol == "player":
                self.player_move_walk_right = True

        if key == Qt.Key_Up:
            if self.rol == "player":
                self.player_move_climb_up = True

        if key == Qt.Key_Down:
            if self.rol == "player":
                self.player_move_climb_down = True

        if Qt.Key_Space in self.multiple_keys:
            if self.rol == "player":
                self.player_move_jump_up = False
                self.player_move_jump_left = False
                self.player_move_jump_right = False

                if Qt.Key_Left in self.multiple_keys:
                    self.player_move_jump_left = True
                elif Qt.Key_Right in self.multiple_keys:
                    self.player_move_jump_right = True
                else:
                    self.player_move_jump_up = True

        if key == Qt.Key_E:
            if self.rol == "player":
                if not self.player_immunity_lock:
                    self.power_up_immunity()

        if key == Qt.Key_R:
            if self.rol == "player":
                if not self.player_regeneration_lock:
                    self.power_up_regeneration()

        if key == Qt.Key_Control:
            if self.rol == "player":
                if self.player_run_status:
                    self.player_run_toggle = not self.player_run_toggle

                if not self.player_run_lock:
                    self.power_up_run()

        if Qt.Key_B in self.multiple_keys and Qt.Key_F3 in self.multiple_keys:
            self.method_show_collisions_toggle()

    def keyReleaseEvent(self, event):
        key = event.key()
        self.multiple_keys.discard(key)

        if key == Qt.Key_Left:
            if self.rol == "player":
                self.player_move_walk_left = False

        elif key == Qt.Key_Right:
            if self.rol == "player":
                self.player_move_walk_right = False

        elif key == Qt.Key_Space:
            if self.rol == "player":
                self.player_move_jump_up = False
                self.player_move_jump_left = False
                self.player_move_jump_right = False

        elif key == Qt.Key_Up:
            if self.rol == "player":
                self.player_move_climb_up = False

        elif key == Qt.Key_Down:
            if self.rol == "player":
                self.player_move_climb_down = False

        elif key == Qt.Key_R:
            if self.rol == "player":
                self.player_powerup_immunity = False

# ======================================================================================================================

# ======================================================================================================================
# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Level1()

    window.show()
    app.exec()
# ======================================================================================================================