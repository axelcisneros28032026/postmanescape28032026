import os
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QPainterPath
from PySide6.QtCore import QRectF
from src.config.rutas import DIR_TILES


class Platforms(QGraphicsPixmapItem):

    def __init__(self):
        super().__init__()

        # Asignar sprite de la plataforma
        self.setPixmap(
            QPixmap(
                os.path.join(DIR_TILES, "plataform_1A.png")
            )
        )
        self.border_left = 0
        self.border_right = 0
        self.border_top = -48
        self.border_bottom = 0

        self.border2_left = 0
        self.border2_right = 0
        self.border2_top = -48 + 8
        self.border2_bottom = -16

        self.border3_left = -64
        self.border3_right = -self.pixmap().width()
        self.border3_top = 16
        self.border3_bottom = -16

        self.rect = self.pixmap().rect()

    def boundingRect(self):
        return QRectF(
            self.rect.left() + self.border_left,
            self.rect.top() - self.border_top,
            self.rect.width() - self.border_left + self.border_right,
            self.rect.height() + self.border_top + self.border_bottom
        )

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def area1(self):
        return QRectF(
            self.rect.left() + self.border2_left,
            self.rect.top() - self.border2_top,
            self.rect.width() - self.border2_left + self.border2_right,
            self.rect.height() + self.border2_top + self.border2_bottom
        )

