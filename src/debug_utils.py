import matplotlib
import numpy as np


def draw_path_on_map(map, path, target_row, target_column):
  map_tmp = np.copy(map)
  for row, column in path:
    map_tmp[row][column] = 1

  # Mark Target as square
  map_tmp[target_row - 3:target_row + 3,
  target_column - 3:target_column + 3].fill(1)

  matplotlib.pyplot.imshow(map_tmp)
  matplotlib.pyplot.show()
