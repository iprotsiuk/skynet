import unittest

from src.enums import Direction
from src.minimap_provider import MapProvider
from src.path_planner import PathFinder


class TestPathPlanner(unittest.TestCase):

  def test_path_to_directions_going_down(self):
    path = [(98, 99), (99, 99), (100, 99), (101, 99), (102, 99), (103, 99), (104, 99), (105, 99), (106, 99), (107, 99),
            (108, 99), (109, 99), (110, 99), (111, 99), (112, 99), (113, 99), (114, 99), (115, 99), (116, 99),
            (117, 99), (118, 99), (119, 99), (120, 99), (121, 99), (122, 99), (123, 99), (124, 99), (125, 99),
            (126, 99), (127, 98)]
    directions = PathFinder.to_directions_with_time(PathFinder.path_to_directions(path))
    dir, time_sec = directions[0]
    self.assertEqual(Direction.DOWN, dir)


if __name__ == '__main__':
  unittest.main()

m = MapProvider()
m.update_maps()
