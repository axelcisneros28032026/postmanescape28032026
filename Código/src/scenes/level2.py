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
from src.entities.blocks.plataforms_2 import Platforms
from src.entities.enemy.enemy1 import Enemy
from src.entities.items.coins import Coins
from src.entities.tools.aim import Aim
from src.entities.items.bones import Bones
from src.entities.player.player1 import Player
from src.network.network import GameServer, GameClient


sound = Sound()
# ======================================================================================================================

# ======================================================================================================================
# Nivel 1
class Level2(QWidget):

    # Señales
    signal_back = Signal() # Señal para volver a la pantalla anterior
    signal_back_init = Signal() # Señal para volver a la pantalla inicial
    signal_next_level = Signal() # Señal para avanzar

    # Lógica inicial
    def __init__(self, rol = "player", host = False, ip = "127.0.0.1", port = 25565, round = 1, prev_points = 0,
                 prev_enemy_points = 0 ):

        super().__init__()

        self.round = round
        self.player_points = prev_points
        self.enemy_points = prev_enemy_points

        # Definición de componentes
        self.layout = QGridLayout()
        self.layout_2 = QHBoxLayout()
        self.layout_2A = QHBoxLayout()
        self.layout_2A = QGridLayout()
        self.layout_2B = QGridLayout()
        self.layout_2B1 = QVBoxLayout()
        self.layout_2B2 = QVBoxLayout()

        self.pushButton_back = QPushButton("←")
        self.pushButton_back_init = QPushButton("🏠")

        # Otros:
        self.frequency = 8  # Frecuencia del hilo principal en milisegundos
        self.party_status = True # Estado de partida actual
        self.multiple_keys = set() # Conjunto de teclas presionadas
        self.iterator_show_collisions = 0 # Iterador auxiliar para el visor de colisiones
        self.show_collisions_toggle = False # Interruptor para mostrar colisiones

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

        self.i_player_damage_pvp_aux = 0 # Iterador auxiliar que contabiliza el daño por contacto
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Potenciadores:
        # Aceleración
        self.player_run_initial = 4 # Tiempo de aceleración inicial
        self.player_run_current = self.player_run_initial # Tiempo de aceleración actual (segundos)
        self.player_run_cooldown = 10  # Tiempo de espera para reactivar la aceleración (segundos)
        self.player_run_counter = 0 # Contador de la aceleración
        self.player_run_status = False # Estado de aceleración
        self.player_run_toggle = False # Interruptor de aceleración
        self.player_run_lock = False # Bloqueo de aceleración
        self.player_run_timer = QTimer(timeout = self.player_power_up_run) # Contador de aceleración

        # Regeneración
        self.player_regeneration_initial = 2 # Tiempo de regeneración inicial (segundos)
        self.player_regeneration_current = self.player_regeneration_initial # Tiempo de regeneración actual
        self.player_regeneration_cooldown = 7 # Tiempo de espera para reactivar la regeneración (segundos)
        self.player_regeneration_counter = 0  # Contador de la regeneración
        self.player_regeneration_status = False # Estado de regeneración
        self.player_regeneration_lock = False # Bloqueo de regeneración
        self.player_regeneration_timer = QTimer(timeout = self.player_power_up_regeneration)  # Contador de regeneración

        # Inmunidad
        self.player_immunity_initial = 2  # Tiempo de inmunidad inicial (segundos)
        self.player_immunity_current = self.player_immunity_initial  # Tiempo de inmunidad actual
        self.player_immunity_cooldown = 8  # Tiempo de espera para reactivar la inmunidad (segundos)
        self.player_immunity_counter = 0 # Contador de la inmunidad
        self.player_immunity_status = False  # Estado de inmunidad
        self.player_immunity_lock = False  # Bloqueo de inmunidad
        self.player_immunity_timer = QTimer(timeout=self.player_power_up_immunity)  # Contador de inmunidad
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
        self.player_coll_platform = False # Estado de colisión con platforma
        self.player_coll_platform_sup = False  # Estado de colisión con platforma superior
        self.player_coll_platform_inf = False  # Estado de colisión con platforma inferior
        # --------------------------------------------------------------------------------------------------------------
        # ==============================================================================================================

        # ==============================================================================================================
        # Enemigo
        self.enemy_anim_speed = 4  # Velocidad de animaciones
        self.enemy_life_initial = 15  # Vida inicial (unidades)
        self.enemy_life_current = self.enemy_life_initial  # Vida actual

        # --------------------------------------------------------------------------------------------------------------
        # Daños
        self.enemy_damage_bone = 2 # Daño por hueso lanzado
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Potenciadores:

        # Recargar
        self.enemy_reload_initial = 4  # Tiempo de regeneración inicial (segundos)
        self.enemy_reload_current = self.enemy_reload_initial  # Tiempo de regeneración actual
        self.enemy_reload_cooldown = 4  # Tiempo de espera para reactivar la regeneración (segundos)
        self.enemy_reload_counter = 0  # Contador de la regeneración
        self.enemy_reload_status = False  # Estado de regeneración
        self.enemy_reload_lock = False  # Bloqueo de regeneración
        self.enemy_reload_timer = QTimer(timeout = self.enemy_power_up_reload)  # Contador de regeneración

        # Escape
        self.enemy_escape_initial = 4  # Tiempo de inmunidad inicial (segundos)
        self.enemy_escape_current = self.enemy_escape_initial  # Tiempo de inmunidad actual
        self.enemy_escape_cooldown = 6  # Tiempo de espera para reactivar la inmunidad (segundos)
        self.enemy_escape_counter = 0  # Contador de la inmunidad
        self.enemy_escape_status = False  # Estado de inmunidad
        self.enemy_escape_lock = False  # Bloqueo de inmunidad
        self.enemy_escape_timer = QTimer(timeout=self.enemy_power_up_escape)  # Contador de inmunidad

        # Daño extra (Huesos)
        self.enemy_sharpness_initial = 4  # Tiempo de daño extra inicial (segundos)
        self.enemy_sharpness_current = self.enemy_sharpness_initial  # Tiempo de daño extra actual
        self.enemy_sharpness_cooldown = 6  # Tiempo de espera para reactivar daño extra (segundos)
        self.enemy_sharpness_counter = 0  # Contador del power-up de daño extra
        self.enemy_sharpness_status = False  # Estado del power-up de daño extra
        self.enemy_sharpness_lock = False  # Bloqueo del power-up de daño extra
        self.enemy_sharpness_timer = QTimer(timeout = self.enemy_power_up_sharpness) # Contador del power-up de daño extra
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Movimiento
        self.enemy_speed = 3  # Velocidad del enemigo

        #   Gravedad
        self.enemy_gravity_toggle = True  # Interruptor de gravedad
        self.enemy_gravity_speed_initial = 5  # Velocidad de gravedad inicial
        self.enemy_gravity_speed = self.enemy_gravity_speed_initial  # Velocidad de gravedad
        self.enemy_gravity_jump_speed_initial = self.enemy_gravity_speed_initial  # Velocidad de la gravedad de salto inicial
        self.enemy_gravity_jump_speed = self.enemy_gravity_jump_speed_initial  # Velocidad de la gravedad de salto

        #   Horizontal
        self.enemy_move_horizontal_lock = True  # Bloqueo de movimiento horizontal general
        self.enemy_move_walk_left_lock = False  # Bloqueo de movimiento horizontal a la izquierda
        self.enemy_move_walk_right_lock = False  # Bloqueo de movimiento horizontal a la derecha

        self.enemy_move_walk_left = False  # Movimiento horizontal a la izquierda
        self.enemy_move_walk_right = False  # Movimiento horizontal a la derecha

        #   Saltar
        self.enemy_move_jump_lock = False  # Bloqueo de salto general
        self.enemy_move_jump_up_lock = False  # Bloqueo de salto vertical

        self.enemy_move_jump_up = False  # Salto vertical
        self.enemy_move_jump_left = False  # Salto vertical a la izquierda
        self.enemy_move_jump_right = False  # Salto vertical a la derecha

        self.enemy_move_jump_last = None  # Tipo último de salto

        #   Escalar
        self.enemy_move_climb_lock = True  # Bloqueo de escalado general
        self.enemy_move_climb_up_lock = True  # Bloqueo de escalado hacia arriba
        self.enemy_move_climb_down_lock = False  # Bloqueo de escalado hacia abajo

        self.enemy_move_climb_up = False  # Escalado hacia arriba
        self.enemy_move_climb_down = False  # Escalado hacia abajo

        #   Estados
        self.enemy_throwing_bone_state = False # Estado de lanzamiento de hueso
        self.enemy_scaling_state = False  # Estado de escalado
        self.enemy_jumping_state = False  # Estado de salto

        # Colisiones
        self.enemy_coll_escalera = False  # Estado de colisión con escalera
        self.enemy_coll_platform = False  # Estado de colisión con platform
        # --------------------------------------------------------------------------------------------------------------

        # ==============================================================================================================

        # --------------------------------------------------------------------------------------------------------------
        # Temporizadores

        # Hilo principal
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)

        # ── Red ──────────────────────────────────────────────────────────────
        self.rol = rol
        self._next_rol = None
        self._net_ready = False  # True cuando hay conexión activa
        self._net_send_timer = QTimer()
        self._net_send_timer.setInterval(self.frequency)  # mismo rate que game_loop
        self._net_send_timer.timeout.connect(self._net_send_state)

        if host:  # Soy Servidor (no necesariamente enemy)
            self._server = GameServer(port=port)
            self._server.client_connected.connect(self._on_net_ready)
            self._server.received.connect(self._net_on_received)
            self._server.disconnected.connect(self._on_net_disconnected)
            self._server.start()
        else:  # Soy Cliente
            self._client = GameClient(host=ip, port=port)
            self._client.connected.connect(self._on_net_ready)
            self._client.received.connect(self._net_on_received)
            self._client.disconnected.connect(self._on_net_disconnected)
            self._client.connect_to_server()

        # El rol en pantalla se asigna por separado
        self.rol = rol  # ← no sobreescribir con "enemy"/"player" según host
        # ─────────────────────────────────────────────────────────────────────

        # Administrador de daño
        self.player_damage_timer = QTimer()
        self.player_damage_timer.setSingleShot(True)
        self.player_damage_timer.timeout.connect(self.player_damage_management_aux)

        # --------------------------------------------------------------------------------------------------------------

        # Puntuaciones altas
        self.players_top = 0 # Puntos top del rol actual

        # Visualización de datos
        if self.rol == "player":
            self.label = QLabel(f"Nivel 2 | Ronda {self.round}")
            self.label.setAlignment(Qt.AlignCenter)
            self.label_2 = QLabel(f"I - {self.player_points}")
            self.label_3 = QLabel(f"Top - {self.players_top}")
            self.label_4 = QLabel(f"II - {self.enemy_points}")
            self.label_5 = QLabel(f"❤️ {self.player_life_current}")
            self.label_5.setAlignment(Qt.AlignLeft)
            self.label_6 = QLabel(f"️⚕️ {self.player_regeneration_current} s")
            self.label_6.setAlignment(Qt.AlignLeft)
            self.label_7 = QLabel(f"️🛡️ {self.player_immunity_current} s")
            self.label_7.setAlignment(Qt.AlignLeft)
            self.label_8 = QLabel(f"️🏃 {self.player_run_current} s")
            self.label_8.setAlignment(Qt.AlignLeft)
        if self.rol == "enemy":
            self.label = QLabel(f"Nivel 2 | Ronda {self.round}")
            self.label.setAlignment(Qt.AlignCenter)
            self.label_2 = QLabel(f"I - {self.player_points}")
            self.label_2.setAlignment(Qt.AlignCenter)
            self.label_3 = QLabel(f"Top - {self.players_top}")
            self.label_3.setAlignment(Qt.AlignCenter)
            self.label_4 = QLabel(f"II - {self.enemy_points}")
            self.label_4.setAlignment(Qt.AlignCenter)
            self.label_5 = QLabel(f"🦴 {self.enemy_life_current}")
            self.label_5.setAlignment(Qt.AlignLeft)
            self.label_6 = QLabel(f"️🔃 {self.enemy_reload_current} s")
            self.label_6.setAlignment(Qt.AlignLeft)
            self.label_7 = QLabel(f"️⛓️ {self.enemy_escape_current} s")
            self.label_7.setAlignment(Qt.AlignLeft)
            self.label_8 = QLabel(f"️💪 {self.enemy_sharpness_current} s")
            self.label_8.setAlignment(Qt.AlignLeft)

        # Construcción de escena
        self.scene_width = 1280
        self.scene_height = 720
        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)
        self.view = QGraphicsView(self.scene)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.block1_n = 6  # Número de plataformaas (Par)

        self.enemy = Enemy(speed = self.enemy_speed, anim_speed = int(1000 / self.frequency * 0.115))
        self.victim = Victim(speed = 5, anim_speed = int(1000 / self.frequency * 0.075))
        self.player = Player(speed = self.player_speed, anim_speed = int(1000 / self.frequency * 0.115))

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
            self.platform_y_tolerance = 2

            self.ladder = Ladders()

            if i == 0:
                self.platform.setPos(int((self.scene_width / 2) - self.platform.pixmap().width() / 2),
                                     int(self.scene_height / n * 2 - self.platform.pixmap().height()))
                self.platform_separation = self.platform.pixmap().height() + 16

                self.enemy_posX_0 = self.platform.pos().x()
                self.enemy_posY_0 = int(self.platform.pos().y() - 16)
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

        # Contenedor 1
        self.layout_2A.addWidget(self.label, 0, 1, 1, 1)
        self.layout_2A.addWidget(self.label_2, 1, 0, 1, 1)
        self.layout_2A.addWidget(self.label_3, 1, 1, 1, 1)
        self.layout_2A.addWidget(self.label_4, 1, 2, 1, 1)

        # Contenedor 2 (Botones de retorno, estadísticas y datos)
        self.layout_2B1.addWidget(self.label_5)
        self.layout_2B1.addWidget(self.label_6)
        self.layout_2B2.addWidget(self.label_7)
        self.layout_2B2.addWidget(self.label_8)
        self.layout_2B.addLayout(self.layout_2B1, 0, 0, 1, 1)
        self.layout_2B.addLayout(self.layout_2B2, 0, 1, 1, 1)
        self.layout_2.addWidget(self.pushButton_back)
        self.layout_2.addWidget(self.pushButton_back_init)
        self.layout_2.addLayout(self.layout_2A)
        self.layout_2.addLayout(self.layout_2B)

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

    # Métodos
    def _on_net_ready(self):
        self._net_ready = True
        self.timer.start(self.frequency)
        self._net_send_timer.start()
        print(f"[Red] Conexión lista. Rol: {self.rol}")

    def show_collisions_static(self):

        if not self.show_collisions_toggle:
            return

        for item in list(self.scene.items()):
            if isinstance(item, QGraphicsPolygonItem):
                self.scene.removeItem(item)

        for item in self.scene.items():

            if not isinstance(item, QGraphicsPixmapItem):
                continue

            if isinstance(item, Victim):
                polygon = item.mapToScene(item.shape().toFillPolygon())

                poly_item = QGraphicsPolygonItem(polygon)
                poly_item.setPen(QPen(QColor(0, 128, 255), 1))
                poly_item.setBrush(QColor(0, 128, 255, 50))
                self.scene.addItem(poly_item)

                continue

            if isinstance(item, Enemy):
                polygon = item.mapToScene(item.shape().toFillPolygon())

                poly_item = QGraphicsPolygonItem(polygon)
                poly_item.setPen(QPen(QColor(128, 0, 0), 1))
                poly_item.setBrush(QColor(128, 0, 0, 50))
                self.scene.addItem(poly_item)

                continue

            if isinstance(item, Player):
                polygon = item.mapToScene(item.shape().toFillPolygon())

                poly_item = QGraphicsPolygonItem(polygon)
                poly_item.setPen(QPen(QColor(0, 128, 0), 1))
                poly_item.setBrush(QColor(0, 128, 0, 50))
                self.scene.addItem(poly_item)

                continue

            if isinstance(item, Platforms):
                rect1 = item.boundingRect()

                polygon1 = QPolygonF([
                    rect1.topLeft(),
                    rect1.topRight(),
                    rect1.bottomRight(),
                    rect1.bottomLeft()
                ])

                polygon1 = item.mapToScene(polygon1)

                poly_item1 = QGraphicsPolygonItem(polygon1)
                poly_item1.setPen(QPen(QColor(0, 150, 255), 2, Qt.SolidLine))  # azul
                poly_item1.setBrush(QColor(0, 150, 255, 25))
                self.scene.addItem(poly_item1)

                rect2 = item.area1()

                polygon2 = QPolygonF([
                    rect2.topLeft(),
                    rect2.topRight(),
                    rect2.bottomRight(),
                    rect2.bottomLeft()
                ])

                polygon2 = item.mapToScene(polygon2)

                poly_item2 = QGraphicsPolygonItem(polygon2)
                poly_item2.setPen(QPen(QColor(255, 0, 0), 1, Qt.SolidLine))
                poly_item2.setBrush(QColor(255, 0, 0, 25))
                self.scene.addItem(poly_item2)

            polygon = item.mapToScene(item.shape().toFillPolygon())

            poly_item = QGraphicsPolygonItem(polygon)
            poly_item.setPen(QPen(Qt.green, 1))
            poly_item.setBrush(Qt.transparent)
            self.scene.addItem(poly_item)

    def show_collisions_dynamic(self):
        if not self.show_collisions_toggle:
            return

        for item in list(self.scene.items()):
            if isinstance(item, QGraphicsPolygonItem) and item.data(0) == "debug_player_enemy":
                self.scene.removeItem(item)

        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                continue

            polygon = item.mapToScene(item.shape().toFillPolygon())

            if item is self.player:
                pen = QPen(QColor(0, 255, 0), 1)

                poly_item = QGraphicsPolygonItem(polygon)
                poly_item.setPen(pen)
                poly_item.setBrush(QColor(0, 255, 0, 50))

                poly_item.setData(0, "debug_player_enemy")

                self.scene.addItem(poly_item)
                continue

            if item is self.enemy:
                pen = QPen(QColor(255, 0, 0), 1)

                poly_item = QGraphicsPolygonItem(polygon)
                poly_item.setPen(pen)
                poly_item.setBrush(QColor(255, 0, 0, 50))

                poly_item.setData(0, "debug_player_enemy")

                self.scene.addItem(poly_item)
                continue

            try:
                if item is self.bone:
                    pen = QPen(QColor(255, 0, 0), 1)

                    poly_item = QGraphicsPolygonItem(polygon)
                    poly_item.setPen(pen)
                    poly_item.setBrush(QColor(255, 0, 0, 50))

                    poly_item.setData(0, "debug_player_enemy")

                    self.scene.addItem(poly_item)
                    continue
            except:
                pass

    def method_show_collisions_toggle(self):
        self.show_collisions_toggle = not self.show_collisions_toggle
        if self.show_collisions_toggle:
            self.show_collisions_static()
            self.show_collisions_dynamic()
        else:
            for item in self.scene.items():
                if isinstance(item, QGraphicsPolygonItem):
                    self.scene.removeItem(item)

    def update_score_labels(self):
        # Etiquetas dinámicas según el rol
        if self.rol == "player":
            self.label_2.setText(f"I - {self.player_points}")
            self.label_4.setText(f"II - {self.enemy_points}")
        elif self.rol == "enemy":
            self.label_2.setText(f"I - {self.enemy_points}")
            self.label_4.setText(f"II - {self.player_points}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4.setAlignment(Qt.AlignCenter)

        # Actualizar la etiqueta Top con la puntuación más alta
        self.players_top = max(self.player_points, self.enemy_points)
        self.label_3.setText(f"Top - {self.players_top}")

    # ======================================================================================================================
# Jugador

    def method_player_move_jump(self, type):
        self.player_move_jump_type = type
        if self.player_move_jump_type == "up":
            self.player.set_direction("jump_up")
            self.player_move_jump_lock = False

    def player_power_up_immunity(self):
        # Activar Power-Up
        if not self.player_immunity_lock:
            self.player_immunity_lock = True
            self.player_immunity_status = True
            self.label_5.setStyleSheet("""QLabel { color: orange; }""")
            self.player_immunity_counter = self.player_immunity_initial
            self.player_immunity_current = self.player_immunity_counter
            self.player_immunity_timer.start(1000)
            self.label_7.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.player_immunity_counter)
            return
        self.player_immunity_counter -= 1

        if self.player_immunity_status:
            # Finalizar Power-Up
            if self.player_immunity_counter <= 0:
                self.player_immunity_status = False
                # Iniciar cooldown
                self.player_immunity_counter = self.player_immunity_cooldown
                self.player_immunity_current = self.player_immunity_counter
                self.label_7.setStyleSheet("""QLabel { color: gray; }""")
                self.label_5.setStyleSheet("QLabel { color: yellow; }")
                return
            self.player_immunity_current = self.player_immunity_counter
            return

        # Fin de cooldown
        if not self.player_immunity_status:
            if self.player_immunity_counter <= 0:
                self.player_immunity_lock = False
                self.player_immunity_counter = self.player_immunity_initial
                self.player_immunity_current = self.player_immunity_counter
                self.player_immunity_timer.stop()
                print(self.player_immunity_counter)
                self.label_7.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.player_immunity_current = self.player_immunity_counter
            print(self.player_immunity_counter)

    def player_power_up_regeneration(self):
        # Activar Power-Up
        if not self.player_regeneration_lock:
            self.player_regeneration_lock = True
            self.player_regeneration_status = True
            self.label_5.setStyleSheet("""QLabel { color: green; }""")
            if self.player_life_current < self.player_life_initial:
                self.player_life_current += 1
            self.player_regeneration_counter = self.player_regeneration_initial
            self.player_regeneration_current = self.player_regeneration_counter
            self.player_regeneration_timer.start(1000)
            self.label_6.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.player_regeneration_counter)
            return
        self.player_regeneration_counter -= 1

        if self.player_regeneration_status:
            self.label_5.setStyleSheet("""QLabel { color: green; }""")
            if self.player_regeneration_counter >= 1:
                if self.player_life_current < self.player_life_initial:
                    self.player_life_current += 1
            # Finalizar Power-Up
            if self.player_regeneration_counter <= 0:
                self.player_regeneration_status = False
                # Iniciar cooldown
                self.player_regeneration_counter = self.player_regeneration_cooldown
                self.player_regeneration_current = self.player_regeneration_counter
                self.label_6.setStyleSheet("""QLabel { color: gray; }""")
                self.label_5.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.player_regeneration_current = self.player_regeneration_counter
            return

        # Fin de cooldown
        if not self.player_regeneration_status:
            if self.player_regeneration_counter <= 0:
                self.player_regeneration_lock = False
                self.player_regeneration_counter = self.player_regeneration_initial
                self.player_regeneration_current = self.player_regeneration_counter
                self.player_regeneration_timer.stop()
                print(self.player_regeneration_counter)
                self.label_6.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.player_regeneration_current = self.player_regeneration_counter
            print(self.player_regeneration_counter)

    def player_power_up_run(self):
        # Activar Power-Up
        if not self.player_run_lock:
            self.player_run_lock = True
            self.player_run_status = True
            self.player_run_toggle = True
            self.player_run_counter = self.player_run_initial
            self.player_run_current = self.player_run_counter
            self.player_run_timer.start(1000)
            self.label_8.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.player_run_counter)
            return
        self.player_run_counter -= 1

        if self.player_run_status:
            if self.player_life_current < self.player_life_initial:
                self.player_life_current += 1

            # Finalizar Power-Up
            if self.player_run_counter <= 0:
                self.player_run_status = False
                self.player_run_toggle = False
                # Iniciar cooldown
                self.player_run_counter = self.player_run_cooldown
                self.player_run_current = self.player_run_counter
                print(self.player_run_counter)
                self.label_8.setStyleSheet("""QLabel { color: gray; }""")
                return
            self.player_run_current = self.player_run_counter
            print(self.player_run_counter)
            return

        # Fin de cooldown
        if not self.player_run_status:
            if self.player_run_counter <= 0:
                self.player_run_lock = False
                self.player_run_counter = self.player_run_initial
                self.player_run_current = self.player_run_counter
                self.player_run_timer.stop()
                self.label_8.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.player_run_current = self.player_run_counter
            print(self.player_run_counter)

    def player_damage_management(self, player_damage_fall_accumulated_arg= 0, player_damage_pvp_arg = 0):

        total_damage = player_damage_fall_accumulated_arg + player_damage_pvp_arg

        if total_damage <= 0:
            return

        if not self.player_immunity_status:
            self.player_life_current -= total_damage

        self.player_damage_fall_accumulated = 0

        if not self.player_immunity_status:
            self.player_damage_receiving_status = True
            self.label_5.setStyleSheet("""QLabel { color: red; }""")

        self.player_damage_timer.start(1000)

    def player_damage_management_aux(self):
        self.player_damage_receiving_status = False
        self.label_5.setStyleSheet("""QLabel { color: yellow; }""")

