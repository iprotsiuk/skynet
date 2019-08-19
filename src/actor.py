import random

import matplotlib.pyplot as plt
import numpy as np

from src import hero, minimap_provider, path_planner
from src.constants import Constants


class Actor(object):
  def __init__(self):
    self._path_planner = path_planner.PathFinder()
    self._minimap_provider = minimap_provider.MapProvider()
    self.target_col = -1
    self.target_row = -1

    # Public
    self.black_map = None
    self.hero = hero.Character()
    self.planned_pixel_path = []
    self.planned_directions = []
    self.planned_directions_with_time = []
    self.is_in_town = True
    self.is_in_map_selector = True
    self.iteration = 0

  def update_target(self, map):
    row_and_column = self.get_enemy_target()
    if row_and_column and self.iteration % 5 != 0:
      self.target_row, self.target_col = row_and_column[1], row_and_column[0]
      print("Target enemy:", self.target_row, self.target_col)
    else:
      self.target_row, self.target_col = self.get_random_target(map)
      print("Target random:", self.target_row, self.target_col)

  def update_plan(self):
    self.iteration += 1
    map_img = self._minimap_provider.get_minimap()
    map = self._minimap_provider.get_black_minimap_bold(self._minimap_provider.get_black_minimap(map_img))
    self.black_map = map
    self.update_target(map)
    self.is_in_town = self._minimap_provider.is_in_town()
    self.is_in_map_selector = self._minimap_provider.is_in_map_selector()

    if self.is_in_town or self.is_in_map_selector:
      return

    path = []
    path_attempts = 0
    while len(path) == 0 and path_attempts < 10:
      player_row, player_column = self._minimap_provider.locate_player(map_img)
      path = self._path_planner.find_path(map,
                                          player_column,
                                          player_row,
                                          self.target_col, self.target_row)

      if len(path) == 0 and path_attempts < 10:
        path_attempts += 1
        print("path doesn't exist to the target, reassigning target")
        self.update_target(map)
    self.planned_pixel_path = path
    self.planned_directions = self._path_planner.path_to_directions(path)
    self.planned_directions_with_time = self._path_planner.to_directions_with_time(self.planned_directions)

  def get_random_target(self, black_minimap: np.ndarray) -> (int, int):
    max_row, max_cols = black_minimap.shape
    wall = Constants.MINIMAP_WALL

    row = random.randint(1, max_row)
    col = random.randint(1, max_cols)

    while row == wall or col == wall:
      row = random.randint(1, max_row)
      col = random.randint(1, max_cols)
    return row, col

  def get_enemy_target(self) -> (int, int):
    rows, columns = self._minimap_provider.locate_enemies()
    if rows.any() and columns.any():
      return rows[0], columns[0]
    return None

  def _debug_print_path(self, map, path):
    for x, y in path:
      map[y][x] = 1
    plt.imshow(map)
    plt.show()
