from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QPainterPath
import os

from src.config.rutas import DIR_IMAGES


class Coins(QGraphicsPixmapItem):

    def __init__(self):
        super().__init__()

        self.setPixmap(
            QPixmap(
                os.path.join(
                    DIR_IMAGES,
                    "sprites",
                    "coin",
                    "1.png"
                )
            )
        )

    def boundingRect(self):
        rect = self.pixmap().rect()

        # Ajuste de bordes a partir del área original
        border_left = 16
        border_right = -16
        border_top = -16
        border_bottom = -16

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