# ======================================================================================================================

# ======================================================================================================================
# Enemigo

    def method_enemy_move_jump(self, type):
        self.enemy_move_jump_type = type
        if self.enemy_move_jump_type == "up":
            self.enemy.set_direction("jump_up")
            self.enemy_move_jump_lock = False

    def enemy_power_up_escape(self):
        # Activar Power-Up
        if not self.enemy_escape_lock:
            self.enemy_move_horizontal_lock = False

            self.enemy_escape_lock = True
            self.enemy_escape_status = True
            self.enemy_escape_counter = self.enemy_escape_initial
            self.enemy_escape_current = self.enemy_escape_counter
            self.enemy_escape_timer.start(1000)
            self.label_7.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.enemy_escape_counter)
            return
        self.enemy_escape_counter -= 1

        if self.enemy_escape_status:
            # Finalizar Power-Up
            if self.enemy_escape_counter <= 0:
                self.enemy_escape_status = False
                self.enemy_move_horizontal_lock = True
                self.enemy.setPos(self.enemy_posX_0, self.enemy_posY_0)
                # Iniciar cooldown
                self.enemy_escape_counter = self.enemy_escape_cooldown
                self.enemy_escape_current = self.enemy_escape_counter
                self.label_7.setStyleSheet("""QLabel { color: gray; }""")
                return
            self.enemy_escape_current = self.enemy_escape_counter
            return

        # Fin de cooldown
        if not self.enemy_escape_status:
            if self.enemy_escape_counter <= 0:
                self.enemy_escape_lock = False
                self.enemy_escape_counter = self.enemy_escape_initial
                self.enemy_escape_current = self.enemy_escape_counter
                self.enemy_escape_timer.stop()
                print(self.enemy_escape_counter)
                self.label_7.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.enemy_escape_current = self.enemy_escape_counter
            print(self.enemy_escape_counter)

    def enemy_power_up_reload(self):
        # Activar Power-Up
        if not self.enemy_reload_lock:
            self.enemy_reload_lock = True
            self.enemy_reload_status = True
            self.label_5.setStyleSheet("""QLabel { color: green; }""")
            if self.enemy_life_current < self.enemy_life_initial:
                self.enemy_life_current += 1
            self.enemy_reload_counter = self.enemy_reload_initial
            self.enemy_reload_current = self.enemy_reload_counter
            self.enemy_reload_timer.start(1000)
            self.label_6.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.enemy_reload_counter)
            return
        self.enemy_reload_counter -= 1

        if self.enemy_reload_status:
            self.label_5.setStyleSheet("""QLabel { color: green; }""")
            if self.enemy_reload_counter >= 1:
                if self.enemy_life_current < self.enemy_life_initial:
                    self.enemy_life_current += 1
            # Finalizar Power-Up
            if self.enemy_reload_counter <= 0:
                self.enemy_reload_status = False
                # Iniciar cooldown
                self.enemy_reload_counter = self.enemy_reload_cooldown
                self.enemy_reload_current = self.enemy_reload_counter
                self.label_6.setStyleSheet("""QLabel { color: gray; }""")
                self.label_5.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.enemy_reload_current = self.enemy_reload_counter
            return

        # Fin de cooldown
        if not self.enemy_reload_status:
            if self.enemy_reload_counter <= 0:
                self.enemy_reload_lock = False
                self.enemy_reload_counter = self.enemy_reload_initial
                self.enemy_reload_current = self.enemy_reload_counter
                self.enemy_reload_timer.stop()
                print(self.enemy_reload_counter)
                self.label_6.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.enemy_reload_current = self.enemy_reload_counter
            print(self.enemy_reload_counter)

    def enemy_power_up_sharpness(self):
        # Activar Power-Up
        if not self.enemy_sharpness_lock:
            self.enemy_damage_bone += 1

            self.enemy_sharpness_lock = True
            self.enemy_sharpness_status = True
            self.enemy_sharpness_counter = self.enemy_sharpness_initial
            self.enemy_sharpness_current = self.enemy_sharpness_counter
            self.enemy_sharpness_timer.start(1000)
            self.label_8.setStyleSheet("""QLabel { color: cyan; }""")
            print(self.enemy_sharpness_counter)
            return
        self.enemy_sharpness_counter -= 1

        if self.enemy_sharpness_status:
            # Finalizar Power-Up
            if self.enemy_sharpness_counter <= 0:
                self.enemy_sharpness_status = False
                self.enemy_damage_bone -= 1
                # Iniciar cooldown
                self.enemy_sharpness_counter = self.enemy_sharpness_cooldown
                self.enemy_sharpness_current = self.enemy_sharpness_counter
                self.label_8.setStyleSheet("""QLabel { color: gray; }""")
                return
            self.enemy_sharpness_current = self.enemy_sharpness_counter
            return

        # Fin de cooldown
        if not self.enemy_sharpness_status:
            if self.enemy_sharpness_counter <= 0:
                self.enemy_sharpness_lock = False
                self.enemy_sharpness_counter = self.enemy_sharpness_initial
                self.enemy_sharpness_current = self.enemy_sharpness_counter
                self.enemy_sharpness_timer.stop()
                print(self.enemy_sharpness_counter)
                self.label_8.setStyleSheet("""QLabel { color: yellow; }""")
                return
            self.enemy_sharpness_current = self.enemy_sharpness_counter
            print(self.enemy_sharpness_counter)

    def enemy_throw_bones(self):
        if self.enemy_throwing_bone_state:
            self.scene.removeItem(self.enemy_aim)
            if self.enemy_life_current > 0:
                try:
                    self.scene.removeItem(self.bone)
                except:
                    pass
                self.bone = Bones()
                self.bone.setPos(self.enemy_aim.pos().x(), self.enemy_aim.pos().y())
                self.enemy_life_current -= 1
                sound.throw_bone()
                self.scene.addItem(self.bone)
                self.bone.setZValue(10)
        if not self.enemy_throwing_bone_state:
            self.enemy_aim = Aim()
            self.enemy_aim.setPos((self.enemy_x + self.enemy_x2) / 2 - 32, (self.enemy_y2 + self.enemy_y) / 2 - 32)
            self.scene.addItem(self.enemy_aim)
            sound.aim()
            self.enemy_aim.setZValue(10)
        self.enemy_throwing_bone_state = not self.enemy_throwing_bone_state

    def manage_game_progress(self, winner=None):
        if not self.party_status:
            return

        self.timer.stop()
        self._net_send_timer.stop()
        self.party_status = False
        self.winner = winner

        if hasattr(self, "bone") and self.bone.scene():
            self.scene.removeItem(self.bone)

        print("GANADOR:", self.winner)
        self.round += 1

        if hasattr(self, "_server"):
            if self.rol == "enemy":
                my_next_rol = "player"  # servidor pasa a player
                peer_next_rol = "enemy"  # cliente pasa a enemy
            else:  # servidor es player
                my_next_rol = "enemy"  # servidor pasa a enemy
                peer_next_rol = "player"  # cliente pasa a player

            self._next_rol = my_next_rol
            print(f"[Servidor] Rol actual: {self.rol} → siguiente: {my_next_rol} | Peer siguiente: {peer_next_rol}")

            self._net_send({
                "type": "next_round",
                "winner": winner,
                "your_next_rol": peer_next_rol,
                "round": self.round,
            })
            QTimer.singleShot(800, self.signal_next_level.emit)
        else:
            self._net_send({"type": "game_over", "winner": winner})
            print("[Cliente] Esperando instrucciones del servidor...")
    # ======================================================================================================================

    def scheduler(self, ms, func, *funcs):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(func)
        for f in funcs:
            timer.timeout.connect(f)
        timer.start(ms)

