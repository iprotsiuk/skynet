import directions
import collections
from typing import Dict, Tuple, List

import numpy


class PathFinder(object):
  def __init__(self):
    # Empty Consturctor
    pass

  def find_path(self, black_minimap: numpy.ndarray, start_x: int, start_y: int, goal_x: int, goal_y: int) -> List[directions.Direction]:
    path = self._bfs(black_minimap, 1, start_x, start_y, goal_x, goal_y)
    if path is None:
      return []
    return path

  def _bfs(self, grid: numpy.ndarray, wall_value: int, start_x: int, start_y: int, goal_x: int, goal_y: int):
    rows, cols = grid.shape
    to_visit = collections.deque()
    to_visit.append((start_x, start_y))
    seen = set()
    to_A_came_from = {}

    while to_visit:
      (x, y) = to_visit.popleft()
      seen.add((x, y))
      if (x, y) == (goal_x, goal_y):
        return self._build_coord_path(to_A_came_from, start_x, start_y, x, y)
      for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x -1, y-1), (x -1, y+1), (x+1, y-1), (x + 1, y+1)):
        if 0 <= x2 < cols \
            and 0 <= y2 < rows \
            and grid[y2][x2] != wall_value \
            and (x2, y2) not in seen:
          to_A_came_from[(x2, y2)] = [x, y]
          to_visit.append((x2, y2))
          seen.add((x2, y2))

  def _build_coord_path(self, to_A_came_from: Dict[Tuple, Tuple], start_x, start_y, cur_x, cur_y):
    path = []
    while (cur_x, cur_y) != (start_x, start_y):
      path.append((cur_x, cur_y))
      (cur_x, cur_y) = to_A_came_from[cur_x, cur_y]

    path.append((cur_x, cur_y))
    path.reverse()
    return path

  def path_to_directions(self, path : List[Tuple]) -> List[directions.Direction]:
    directions_path = []
    for i in range(len(path) - 1):
      x_cur, y_cur = path[i]
      x_next, y_next = path[i+1]
      diff = (x_next - x_cur, y_next - y_cur)
      if diff == (1, 0):
        directions_path.append(directions.Direction.RIGHT)
      if diff == (0, 1):
        directions_path.append(directions.Direction.UP)
      if diff == (-1, 0):
        directions_path.append(directions.Direction.LEFT)
      if diff == (0, -1):
        directions_path.append(directions.Direction.DOWN)
      if diff == (1, 1):
        directions_path.append(directions.Direction.UP_RIGHT)
      if diff == (-1, 1):
        directions_path.append(directions.Direction.UP_LEFT)
      if diff == (1, -1):
        directions_path.append(directions.Direction.DOWN_RIGHT)
      if diff == (-1, -1):
        directions_path.append(directions.Direction.DOWN_LEFT)
    return directions_path