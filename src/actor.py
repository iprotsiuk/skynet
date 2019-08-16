import matplotlib.pyplot as plt

import random
import numpy
from src import hero, minimap_provider, constants, path_planner


class Actor(object):
  def __init__(self):
    self._path_planner = path_planner.PathFinder()
    self._minimap_provider = minimap_provider.MapProvider()
    self._cur_target_square = 0
    self._cur_target_x = -1
    self._cur_target_y = -1

    # Public
    self.black_map = None
    self.hero = hero.Character()
    self.planned_pixel_path = []
    self.planned_directions = []
    self.planned_directions_with_time = []


  def _update_rand_target(self, map):
    self._cur_target_x, self._cur_target_y = self.get_random_target(map)

  def update_plan(self):
    map = self._minimap_provider.get_black_minimap()
    self.black_map = map
    self._update_rand_target(map)

    path = []
    while len(path) == 0:
      path = self._path_planner.find_path(map,
                                          constants.PLAYER_MINIMAP_X,
                                          constants.PLAYER_MINIMAP_Y,
                                          self._cur_target_x, self._cur_target_y)
      if len(path) == 0:
        print("path doesn't exist to the target, reassigning target")
        self._update_rand_target(map)
    self.planned_pixel_path = path
    self.planned_directions = self._path_planner.path_to_directions(path)
    self.planned_directions_with_time = self._path_planner.to_directions_with_time(self.planned_directions)


    # self._debug_print_path(map, path)

  def get_random_target(self, black_minimap : numpy.ndarray) -> (int, int):
    max_row, max_cols = black_minimap.shape
    wall = constants.MINIMAP_WALL

    row = random.randint(1, max_row)
    col = random.randint(1, max_cols)

    # if(random.randint(0,9) == 9):
    #   self._cur_target_square = random.randint(0,1)
    #
    # if self._cur_target_square == 0:
    #   row = random.randint(1, round(max_row/2))
    #   col = random.randint(1, round(max_cols/2))
    # if self._cur_target_square == 1:
    #   row = random.randint(round(max_row/2), max_row)
    #   col = random.randint(round(max_cols/2), max_cols)

    while row == wall or col == wall:
      row = random.randint(1, max_row)
      col = random.randint(1, max_cols)
    return row, col

  def _debug_print_path(self, map, path):
    for x, y in path :
      map[y][x] = 1
    plt.imshow(map)
    plt.show()
