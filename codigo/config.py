# config.py
import os

from PySide6.QtGui import QFont, QFontDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
fuente_ruta = os.path.join(BASE_DIR, "assets", "fonts", "PixelOperator-Bold.ttf")

def fuente(size=0) -> QFont:
    fuente_id = QFontDatabase.addApplicationFont(fuente_ruta)
    fuente_variantes = QFontDatabase.applicationFontFamilies(fuente_id)
    nombre = fuente_variantes[0] if fuente_variantes else ""
    return QFont(nombre, size)

def fuente_nombre() -> str:
    fuente_id = QFontDatabase.addApplicationFont(fuente_ruta)
    fuente_variantes = QFontDatabase.applicationFontFamilies(fuente_id)
    return fuente_variantes[0] if fuente_variantes else ""