# ======================================================================================================================

# ======================================================================================================================
# Hilo principal
    def game_loop(self):
        if not self.party_status:
            return
        net_mode = self._net_ready

        if self._net_ready:

            self.update_score_labels()

            # Jugador
            self.player_gravity_speed = self.player_gravity_speed_initial

            self.player_speed = self.player.speed
            if not self.player_jumping_state:
                self.player._anim_speed = int(1000 / self.frequency * 0.115)

            self.player_coll_escalera = None
            self.player_coll_platform = None
            self.player_coll_platform_inf = None
            self.player_move_horizontal_lock = False
            self.player_move_walk_left_lock = False
            self.player_move_walk_right_lock = False

            if not self.player_scaling_state:
                self.player_move_climb_lock = True
                self.player_move_climb_up_lock = True
                self.player_move_climb_down_lock = True

            if not self.player_scaling_state and not self.player_jumping_state:
                self.player_gravity_toggle = True

            # Enemigo
            self.enemy_gravity_speed = self.enemy_gravity_speed_initial

            self.enemy_speed = self.enemy.speed
            if not self.enemy_jumping_state:
                self.enemy._anim_speed = int(1000 / self.frequency * 0.115)

            self.enemy_coll_escalera = None
            self.enemy_coll_platform = None
            #self.enemy_move_horizontal_lock = False
            self.enemy_move_walk_left_lock = False
            self.enemy_move_walk_right_lock = False

            if not self.enemy_scaling_state:
                self.enemy_move_climb_lock = True
                self.enemy_move_climb_up_lock = True
                self.enemy_move_climb_down_lock = True

            if not self.enemy_scaling_state and not self.enemy_jumping_state:
                self.enemy_gravity_toggle = True

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

        # Colisiones - Detección
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

                    if self.player_y > self.platform_y and self.player_y2 > self.platform_y2:
                        self.player_coll_platform_sup = True
                    elif self.player_y < self.platform_y and self.player_y2 < self.platform_y2:
                        self.player_coll_platform_inf = True

                if isinstance(item, Coins):
                    sound.money_pickup()
                    self.scene.removeItem(item)
                    self.player_points += 1

                if isinstance(item, Victim):
                    if self.party_status:  # ← guard
                        self.manage_game_progress(winner="player")

                if isinstance(item, Enemy):
                    self.i_player_damage_pvp_aux += 1
                    if self.i_player_damage_pvp_aux >= 1000 / self.frequency:
                        self.player_damage_management(player_damage_pvp_arg = 1)
                        self.i_player_damage_pvp_aux = 0

                if isinstance(item, Bones):
                    self.player_damage_management(player_damage_pvp_arg = self.enemy_damage_bone)
                    self.scene.removeItem(self.bone)

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

                    # Colisiones
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

            # Enemigo
            #   Colisiones
            #       Detección
            for item in self.enemy.collidingItems():
                if isinstance(item, Ladders):
                    self.enemy_coll_escalera = item
                    escalera_rect = item.mapToScene(item.boundingRect()).boundingRect()

                    self.escalera_x = escalera_rect.left()
                    self.escalera_x2 = escalera_rect.right()
                    self.escalera_y = escalera_rect.top()
                    self.escalera_y2 = escalera_rect.bottom()

                if isinstance(item, Platforms):
                    self.enemy_coll_platform = item
                    platform_rect = item.mapToScene(item.boundingRect()).boundingRect()

                    self.platform_x = platform_rect.left()
                    self.platform_x2 = platform_rect.right()
                    self.platform_y = platform_rect.top()
                    self.platform_y2 = platform_rect.bottom()

                if isinstance(item, Coins):
                    sound.money_pickup()
                    self.scene.removeItem(item)
                    self.enemy_points += 1

                if isinstance(item, Victim):
                    print("¡Jugador ha ganado!")

                if isinstance(item, Player):
                    if self.enemy_move_walk_left:
                        if self.enemy_x >= self.player_x:
                            self.player.moveBy(-1.5 * self.enemy_speed, 0)
                    elif self.enemy_move_walk_right:
                        if self.enemy_x2 <= self.player_x2:
                            self.player.moveBy(1.5 * self.enemy_speed, 0)

            for platform in self.scene.items():
                if isinstance(platform, Platforms):
                    platform_area1 = platform.mapToScene(QPolygonF(platform.area1())).boundingRect()
                    self.platform_area1_x = platform_area1.left()
                    self.platform_area1_x2 = platform_area1.right()
                    self.platform_area1_y = platform_area1.top()
                    self.platform_area1_y2 = platform_area1.bottom()

                    if platform_area1.intersects(enemy_rect):
                        self.enemy_coll_platform_area1 = True
                        if self.enemy_y2 <= self.platform_area1_y2:
                            self.enemy_gravity_speed = 1
                    else:
                        self.enemy_coll_platform_area1 = False

            # 1.1 Colisión con platforms
            if self.enemy_coll_platform:
                if (self.platform_y + self.platform_y_tolerance >= self.enemy_y2 >= self.platform_y -
                        self.platform_y_tolerance):
                    self.enemy_move_jump_lock = False

                # Salto
                if self.enemy_y >= self.platform_y2:
                    self.enemy_gravity_jump_speed = 0
                    self.enemy_jumping_state = False
                # Plataforma debajo del jugador
                if self.enemy_y2 <= self.platform_y + self.platform_y_tolerance and self.enemy_y < self.platform_y:
                    self.enemy_gravity_toggle = False
                    self.enemy_jumping_state = False
                    self.enemy_gravity_jump_speed = self.enemy_gravity_jump_speed_initial
                    if not self.enemy_move_walk_left and not self.enemy_move_walk_right:
                        self.enemy.set_direction("idle")
                # Plataforma lateral al jugador
                elif self.enemy_y2 > self.platform_y2:
                    if self.enemy_y2 > self.platform_y2 + self.platform_y_tolerance:
                        if self.enemy_x2 >= self.platform_x:
                            self.enemy_move_walk_right_lock = True
                        if self.enemy_x <= self.platform_x2:
                            self.enemy_move_walk_left_lock = True

            # 1.2 Colisión con escaleras
            if self.enemy_coll_escalera:
                self.enemy_move_climb_lock = False
                if self.enemy_move_climb_up or self.enemy_move_climb_down:
                    self.enemy_scaling_state = True
                    self.enemy_gravity_toggle = False
            else:
                self.enemy_move_climb_lock = True
                self.enemy_scaling_state = False

            # 2. Colisión con platforms y escaleras
            if self.enemy_coll_platform and self.enemy_coll_escalera:
                self.enemy_move_climb_lock = False
                if self.enemy_y2 <= self.escalera_y:
                    self.enemy_move_climb_up_lock = True
                else:
                    self.enemy_move_climb_up_lock = False
                if self.enemy_y2 > self.escalera_y + 1 and self.enemy_y < self.escalera_y:
                    self.enemy_move_horizontal_lock = True
                else:
                    self.enemy_move_horizontal_lock = False

                if self.enemy_y2 >= self.escalera_y2:
                    self.enemy_move_climb_down_lock = True
                    self.enemy_jumping_state = False
                else:
                    self.enemy_move_climb_down_lock = False

        # ==================================================================================================================
        # Jugador - Lógica principal
            if self.rol == "player":
                self.view.centerOn(self.camera_x, self.player.scenePos().y())

        # ------------------------------------------------------------------------------------------------------------------
        # Etiquetas
                self.label_5.setText(f"❤️ {self.player_life_current}")
                self.label_6.setText(f"️⚕️ {self.player_regeneration_current} s")
                self.label_7.setText(f"️🛡️ {self.player_immunity_current} s")
                self.label_8.setText(f"️🏃 {self.player_run_current} s")
        # ------------------------------------------------------------------------------------------------------------------

        # Movimientos:
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
                        self.player.moveBy(-self.player_gravity_jump_speed * 1.1, -self.player_gravity_jump_speed * 0.75)
                    elif self.player_move_jump_last == "right":
                        self.player.set_direction("jump_right")
                        self.player.moveBy(self.player_gravity_jump_speed * 1.1, -self.player_gravity_jump_speed * 0.75)

                    # Ajuste para que dure más
                    self.player_gravity_jump_speed -= 0.25  # antes era 1

                    self.player._anim_speed = int(self.player_gravity_jump_speed * 0.01)

                    if self.player_gravity_jump_speed <= 0:
                        self.player_jumping_state = False
                        self.player_gravity_toggle = True
                        self.player._anim_speed = 4

                # Verificar si el jugador salió de la escena
                if (self.player.x() < 0 or
                        self.player.x() > self.scene_width or
                        self.player.y() < 0 or
                        self.player.y() > self.scene_height):
                    self.player_life_current = 0
                    self.manage_game_progress(winner = "enemy")
        # ------------------------------------------------------------------------------------------------------------------
        # ==================================================================================================================

        # ==================================================================================================================
        # Enemigo - Lógica principal
            if self.rol == "enemy":
                self.view.centerOn(self.camera_x, self.enemy.scenePos().y())

        # ------------------------------------------------------------------------------------------------------------------
        # Visualización de datos
                self.label_5.setText(f"🦴 {self.enemy_life_current}")
                self.label_6.setText(f"️🔃 {self.enemy_reload_current} s")
                self.label_7.setText(f"️⛓️ {self.enemy_escape_current} s")
                self.label_8.setText(f"️💪 {self.enemy_sharpness_current} s")
        # ------------------------------------------------------------------------------------------------------------------

        # Movimientos:
        # Movimiento horizontal
                if not self.enemy_move_horizontal_lock:
            # Izquierda
                    if self.enemy_move_walk_left and self.enemy_move_walk_left_lock == False:
                        self.enemy.moveBy(-self.enemy_speed * 1.5, 0)
                        self.enemy.set_direction("run_left")
            # Derecha
                    if self.enemy_move_walk_right and self.enemy_move_walk_right_lock == False:
                        self.enemy.moveBy(self.enemy_speed * 1.5, 0)
                        self.enemy.set_direction("run_right")

            # Escalado
                if not self.enemy_move_climb_lock:
                # Ascendente
                    if not self.enemy_move_climb_up_lock:
                        if self.enemy_move_climb_up:
                            self.enemy.moveBy(0, -self.enemy_speed)
                            self.enemy.set_direction("climb_up")
                # Descendente
                    if not self.enemy_move_climb_down_lock:
                        if self.enemy_move_climb_down:
                            self.enemy.moveBy(0, self.enemy_speed)
                            self.enemy.set_direction("climb_down")
                if self.enemy_scaling_state:
                    self.enemy_gravity_toggle = False

            # Salto
                if not self.enemy_move_jump_lock and not self.enemy_scaling_state:
                    tipo = None
                    if self.enemy_move_jump_left:
                        tipo = "left"
                    elif self.enemy_move_jump_right:
                        tipo = "right"
                    elif self.enemy_move_jump_up:
                        tipo = "up"

                    if tipo:
                        self.enemy_move_jump_last = tipo
                        self.enemy_move_jump_up = False
                        self.enemy_move_jump_left = False
                        self.enemy_move_jump_right = False
                        self.enemy_jumping_state = True
                        self.enemy_move_jump_lock = True
                        self.enemy_gravity_jump_speed = self.enemy_gravity_jump_speed_initial
                        self.enemy_gravity_toggle = False

                if self.enemy_jumping_state:
                    if self.enemy_move_jump_last == "up":
                        self.enemy.set_direction("jump_up")
                        self.enemy.moveBy(0, -self.enemy_gravity_jump_speed)
                    elif self.enemy_move_jump_last == "left" and not self.enemy_move_horizontal_lock:
                        self.enemy.set_direction("jump_left")
                        self.enemy.moveBy(-self.enemy_gravity_jump_speed * 1.1,
                                          -self.enemy_gravity_jump_speed * 0.75)
                    elif self.enemy_move_jump_last == "right" and not self.enemy_move_horizontal_lock:
                        self.enemy.set_direction("jump_right")
                        self.enemy.moveBy(self.enemy_gravity_jump_speed * 1.1,
                                          -self.enemy_gravity_jump_speed * 0.75)

                    self.enemy_gravity_jump_speed -= 0.25

                    self.enemy._anim_speed = int(self.enemy_gravity_jump_speed * 0.01)

                    if self.enemy_gravity_jump_speed <= 0:
                        self.enemy_jumping_state = False
                        self.enemy_gravity_toggle = True
                        self.enemy._anim_speed = 4
        # ------------------------------------------------------------------------------------------------------------------
        # ==================================================================================================================

        # ------------------------------------------------------------------------------------------------------------------
        # Gravedad:
        # Jugador
            if self.player_gravity_toggle and self.rol == "player":
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
                    self.player_damage_management(player_damage_fall_accumulated_arg = self.player_damage_fall_accumulated)
                self.i_player_damage_fall_accumulated = 0

            if self.player_life_current <= 0:
                if self.party_status:
                    self.manage_game_progress(winner="enemy")

        # Enemigo
            if self.enemy_gravity_toggle and self.rol == "enemy":
                if not self.enemy_jumping_state:
                    print("NO ESTA SALTANDO")
                    self.enemy.moveBy(0, self.enemy_gravity_speed)

        # Huesos
            if hasattr(self, "bone"):
                self.bone.moveBy(1, 1)
                self.bone.set_direction("right")
        # ------------------------------------------------------------------------------------------------------------------

            # Debug
            if self.show_collisions_toggle:
                self.show_collisions_dynamic()

