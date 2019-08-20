import time

import PIL
from PIL import ImageGrab
import cv2 as cv
import numpy
import numpy as np
import pyautogui

from src.constants import Constants

# import draw_image

MINIMAP_X_SIZE = Constants.MINIMAP_COLUMNS
MINIMAP_Y_SIZE = Constants.MINIMAP_ROWS
WINDOW_COLUMNS_SIZE = Constants.WINDOW_COLUMNS
WINDOW_ROWS_SIZE = Constants.WINDOW_ROWS
MINIMAP_COLS_LOCATION = Constants.MIMIMAP_LOCATION_COLS
MINIMAP_ROWS_LOCATION = Constants.MIMIMAP_LOCATION_ROWS


class MapProvider(object):
  def __init__(self):
    teleport_location = pyautogui.locateOnScreen('data/teleport_icon.png')
    if teleport_location is None:
      print("teleport_icon wasn't found, wait a bit longer")
      time.sleep(2)
      teleport_location = pyautogui.locateOnScreen('data/teleport_icon.png')

    if teleport_location is not None:
      self.window_location_col = teleport_location.left - 766
      self.window_location_row = teleport_location.top - 660
    else:
      print("teleport_icon wasn't found, abort now!")

    self.first_town_template = cv.imread('data/town.png', 0)
    self.last_town_template = cv.imread('data/last_town.png', 0)
    self.enemy_template = cv.imread('data/red_enemy.png', 0)
    self.player_template = cv.imread('data/player.png', 0)
    self.map_selector_template = cv.imread('data/map_selector.png', 0)
    #########################
    self.game_window_image = PIL.Image.Image()
    self.minimap_image = PIL.Image.Image()
    self.is_in_town_image = PIL.Image.Image()
    self.is_in_map_selector_image = PIL.Image.Image()
    #########################

  def get_minimap(self) -> PIL.Image.Image:
    return self.minimap_image

  @staticmethod
  def get_black_minimap(map_np_array) -> numpy.ndarray:
    # Load image and convert to greyscale
    map_np_array = MapProvider.remove_creatures_from_map(map_np_array)
    img_gray = cv.cvtColor(map_np_array, cv.COLOR_BGR2GRAY)
    black_picture = (img_gray > Constants.BLACK_THRESHOLD_VALUE)
    return black_picture

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
    img_rgb = self.minimap_np_array
    img_rgb = self.map_to_red(img_rgb)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.enemy_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res >= threshold)
    return loc

  def is_in_town(self) -> bool:
    img_rgb = self.is_in_town_image
    # print('taking screenshot is_in_town, time_sec=', round(time.time() - ts, 4))
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
    # img_rgb = pyautogui.screenshot(region=(self.minimap_col, self.minimap_row, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
    # print4('taking screenshot is_in_map_selector, time_sec=', round(time.time() - ts, 4))
    img_gray = cv.cvtColor(self.minimap_np_array, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, self.map_selector_template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
      return False
    return True

  def update_maps(self):
    # make a screenshot of game window
    game_window_image = ImageGrab.grab((self.window_location_col, self.window_location_row,
                                        self.window_location_col + WINDOW_COLUMNS_SIZE,
                                        self.window_location_row + WINDOW_ROWS_SIZE))
    self.minimap_image = self.crop_minimap_image(game_window_image).crop().convert('RGB')
    self.is_in_town_image = self.crop_is_in_town_image(game_window_image).crop().convert('RGB')
    self.minimap_np_array = np.array(self.minimap_image)

    # .save("out/capture.png", "PNG")
    return True

  @staticmethod
  def crop_minimap_image(game_window_image) -> PIL.Image.Image:
    minimap = game_window_image.crop((MINIMAP_COLS_LOCATION, MINIMAP_ROWS_LOCATION,
                                      MINIMAP_COLS_LOCATION + MINIMAP_X_SIZE, MINIMAP_ROWS_LOCATION + MINIMAP_Y_SIZE))
    return minimap

  @staticmethod
  def crop_is_in_town_image(game_window_image) -> PIL.Image.Image:
    is_in_town_image = game_window_image.crop(
      (MINIMAP_COLS_LOCATION, MINIMAP_ROWS_LOCATION - 51, MINIMAP_COLS_LOCATION + MINIMAP_X_SIZE, 51))
    return is_in_town_image

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
