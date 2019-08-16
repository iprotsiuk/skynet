import matplotlib
import numpy as np


def draw_path_on_map(map, path, target_x, target_y):
  map_tmp = np.copy(map)
  for x, y in path:
    map_tmp[x][y] = 1

  # Mark Target as square
  map_tmp[target_x - 3:target_x + 3,
  target_y - 3:target_y + 3].fill(1)

  matplotlib.pyplot.imshow(map_tmp)
  matplotlib.pyplot.show()
