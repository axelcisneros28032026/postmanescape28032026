import os
from pathlib import Path

DIR_BASE = Path(__file__).resolve().parents[2]

#   - Carpetas principales
#       Assets
DIR_ASSETS = os.path.join(DIR_BASE, "assets")
#       Scenes
DIR_SCENES = os.path.join(DIR_BASE, "scenes")
#       Src
DIR_SRC = os.path.join(DIR_BASE, "src")
#   - Rutas frecuentes
#       Assets
#           Fonts
DIR_FONTS = os.path.join(DIR_ASSETS, "fonts")
#           Icons
DIR_ICONS = os.path.join(DIR_ASSETS, "icons")
#               Icono del programa
APP_ICON = os.path.join(DIR_BASE, "assets", "icons", "appIcon.ico")
APP_ICON_PNG = os.path.join(DIR_BASE, "assets", "icons", "appIcon.png")
#           Images
DIR_IMAGES = os.path.join(DIR_ASSETS, "images")
#           Music
DIR_MUSIC = os.path.join(DIR_ASSETS, "music")
#           Sounds
DIR_SOUNDS = os.path.join(DIR_ASSETS, "sounds")
#           Tiles
DIR_TILES = os.path.join(DIR_ASSETS, "tiles")
