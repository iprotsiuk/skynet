import random

import matplotlib.pyplot as plt
import numpy as np

from src import hero, minimap_provider, constants, path_planner


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
    self.iteration=0

  def _update_target(self, map):
    col_row = self.get_enemy_target()
    if col_row and self.iteration % 5 != 0:
      print("Enemy detected!")
      self.target_row, self.target_col = col_row[1], col_row[0]
    else:
      self.target_row, self.target_col = self.get_random_target(map)

  def update_plan(self):
    self.iteration+=1
    map = self._minimap_provider.get_black_minimap_bold(self._minimap_provider.get_black_minimap())
    self.black_map = map
    self._update_target(map)
    self.is_in_town = self._minimap_provider.is_in_town()
    self.is_in_map_selector = self._minimap_provider.is_in_map_selector()

    if self.is_in_town or self.is_in_map_selector:
      return

    path = []
    while len(path) == 0:
      path = self._path_planner.find_path(map,
                                          constants.PLAYER_MINIMAP_COLUMN,
                                          constants.PLAYER_MINIMAP_ROW,
                                          self.target_col, self.target_row)
      attempts = 0
      if len(path) == 0 and attempts < 10:
        attempts += 1
        print("path doesn't exist to the target, reassigning target")
        self._update_target(map)
    self.planned_pixel_path = path
    self.planned_directions = self._path_planner.path_to_directions(path)
    self.planned_directions_with_time = self._path_planner.to_directions_with_time(self.planned_directions)

  def get_random_target(self, black_minimap: np.ndarray) -> (int, int):
    max_row, max_cols = black_minimap.shape
    wall = constants.MINIMAP_WALL

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
