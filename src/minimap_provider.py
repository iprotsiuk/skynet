import time

import PIL
import cv2 as cv
import numpy
import numpy as np
import pyautogui

from src import constants, debug_utils
from src.constants import BLACK_THRESHOLD_VALUE, PLAYER_HEIGHT, PLAYER_WIDTH

MINIMAP_X_SIZE = constants.MINIMAP_COLUMNS
MINIMAP_Y_SIZE = constants.MINIMAP_ROWS
PLAYER_COL = constants.PLAYER_MINIMAP_COLUMN
PLAYER_ROW = constants.PLAYER_MINIMAP_ROW


class MapProvider:

  def __init__(self):
    windowLocation = pyautogui.locateOnScreen('data/teleport_icon.png')
    if windowLocation is None:
      print("teleport_icon wasn't found, wait a bit longer")
      time.sleep(2)
      windowLocation = pyautogui.locateOnScreen('data/teleport_icon.png')
    self.minimap_col = windowLocation.left + 280
    self.minimap_row = windowLocation.top - 416 - MINIMAP_Y_SIZE
    self.town_template = cv.imread('data/town.png', 0)
    self.enemy_template = cv.imread('data/red_enemy.png', 0)
    self.map_selector_template = cv.imread('data/map_selector.png', 0)

  def get_minimap(self) -> PIL.Image.Image:
    print("Taking a picture of minimap area ")
    return pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    # Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details)

  def get_black_minimap(self) -> numpy.ndarray:
    # Load image and convert to greyscale
    img = self.get_minimap()
    img_data = np.asarray(img)
    img_data = self.remove_enemies_from_map(img_data)
    img_gray = cv.cvtColor(img_data, cv.COLOR_BGR2GRAY)
    # debug_utils.draw_image(img_gray)

    # Pixels higher than this will be 1. Otherwise 0.
    black_picture = (img_gray > BLACK_THRESHOLD_VALUE)
    # debug_utils.draw_image(black_picture)

    # Remove character from the map
    black_picture[PLAYER_ROW - PLAYER_HEIGHT:PLAYER_ROW + PLAYER_HEIGHT,
    PLAYER_COL - PLAYER_WIDTH:PLAYER_COL + PLAYER_WIDTH].fill(0)

    return black_picture

  # Add 1 pixel below every black
  def get_black_minimap_bold(self, original_map) -> numpy.ndarray:
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

  def locate_enemies(self) -> (list, list):
    img_rgb = self.get_minimap()
    img_rgb = np.array(img_rgb)
    img_rgb = self.map_to_red(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray,self.enemy_template,cv.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where( res >= threshold)
    return loc

  def map_to_red(self, map):

    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)

    lower_red = np.array([0,220,100])
    upper_red = np.array([255,230,255])

    # lower_red = np.array([0,50,180])
    # upper_red = np.array([255,255,255])

    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map,map, mask= mask)

    # cv.imshow('hsv',hsv)
    # cv.imshow('img_rgb',map)
    # cv.imshow('mask',mask)
    # cv.imshow('res',res)
    # cv.waitKey(0)
    return res

  def is_in_map_selector(self) -> bool:
    img_rgb = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    img_rgb = np.array(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.map_selector_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
      return False
    return True

  def remove_enemies_from_map(self, map : np.array):
    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)

    lower_red = np.array([0,0,0])
    upper_red = np.array([80,220,220])

    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map,map, mask= mask)
    return res
