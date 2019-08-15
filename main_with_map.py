import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import collections
import time
import pyautogui as p

MINIMAP_X_SIZE = 198
MINIMAP_Y_SIZE = 196
PLAYER_X = 99
PLAYER_Y = 98
BLACK_THRESHOLD_VALUE = 40


def rgb2gray(rgb):
  return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def getMinimap():
  time.sleep(2)
  windowLocation = p.locateOnScreen('data/teleport_icon.png')
  miniMapLocationX = windowLocation.left+280

  miniMapLocationY = windowLocation.top-416-MINIMAP_Y_SIZE

  return p.screenshot('data/minimap.png', region=(miniMapLocationX, miniMapLocationY, MINIMAP_X_SIZE, MINIMAP_Y_SIZE))
  #Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details)


def imageToBlack(img):
  # Load image and convert to greyscale
  # img = Image.open("example_map1.png")
  img = img.convert("L")

  imgData = np.asarray(img)
  # Pixels higher than this will be 1. Otherwise 0.
  black_picture = (imgData > BLACK_THRESHOLD_VALUE)
  range = 5
  plt.imshow(black_picture[PLAYER_Y-range:PLAYER_Y+range, PLAYER_X-range:PLAYER_X+range])
  plt.show()

  black_picture[PLAYER_Y-range:PLAYER_Y+range, PLAYER_X-range:PLAYER_X+range].fill(0)

  return black_picture


def buildPath(to_A_came_from, start_x, start_y, cur_x, cur_y):
  path = []
  while (cur_x, cur_y) != (start_x, start_y):
    path.append((cur_x, cur_y))
    (cur_x, cur_y) = to_A_came_from[cur_x, cur_y]

  path.append((cur_x, cur_y))
  path.reverse()
  return path


def bfs(grid, start_x, start_y, goal_x, goal_y):
  width, height = grid.shape
  wall = 1

  to_visit = collections.deque()
  to_visit.append((start_x, start_y))

  seen = set()
  to_A_came_from = {}
  while to_visit:
    (x, y) = to_visit.popleft()
    # print("looking", x, y)
    seen.add((x, y))
    if (x, y) == (goal_x, goal_y):
      return buildPath(to_A_came_from, start_x, start_y, x, y)
    for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
      if 0 <= x2 < width \
        and 0 <= y2 < height \
        and grid[x2][y2] != wall \
        and (x2, y2) not in seen:
          to_A_came_from[(x2, y2)] = [x, y]
          to_visit.append((x2, y2))
          seen.add((x2, y2))




# MAIN!!!!!!!!!!
minimapImage = getMinimap()
plt.imshow(minimapImage)
plt.show()

black_picture = imageToBlack(minimapImage)
plt.imshow(black_picture)

plt.imshow(black_picture)
plt.show()

print(black_picture.__dict__)
bfs(black_picture, 100, 100, 5, 4)

