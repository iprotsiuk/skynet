import time

import PIL
import cv2 as cv
import numpy
import numpy as np
import pyautogui

from src import constants

MINIMAP_X_SIZE = constants.MINIMAP_COLUMNS
MINIMAP_Y_SIZE = constants.MINIMAP_ROWS
PLAYER_X = constants.PLAYER_MINIMAP_COLUMN
PLAYER_Y = constants.PLAYER_MINIMAP_ROW
BLACK_THRESHOLD_VALUE = 40
PLAYER_RADIUS = 5


class MapProvider:
  def __init__(self):
    time.sleep(2)
    windowLocation = pyautogui.locateOnScreen('data/teleport_icon.png')
    if windowLocation is None:
      print("teleport_icon wasn't found, wait a bit longer")
      time.sleep(2)
    self.minimap_col = windowLocation.left + 280
    self.minimap_row = windowLocation.top - 416 - MINIMAP_Y_SIZE
    self.town_template = cv.imread('data/town.png', 0)

  def get_minimap(self) -> PIL.Image.Image:
    print("Taking a picture of minimap area ")
    return pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
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

  # Add 1 pixel below every black
  def get_black_minimap_bold(self) -> numpy.ndarray:
    original_map = self.get_black_minimap()
    max_row, max_col = original_map.shape
    bold_map = np.copy(original_map)

    for row in range(max_row):
      for col in range(max_col):
        if original_map[row][col] == 1 and row < max_row - 1:
          bold_map[row + 1][col] = 1

    return bold_map

  def is_in_town(self) -> bool:
    img_rgb = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row - 51, MINIMAP_X_SIZE, 51))
    img_rgb = np.array(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.town_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
      return False
    return True
