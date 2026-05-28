import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFontMetrics, Qt, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QHBoxLayout, QPushButton


class NavigationMenu(QWidget):

    signalOpcionElegida = Signal(int)

    def __init__(self,
                 opciones,  # Lista de opciones (str)
                 indicador = None,  # Carácter que indica la opción activa (str)
                 indiceInicial = 0,  # Índice donde inicia la navegación (int)

                 estiloIndicador = "",  # Hojas de estilo (setStyleSheet) del indicador (str)
                 fuenteIndicador = None,  # Fuente de texto del indicador (str)
                 sizeFuenteIndicador = None,  # Tamaño de fuente de texto del indicador (int)

                 estiloOpcion = "",  # Hojas de estilo (setStyleSheet) de las opciones (str)
                 fuenteOpcion = None,  # Fuente de texto de las opciones (int)
                 sizeFuenteOpcion = None,  # Tamaño de fuente de texto de las opciones (int)

                 autoajustar: bool = False, # Autoajustar tamaño de indicador y opciones (bool)

                 anchoIndicador = 0,    # Ajustar ancho del indicador
                 anchoOpciones = 0
                 ):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

        self.opciones = opciones
        self.indicador = indicador
        self.indiceInicial = indiceInicial
        self.estiloIndicador = estiloIndicador
        self.estiloOpcion = estiloOpcion
        self.anchoIndicador = anchoIndicador

        self.indiceActual = indiceInicial

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout = []
        self.label = []
        self.pushButton = []

        self.indiceMaximo  = int(len(opciones) - 1)
        n = 0

        for opcion in opciones:
            hBoxLayouts = QHBoxLayout()

            if n == indiceInicial:
                labels = QLabel(indicador)
            else:
                labels = QLabel()
            labels.setStyleSheet(self.estiloIndicador)

            margenIndicador = QFontMetrics(QFont(fuenteIndicador, sizeFuenteIndicador) if fuenteIndicador else
                                           self.font()).horizontalAdvance(indicador) + self.anchoIndicador

            if autoajustar or self.anchoIndicador != 0:
                labels.setFixedWidth(margenIndicador)

            buttons = QPushButton(opcion)

            buttons.setFocusPolicy(Qt.NoFocus)
            try:
                buttons.setStyleSheet(self.estiloOpcion)
            except:
                pass
            try:
                buttons.setFont(QFont(fuenteOpcion, sizeFuenteOpcion))
            except:
                pass
            try:
                labels.setFont(QFont(fuenteIndicador, sizeFuenteIndicador))
            except:
                pass

            n += 1

            if indicador:
                hBoxLayouts.addWidget(labels)
            hBoxLayouts.addWidget(buttons)

            if autoajustar:
                hBoxLayouts.insertStretch(0)
                hBoxLayouts.insertStretch(3)

            self.hBoxLayout.append(hBoxLayouts)
            self.label.append(labels)
            self.pushButton.append(buttons)

            self.layout.addLayout(hBoxLayouts)

        anchoMaximo = max(button.sizeHint().width() for button in self.pushButton)

        for buttons in self.pushButton:
            buttons.setFixedWidth(anchoMaximo)

    # Eventos y Métodos

    def navegacion(self):
        if self.indiceActual > self.indiceMaximo:
            self.indiceActual = 0
        elif self.indiceActual < 0:
            self.indiceActual = self.indiceMaximo

        for i, label in enumerate(self.label):
            if i == self.indiceActual:
                label.setText(self.indicador)
            else:
                label.clear()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.indiceActual -= 1
            self.navegacion()

        elif event.key() == Qt.Key.Key_Down:
            self.indiceActual += 1
            self.navegacion()

        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.signalOpcionElegida_emitir(self.indiceActual)

        else:
            super().keyPressEvent(event)

    def signalOpcionElegida_emitir(self, indiceActual):
        self.signalOpcionElegida.emit(indiceActual)


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.navigationMenu = NavigationMenu(
            ["1", "Opción 2", "3"],
            "*",
            0,
            "color: red;",
            "Sans Serif",
            24,
            "color: blue;",
            "Sans Serif",
            24,
            True,
            0,
            0
        )

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.navigationMenu)


# Ejecución
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Demo()
    ventana.show()
    app.exec()