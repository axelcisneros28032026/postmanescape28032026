import os

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QPainterPath
from PySide6.QtWidgets import QGraphicsPixmapItem

from src.config.rutas import DIR_IMAGES


class Bones(QGraphicsPixmapItem):

    def __init__(self, speed=1, anim_speed=16):
        super().__init__()

        self.current_direction = "idle"
        self.direction = "idle"
        self.last_direction = "down"

        self.speed = speed

        self._frame_index = 0
        self._anim_counter = 0
        self._anim_speed = anim_speed

        self.frames = {
            "left": [
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0002.png"),
            ],
            "right": [
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0002.png"),
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
            ],
            "up": [
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0002.png"),
            ],
            "down": [
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0002.png"),
            ],
            "idle": {
                "left": os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                "right": os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                "up": os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png"),
                "down": os.path.join(DIR_IMAGES, "sprites", "bones", "Sprite-0001.png")
            }
        }

        self.setPixmap(
            QPixmap(self.frames["idle"]["down"])
        )

    def mover(self):

        if self.direction == "left":
            self.setX(self.x() - self.speed)

        elif self.direction == "right":
            self.setX(self.x() + self.speed)

        elif self.direction == "up":
            self.setY(self.y() - self.speed)

        elif self.direction == "down":
            self.setY(self.y() + self.speed)

    def set_direction(self, direction):

        if direction != self.current_direction:
            self._frame_index = 0
            self._anim_counter = 0

        self.current_direction = direction

        if direction == "idle":

            frame = self.frames["idle"].get(
                self.last_direction,
                self.frames["idle"]["down"]
            )

        else:

            self.last_direction = direction
            frames = self.frames[direction]

            self._anim_counter += 1

            if self._anim_counter >= self._anim_speed:
                self._anim_counter = 0
                self._frame_index = (
                    self._frame_index + 1
                ) % len(frames)

            frame = frames[self._frame_index]

        self.setPixmap(QPixmap(frame))

    def boundingRect(self):

        rect = self.pixmap().rect()

        border_left = 24
        border_right = -24
        border_top = -24
        border_bottom = -24

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