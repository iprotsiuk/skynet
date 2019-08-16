import collections
from typing import Dict, Tuple, List

import numpy

from src import enums, constants


class PathFinder(object):
  def __init__(self):
    # Empty Constructor
    pass

  def find_path(self, black_minimap: numpy.ndarray, start_col: int, start_row: int, goal_col: int, goal_row: int) -> \
      List[
        enums.Direction]:
    path = self._bfs(black_minimap, 1, start_col, start_row, goal_col, goal_row)
    if path is None:
      return []
    return path

  def _bfs(self, grid: numpy.ndarray, wall_value: int, start_col: int, start_row: int, goal_col: int, goal_row: int):
    rows, cols = grid.shape
    to_visit = collections.deque()
    to_visit.append((start_col, start_row))
    seen = set()
    to_A_came_from = {}

    while to_visit:
      (col, row) = to_visit.popleft()
      seen.add((col, row))
      if (col, row) == (goal_col, goal_row):
        return self._build_coord_path(to_A_came_from=to_A_came_from, start_col=start_col, start_row=start_row,
                                      cur_col=col, cur_row=row)
      for col_2, row_2 in (
          (col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1), (col - 1, row - 1), (col - 1, row + 1),
          (col + 1, row - 1),
          (col + 1, row + 1)):
        if 0 <= col_2 < cols \
            and 0 <= row_2 < rows \
            and grid[row_2][col_2] != wall_value \
            and (col_2, row_2) not in seen:
          to_A_came_from[(col_2, row_2)] = [col, row]
          to_visit.append((col_2, row_2))
          seen.add((col_2, row_2))

  @staticmethod
  def _build_coord_path(to_A_came_from: Dict[Tuple, Tuple], start_col, start_row, cur_col, cur_row):
    path = []
    while (cur_col, cur_row) != (start_col, start_row):
      path.append((cur_col, cur_row))
      (cur_col, cur_row) = to_A_came_from[cur_col, cur_row]

    path.append((cur_col, cur_row))
    path.reverse()
    return path

  @staticmethod
  def path_to_directions(path: List[Tuple]) -> List[enums.Direction]:
    directions_path = []
    for i in range(len(path) - 1):
      cur_col, cur_row = path[i]
      next_col, next_row = path[i + 1]
      diff = (next_col - cur_col, next_row - cur_row)
      if diff == (1, 0):
        directions_path.append(enums.Direction.RIGHT)
      if diff == (0, 1):
        directions_path.append(enums.Direction.UP)
      if diff == (-1, 0):
        directions_path.append(enums.Direction.LEFT)
      if diff == (0, -1):
        directions_path.append(enums.Direction.DOWN)
      if diff == (1, 1):
        directions_path.append(enums.Direction.UP_RIGHT)
      if diff == (-1, 1):
        directions_path.append(enums.Direction.UP_LEFT)
      if diff == (1, -1):
        directions_path.append(enums.Direction.DOWN_RIGHT)
      if diff == (-1, -1):
        directions_path.append(enums.Direction.DOWN_LEFT)
    return directions_path

  @staticmethod
  def to_directions_with_time(directions: List[enums.Direction]) -> List[Tuple]:
    directions_with_time = []
    if not directions:
      return []

    cur_direction = directions[0]
    cur_time = constants.SEC_PER_PIXEL_SPEED

    for i in range(2, len(directions)):
      if directions[i] == cur_direction:
        cur_time += constants.SEC_PER_PIXEL_SPEED
      else:
        directions_with_time.append((cur_direction, cur_time))
        cur_direction = directions[i]
        cur_time = constants.SEC_PER_PIXEL_SPEED
    return directions_with_time