# ======================================================================================================================
    # =========================================================================
    # RED
    # =========================================================================

    def _net_send(self, data: dict):
        if not self._net_ready:
            return
        if hasattr(self, "_server"):
            self._server.send(data)
        elif hasattr(self, "_client"):
            self._client.send(data)

    def _on_net_disconnected(self):
        self._net_ready = False
        self._net_send_timer.stop()
        print("[Red] Peer desconectado.")

    def _net_send_state(self):
        if self.rol == "player":
            self._net_send({
                "type": "state",
                "player": {
                    "x": self.player.x(),
                    "y": self.player.y(),
                    "dir": self.player.current_direction,
                    "frame": getattr(self.player, "_frame_index", 0),
                    "life": self.player_life_current,
                    "points": self.player_points,
                    "jumping": self.player_jumping_state,
                },
            })
        elif self.rol == "enemy":
            packet = {
                "type": "state",
                "enemy": {
                    "x": self.enemy.x(),
                    "y": self.enemy.y(),
                    "dir": self.enemy.current_direction,
                    "frame": getattr(self.enemy, "_frame_index", 0),
                    "life": self.enemy_life_current,
                    "points": self.enemy_points,
                    "jumping": self.enemy_jumping_state,
                },
            }
            if hasattr(self, "bone") and self.bone.scene():
                packet["bone"] = {"active": True, "x": self.bone.x(), "y": self.bone.y()}
            else:
                packet["bone"] = {"active": False}
            self._net_send(packet)

    def _net_on_received(self, packet: dict):
        """Procesa un paquete recibido del peer."""
        ptype = packet.get("type")

        if ptype == "state":
            if self.rol == "enemy":
                p = packet.get("player", {})
                if p:
                    self.player.setPos(p["x"], p["y"])
                    self.player.set_direction(p.get("dir", "idle"))
                    self.player_life_current = p.get("life", self.player_life_current)
                    self.player_points       = p.get("points", self.player_points)
                    self.player_jumping_state = p.get("jumping", False)

            elif self.rol == "player":
                e = packet.get("enemy", {})
                if e:
                    self.enemy.setPos(e["x"], e["y"])
                    self.enemy.set_direction(e.get("dir", "idle"))
                    self.enemy_life_current = e.get("life", self.enemy_life_current)
                    self.enemy_points       = e.get("points", self.enemy_points)
                    self.enemy_jumping_state = e.get("jumping", False)

                bone_data = packet.get("bone", {})
                if bone_data.get("active"):
                    if not hasattr(self, "bone") or not self.bone.scene():
                        from src.entities.items.bones import Bones
                        self.bone = Bones()
                        self.scene.addItem(self.bone)
                        self.bone.setZValue(10)
                    self.bone.setPos(bone_data["x"], bone_data["y"])
                else:
                    if hasattr(self, "bone") and self.bone.scene():
                        self.scene.removeItem(self.bone)

        elif ptype == "next_round":
            if hasattr(self, "_client"):
                self._next_rol = packet.get("your_next_rol")
                self.round = packet.get("round", self.round)
                winner = packet.get("winner")
                print(f"[Cliente] Rol asignado: {self._next_rol} | Ronda: {self.round}")
                if self.party_status:
                    self.party_status = False
                    self.timer.stop()
                    self._net_send_timer.stop()
                QTimer.singleShot(800, self.signal_next_level.emit)

        elif ptype == "game_over":
            if hasattr(self, "_server") and self.party_status:
                self.manage_game_progress(winner=packet.get("winner"))

