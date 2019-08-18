import matplotlib.pyplot
import numpy as np

from src import constants

PLAYER_COL = constants.PLAYER_MINIMAP_COLUMN
PLAYER_ROW = constants.PLAYER_MINIMAP_ROW


def draw_path_on_map(map, path, target_row, target_column):
  map_tmp = np.copy(map)
  for row, column in path:
    map_tmp[row][column] = 1

  # Mark Target as square
  # map_tmp[target_row - 5:target_row + 5,
  # target_column - 5:target_column + 5].fill(30)

  # Mark Player
  map_tmp[constants.PLAYER_MINIMAP_ROW - 3:constants.PLAYER_MINIMAP_ROW + 3,
  constants.PLAYER_MINIMAP_COLUMN - 3:constants.PLAYER_MINIMAP_COLUMN + 3].fill(30)

  matplotlib.pyplot.imshow(map_tmp)
  matplotlib.pyplot.show()


def draw_image(img):
  matplotlib.pyplot.imshow(img)
  matplotlib.pyplot.show()

# def get_black_minimap() -> numpy.ndarray:
#   # Load image and convert to greyscale
#   img = cv.imread('test_data/map_wrong_path.png')
#   img_data = np.asarray(img)
#   img_gray = cv.cvtColor(img_data, cv.COLOR_BGR2GRAY)
#   # debug_utils.draw_image(img_gray)
#
#   # Pixels higher than this will be 1. Otherwise 0.
#   black_picture = (img_gray > BLACK_THRESHOLD_VALUE)
#   # debug_utils.draw_image(black_picture)
#
#   # Remove character from the map
#   black_picture[PLAYER_ROW - PLAYER_HEIGHT:PLAYER_ROW + PLAYER_HEIGHT,
#   PLAYER_COL - PLAYER_WIDTH:PLAYER_COL + PLAYER_WIDTH].fill(0)
#
#   return black_picture
#
# def get_black_minimap_bold(original_map) -> numpy.ndarray:
#   max_row, max_col = original_map.shape
#   bold_map = np.copy(original_map)
#
#   for row in range(max_row):
#     for col in range(max_col):
#       if original_map[row][col] == 1 and row < max_row - 1:
#         bold_map[row + 1][col] = 1
#
#   return bold_map