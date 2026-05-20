import os
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect
from src.config.rutas import *


class Sound:
    def __init__(self):
        self.volume_general = 0.5

    def background(self):
        self.musica = QSoundEffect()
        ruta_musica = os.path.join(DIR_MUSIC, "background.wav")
        self.musica.setSource(QUrl.fromLocalFile(ruta_musica))
        self.musica.setVolume(self.volume_general * 0.1)
        self.musica.play()

    def click_button(self):
        self.effect = QSoundEffect()
        ruta_effect = os.path.join(DIR_SOUNDS, "clickButton.wav")
        self.effect.setSource(QUrl.fromLocalFile(ruta_effect))
        self.effect.setVolume(self.volume_general * 0.5)
        self.effect.play()