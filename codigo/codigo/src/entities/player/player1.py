import os

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QPainterPath
from PySide6.QtWidgets import QGraphicsPixmapItem

from src.config.rutas import DIR_IMAGES


class Player(QGraphicsPixmapItem):
    def __init__(self, speed = 1, anim_speed = 16):
        super().__init__()

        self.current_direction = "idle"
        self.direction = "idle"
        self.last_direction = "idle"
        self.speed = speed

        self._frame_index = 0
        self._anim_counter = 0
        self._anim_speed = anim_speed

        self.frames = {
            "left": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "walk", "down", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "walk", "down", "2.png"),
            ],
            "right": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "walk", "right", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "walk", "right", "2.png"),
            ],
            "run_left": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "7.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "down", "8.png"),
            ],
            "run_right": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "7.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "run", "right", "8.png"),
            ],
            "jump_up": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "5.png"),
            ],
            "jump_left": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "5.png"),
            ],
            "jump_right": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "5.png"),
            ],
            "climb_up": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "6.png"),
            ],
            "climb_down": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "1.png"),
            ],
            "up": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "6.png"),
            ],
            "down": [
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "1.png"),
            ],
            "idle": {
                "left": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "idle", "down", "1.png"),
                "right": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "idle", "right", "1.png"),
                "up": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "idle", "up", "1.png"),
                "down": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "climb", "up", "6.png"),
                "jump_up": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "up", "1.png"),
                "jump_left": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "down", "1.png"),
                "jump_right": os.path.join(DIR_IMAGES, "sprites", "player", "standard", "jump", "right", "1.png"),
            }
        }

        self.setPixmap(QPixmap(self.frames["idle"]["right"]))

    def mover(self):
        if self.direction == "left":
            self.setX(self.x() - self.speed)
        elif self.direction == "right":
            self.setX(self.x() + self.speed)
        elif self.direction == "jump_up":
            self.setY(self.y() - self.speed)
        elif self.direction == "up":
            self.setY(self.y() - 3 / self.speed)
        elif self.direction == "down":
            self.setY(self.y() + 3 / self.speed)

    def set_direction(self, direction):
        # Si cambió de dirección, reinicia la animación
        if direction != self.current_direction:
            self._frame_index = 0
            self._anim_counter = 0

        self.current_direction = direction

        if direction == "idle":
            frame = self.frames["idle"].get(self.last_direction, self.frames["idle"]["right"])
        elif direction == "jump_up":
            self.last_direction = direction
            frames = self.frames[direction]

            # Avanzar frame cada N ticks
            self._anim_counter += 0.25
            if self._anim_counter >= self._anim_speed:
                self._anim_counter = 0
                self._frame_index = (self._frame_index + 1) % len(frames)

            frame = frames[self._frame_index]
        else:
            self.last_direction = direction
            frames = self.frames[direction]

            # Avanzar frame cada N ticks
            self._anim_counter += 1
            if self._anim_counter >= self._anim_speed:
                self._anim_counter = 0
                self._frame_index = (self._frame_index + 1) % len(frames)

            frame = frames[self._frame_index]

        self.setPixmap(QPixmap(frame))

    def set_frame(self, frame: int):
        try:
            # Intenta con _animations
            animations = getattr(self, "_animations", None)
            # Si no existe, busca otros nombres comunes
            if animations is None:
                animations = getattr(self, "animations", None)
            if animations is None:
                animations = getattr(self, "_frames", None)
            if animations is None:
                animations = getattr(self, "frames", None)

            if animations is None:
                return  # No se encontró ningún dict de animaciones, salir sin error

            direction = getattr(self, "current_direction", None)
            if direction is None:
                return

            frames = animations.get(direction, [])
            if frames and 0 <= frame < len(frames):
                self.setPixmap(frames[frame])
        except Exception:
            pass  # Silencia cualquier error inesperado

    def boundingRect(self):
        rect = self.pixmap().rect()

        # Ajuste de bordes a partir del área original
        border_left = 16
        border_right = -16
        border_top = -16
        border_bottom = 0

        return QRectF(
            rect.left() + border_left,
            rect.top() - border_top,
            rect.width() - border_left + border_right,
            rect.height() + border_top + border_bottom
        )

    def shape(self):

        path = QPainterPath()

        path.addRect(self.boundingRect())

        return path
