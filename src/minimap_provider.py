import time

import PIL
import cv2 as cv
import numpy
import numpy as np
import pyautogui


from src import constants
from src.constants import Constants

# import draw_image

MINIMAP_X_SIZE = Constants.MINIMAP_COLUMNS
MINIMAP_Y_SIZE = Constants.MINIMAP_ROWS



class MapProvider(object):
  def __init__(self):
    windowLocation = pyautogui.locateOnScreen('data/teleport_icon.png')
    if windowLocation is None:
      print("teleport_icon wasn't found, wait a bit longer")
      time.sleep(2)
      windowLocation = pyautogui.locateOnScreen('data/teleport_icon.png')

    if windowLocation is not None:
      self.minimap_col = windowLocation.left + 280 - 2
      self.minimap_row = windowLocation.top - 416 - MINIMAP_Y_SIZE - 3
    else:
      print("teleport_icon wasn't found, abort now!")
    self.first_town_template = cv.imread('data/town.png', 0)
    self.last_town_template = cv.imread('data/last_town.png', 0)
    self.enemy_template = cv.imread('data/red_enemy.png', 0)
    self.player_template = cv.imread('data/player.png', 0)
    self.map_selector_template = cv.imread('data/map_selector.png', 0)

  def get_minimap(self) -> PIL.Image.Image:
    # Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details)
    ts = time.time()
    img = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    print('taking screenshot get_minimap, time_sec=', round(time.time() - ts, 4))
    return img

  @staticmethod
  def get_black_minimap(img) -> numpy.ndarray:
    # Load image and convert to greyscale
    img = np.asarray(img)
    img = MapProvider.remove_creatures_from_map(img)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # debug_utils.draw_image(img_gray)

    # Pixels higher than this will be 1. Otherwise 0.
    black_picture = (img_gray > Constants.BLACK_THRESHOLD_VALUE)
    # debug_utils.draw_image(black_picture)

    # Remove character from the map
    # black_picture[PLAYER_ROW - PLAYER_HEIGHT:PLAYER_ROW + PLAYER_HEIGHT,
    # PLAYER_COL - PLAYER_WIDTH:PLAYER_COL + PLAYER_WIDTH].fill(0)

    return black_picture

  # Add 1 pixel below every black
  @staticmethod
  def get_black_minimap_bold(original_map) -> numpy.ndarray:
    max_row, max_col = original_map.shape
    bold_map = np.copy(original_map)

    for row in range(max_row):
      for col in range(max_col):
        if original_map[row][col] == 1 and row < max_row - 3:
          bold_map[row + 1][col] = 1
          bold_map[row + 2][col] = 1
          bold_map[row + 3][col] = 1
        if original_map[row][col] == 1 and col < max_col - 1:
          bold_map[row][col + 1] = 1

    return bold_map

  def locate_enemies(self) -> (list, list):
    img_rgb = self.get_minimap()
    img_rgb = np.array(img_rgb)
    img_rgb = self.map_to_red(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.enemy_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res >= threshold)
    return loc

  def is_in_town(self) -> bool:
    ts = time.time()
    img_rgb = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row - 51, MINIMAP_X_SIZE, 51))
    #print('taking screenshot is_in_town, time_sec=', round(time.time() - ts, 4))
    img_rgb = np.array(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res_first_town = cv.matchTemplate(img_gray, self.first_town_template, cv.TM_CCOEFF_NORMED)
    res_last_town = cv.matchTemplate(img_gray, self.last_town_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc_first_town = np.where(res_first_town >= threshold)
    loc_last_town = np.where(res_last_town >= threshold)
    if len(loc_last_town[0]) != 0 or len(loc_first_town[0] != 0):
      return True
    return False

  def locate_player(self, img_rgb) -> (list, list):
    img_rgb = np.array(img_rgb)
    img_rgb = self.filter_player(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.player_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.945
    loc = np.where(res >= threshold)

    rows, columns = loc
    if rows.any() and columns.any():
      return rows[0], columns[0] + 2
    return Constants.PLAYER_MINIMAP_ROW, Constants.PLAYER_MINIMAP_COLUMN

  @staticmethod
  def map_to_red(map: np.array):

    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 220, 100])
    upper_red = np.array([255, 230, 255])

    # lower_red = np.array([0,50,180])
    # upper_red = np.array([255,255,255])

    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map, map, mask=mask)

    # cv.imshow('hsv',hsv)
    # cv.imshow('img_rgb',map)
    # cv.imshow('mask',mask)
    # cv.imshow('res',res)
    # cv.waitKey(0)
    return res

  @staticmethod
  def filter_player(map: np.array):

    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)
    lower_red = np.array([0, 0, 0])
    upper_red = np.array([255, 135, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map, map, mask=mask)

    # cv.imshow('hsv',hsv)
    # cv.imshow('img_rgb',map)
    # cv.imshow('mask',mask)
    # cv.imshow('res',res)
    # cv.waitKey(0)
    return res

  def is_in_map_selector(self) -> bool:
    ts = time.time()
    img_rgb = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    #print4('taking screenshot is_in_map_selector, time_sec=', round(time.time() - ts, 4))
    img_rgb = np.array(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.map_selector_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
      return False
    return True

  @staticmethod
  def remove_creatures_from_map(map: np.array):
    map = MapProvider.remove_player_from_map(map)
    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 0])
    upper_red = np.array([80, 220, 220])

    # lower_red = np.array([0,0,0])
    # upper_red = np.array([80,220,220])

    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map, map, mask=mask)
    return res

  @staticmethod
  def remove_player_from_map(map: np.array):
    hsv = cv.cvtColor(map, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 135, 0])
    upper_red = np.array([255, 255, 255])

    mask = cv.inRange(hsv, lower_red, upper_red)
    res = cv.bitwise_and(map, map, mask=mask)
    return res
