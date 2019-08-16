import time
import numpy
import numpy as np
import PIL
import pyautogui as p
from src import constants

MINIMAP_Y_SIZE = constants.MINIMAP_Y_SIZE
MINIMAP_X_SIZE = constants.MINIMAP_X_SIZE
PLAYER_Y = constants.PLAYER_MINIMAP_Y
PLAYER_X = constants.PLAYER_MINIMAP_X
BLACK_THRESHOLD_VALUE = 40
PLAYER_RADIUS = 5


class MapProvider:
  def __init__(self):
    time.sleep(2)
    windowLocation = p.locateOnScreen('data/teleport_icon.png')
    if windowLocation is None:
      time.sleep(1)
    self._x = windowLocation.left + 280
    self._y = windowLocation.top - 416 - MINIMAP_Y_SIZE

  def get_minimap(self) -> PIL.Image.Image:
    return p.screenshot('data/minimap.png', region=(self._x, self._y, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    # Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details)

  def get_black_minimap(self) -> numpy.ndarray:
    # Load image and convert to greyscale
    img = self.get_minimap().convert("L")

    img_data = np.asarray(img)
    # Pixels higher than this will be 1. Otherwise 0.
    black_picture = (img_data > BLACK_THRESHOLD_VALUE)

    # Remove character from the map
    black_picture[PLAYER_Y - PLAYER_RADIUS:PLAYER_Y + PLAYER_RADIUS,
    PLAYER_X - PLAYER_RADIUS:PLAYER_X + PLAYER_RADIUS].fill(0)

    return black_picture