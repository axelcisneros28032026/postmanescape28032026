import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QSlider, QLabel
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect


class AudioManager:
    def __init__(self):
        # Volúmenes
        self.volumen = {
            "master": 1.0,
            "musica": 0.5,
            "efectos": 0.7
        }

        # === Canal música (1 solo sonido en loop) ===
        self.musica = QSoundEffect()
        self.musica.setSource(QUrl.fromLocalFile("musica.wav"))
        self.musica.setLoopCount(QSoundEffect.Infinite)

        # === Canal efectos (pool) ===
        self.efectos_pool = []
        self.max_efectos = 10

        self.actualizar_volumenes()
        self.musica.play()

    def actualizar_volumenes(self):
        vol_musica = self.volumen["master"] * self.volumen["musica"]
        self.musica.setVolume(vol_musica)

        for efecto in self.efectos_pool:
            vol_fx = self.volumen["master"] * self.volumen["efectos"]
            efecto.setVolume(vol_fx)

    def set_volumen(self, canal, valor):
        self.volumen[canal] = valor
        self.actualizar_volumenes()

    def play_efecto(self, archivo):
        # Reutilizar efectos disponibles
        for efecto in self.efectos_pool:
            if not efecto.isPlaying():
                efecto.setSource(QUrl.fromLocalFile(archivo))
                efecto.play()
                return

        # Crear nuevo si no hay libres
        if len(self.efectos_pool) < self.max_efectos:
            efecto = QSoundEffect()
            efecto.setSource(QUrl.fromLocalFile(archivo))
            self.efectos_pool.append(efecto)
            self.actualizar_volumenes()
            efecto.play()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mixer simple")

        self.audio = AudioManager()

        layout = QVBoxLayout()

        # Música slider
        layout.addWidget(QLabel("Música"))
        self.slider_musica = QSlider(Qt.Horizontal)
        self.slider_musica.setRange(0, 100)
        self.slider_musica.setValue(50)
        self.slider_musica.valueChanged.connect(
            lambda v: self.audio.set_volumen("musica", v / 100)
        )

        # Efectos slider
        layout.addWidget(QLabel("Efectos"))
        self.slider_fx = QSlider(Qt.Horizontal)
        self.slider_fx.setRange(0, 100)
        self.slider_fx.setValue(70)
        self.slider_fx.valueChanged.connect(
            lambda v: self.audio.set_volumen("efectos", v / 100)
        )

        # Botón disparar efecto
        btn_fx = QPushButton("Disparar efecto")
        btn_fx.clicked.connect(
            lambda: self.audio.play_efecto("efecto.wav")
        )

        layout.addWidget(self.slider_musica)
        layout.addWidget(self.slider_fx)
        layout.addWidget(btn_fx)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.resize(300, 200)
    window.show()
    sys.exit(app.exec())