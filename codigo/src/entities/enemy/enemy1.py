import os

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QPainterPath
from PySide6.QtWidgets import QGraphicsPixmapItem

from src.config.rutas import DIR_IMAGES


class Enemy(QGraphicsPixmapItem):
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
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "walk", "down", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "walk", "down", "2.png"),
            ],
            "right": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "walk", "right", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "walk", "right", "2.png"),
            ],
            "jump_up": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "jump", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "jump", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "jump", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "jump", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "jump", "up", "5.png"),
            ],
            "climb_up": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "6.png"),
            ],
            "climb_down": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "1.png"),
            ],
            "up": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "1.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "6.png"),
            ],
            "down": [
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "6.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "5.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "4.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "3.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "2.png"),
                os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "1.png"),
            ],
            "idle": {
                "left": os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "idle", "down", "1.png"),
                "right": os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "idle", "right", "1.png"),
                "up": os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "idle", "up", "1.png"),
                "down": os.path.join(DIR_IMAGES, "sprites", "enemy", "standard", "climb", "up", "6.png"),
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
        else:
            self.last_direction = direction
            frames = self.frames[direction]

            # Avanzar frame cada N ticks
            if self.last_direction == "jump_up":
                for i in range(5):
                    self._anim_counter += 1
                    if self._anim_counter >= self._anim_speed:
                        self._anim_counter = 0
                        self._frame_index = (self._frame_index + 1) % len(frames)
            else:
                self._anim_counter += 1
            if self._anim_counter >= self._anim_speed:
                self._anim_counter = 0
                self._frame_index = (self._frame_index + 1) % len(frames)

            frame = frames[self._frame_index]

        self.setPixmap(QPixmap(frame))

    def boundingRect(self):
        rect = self.pixmap().rect()

        # Ajuste de bordes a partir del área original
        border_left = 16
        border_right = -16
        border_top = -8
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