# ======================================================================================================================
# Controles
    def keyPressEvent(self, event):
        key = event.key()
        self.multiple_keys.add(key)

        if key == Qt.Key_H:
            if self.rol == "player":
                self.player.moveBy(0, -256)

        if self._net_ready:
            if key == Qt.Key_D:
                print("self.platforms_separation", self.platform_separation)
                print("self.i_player_damage_fall_accumulated", self.i_player_damage_fall_accumulated)
                pass

            if key == Qt.Key_T:
                if self.rol == "enemy":
                    self.enemy_throw_bones()

            if key == Qt.Key_Left:
                if self.rol == "player":
                    self.player_move_walk_left = True
                if self.rol == "enemy":
                    if self.enemy_throwing_bone_state:
                        try:
                            self.enemy_aim.moveBy(-16, 0)
                        except:
                            pass
                    else:
                        self.enemy_move_walk_left = True

            if key == Qt.Key_Right:
                if self.rol == "player":
                    self.player_move_walk_right = True
                if self.rol == "enemy":
                    if self.enemy_throwing_bone_state:
                        try:
                            self.enemy_aim.moveBy(16, 0)
                        except:
                            pass
                    else:
                        self.enemy_move_walk_right = True

            if key == Qt.Key_Up:
                if self.rol == "player":
                    self.player_move_climb_up = True
                if self.rol == "enemy":
                    if self.enemy_throwing_bone_state:
                        try:
                            self.enemy_aim.moveBy(0, -16)
                        except:
                            pass
                    else:
                        self.enemy_move_climb_up = True

            if key == Qt.Key_Down:
                if self.rol == "player":
                    self.player_move_climb_down = True
                if self.rol == "enemy":
                    if self.enemy_throwing_bone_state:
                        try:
                            self.enemy_aim.moveBy(0, 16)
                        except:
                            pass
                    else:
                        self.enemy_move_climb_down = True

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
                if self.rol == "enemy":
                    self.enemy_move_jump_up = False
                    self.enemy_move_jump_left = False
                    self.enemy_move_jump_right = False

                    if Qt.Key_Left in self.multiple_keys:
                        self.enemy_move_jump_left = True
                    elif Qt.Key_Right in self.multiple_keys:
                        self.enemy_move_jump_right = True
                    else:
                        self.enemy_move_jump_up = True

            if key == Qt.Key_E:
                if self.rol == "player":
                    if not self.player_immunity_lock:
                        self.player_power_up_immunity()
                if self.rol == "enemy":
                    if not self.enemy_escape_lock:
                        self.enemy_power_up_escape()

            if key == Qt.Key_R:
                if self.rol == "player":
                    if not self.player_regeneration_lock:
                        self.player_power_up_regeneration()
                if self.rol == "enemy":
                    if not self.enemy_reload_lock:
                        self.enemy_power_up_reload()

            if key == Qt.Key_Control:
                if self.rol == "player":
                    if self.player_run_status:
                        self.player_run_toggle = not self.player_run_toggle

                    if not self.player_run_lock:
                        self.player_power_up_run()

                if self.rol == "enemy":
                    if not self.enemy_sharpness_lock:
                        self.enemy_power_up_sharpness()

        if Qt.Key_B in self.multiple_keys and Qt.Key_F3 in self.multiple_keys:
            self.method_show_collisions_toggle()

    def keyReleaseEvent(self, event):
        key = event.key()
        self.multiple_keys.discard(key)

        if key == Qt.Key_Left:
            if self.rol == "player":
                self.player_move_walk_left = False
            if self.rol == "enemy":
                self.enemy_move_walk_left = False

        elif key == Qt.Key_Right:
            if self.rol == "player":
                self.player_move_walk_right = False
            if self.rol == "enemy":
                self.enemy_move_walk_right = False

        elif key == Qt.Key_Space:
            if self.rol == "player":
                self.player_move_jump_up = False
                self.player_move_jump_left = False
                self.player_move_jump_right = False
            if self.rol == "enemy":
                self.enemy_move_jump_up = False
                self.enemy_move_jump_left = False
                self.enemy_move_jump_right = False

        elif key == Qt.Key_Up:
            if self.rol == "player":
                self.player_move_climb_up = False
            if self.rol == "enemy":
                self.enemy_move_climb_up = False

        elif key == Qt.Key_Down:
            if self.rol == "player":
                self.player_move_climb_down = False
            if self.rol == "enemy":
                self.enemy_move_climb_down = False

        elif key == Qt.Key_R:
            if self.rol == "player":
                self.player_powerup_immunity = False

# ======================================================================================================================

# ======================================================================================================================
# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Level2()
    window.show()
    app.exec()
# ======================================================================================================================