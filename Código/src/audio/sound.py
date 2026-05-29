import os
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect
from src.config.rutas import *


class Sound:
    def __init__(self):
        self.volume_general = 1

    def background(self):
        self.musica = QSoundEffect()
        ruta_musica = os.path.join(DIR_MUSIC, "background.wav")
        self.musica.setSource(QUrl.fromLocalFile(ruta_musica))
        self.musica.setVolume(self.volume_general * 0.25)
        self.musica.play()

    def click_button(self):
        self.effect = QSoundEffect()
        ruta_effect = os.path.join(DIR_SOUNDS, "click_button.wav")
        self.effect.setSource(QUrl.fromLocalFile(ruta_effect))
        self.effect.setVolume(self.volume_general * 0.5)
        self.effect.play()

    def money_pickup(self):
        self.effect = QSoundEffect()
        ruta_effect = os.path.join(DIR_SOUNDS, "money_pickup.wav")
        self.effect.setSource(QUrl.fromLocalFile(ruta_effect))
        self.effect.setVolume(self.volume_general * 0.5)
        self.effect.play()

    def throw_bone(self):
        self.effect = QSoundEffect()
        ruta_effect = os.path.join(DIR_SOUNDS, "throw_bone.wav")
        self.effect.setSource(QUrl.fromLocalFile(ruta_effect))
        self.effect.setVolume(self.volume_general * 0.5)
        self.effect.play()

    def aim(self):
        self.effect = QSoundEffect()
        ruta_effect = os.path.join(DIR_SOUNDS, "aim.wav")
        self.effect.setSource(QUrl.fromLocalFile(ruta_effect))
        self.effect.setVolume(self.volume_general * 1)
        self.effect.play()