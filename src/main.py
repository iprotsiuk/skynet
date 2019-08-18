import time

import pyautogui

from src import actor, menu_navigator, constants

print("....")
time.sleep(0.3)
print("...")
time.sleep(0.3)
print("..")
time.sleep(0.3)
print(".")
time.sleep(0.3)
print(" Satrted ")


# def draw_path_on_map_from_img(imp_path):
#   path = []
#   img = cv2.imread(imp_path)
#   black_map = minimap_provider.MapProvider.get_black_minimap(img)
#   draw_image(black_map)
#   map = minimap_provider.MapProvider.get_black_minimap_bold(black_map)
#   draw_image(map)
#   draw_path_on_map(map, path, 171,103)
#
# draw_path_on_map_from_img('test_data/map_trying_go_171_103.png')


def wait_and_click_f(timeout, hero):
  time_end_move = time.time() + timeout
  while time.time() < time_end_move:
    hero.act()
    pyautogui.hotkey('4')
    pyautogui.hotkey('1')
    pyautogui.hotkey('2')


# Start and go right'
menu_navigator.reload()
pyautogui.keyDown('d')
a = actor.Actor()
time.sleep(2.1)
pyautogui.keyUp('d')

end_time = time.time() + constants.MAP_TIME_SEC
while True:
  print("\nStart of iteration", a.iteration)
  a.update_plan()
  # print("planned_pixel_path = ", a.planned_pixel_path)
  # print("planned_directions = ", a.planned_directions)
  print("planned_directions_with_time = ", a.planned_directions_with_time)
  1
  print("is in town = ", a.is_in_town)
  if a.is_in_map_selector:
    a.hero.stop()
    menu_navigator.escape()
    menu_navigator.reload()

  if a.is_in_town or time.time() > end_time:
    a.hero.stop()
    menu_navigator.reload()
    end_time = time.time() + constants.MAP_TIME_SEC

  if not a.planned_directions_with_time:
    a.hero.random_move()
    continue
  # debug_utils.draw_path_on_map(a.black_map, a.planned_pixel_path, target_row=a.target_row, target_column=a.target_col)

  time_end_move = time.time() + 1.5
  for move, time_sec in a.planned_directions_with_time:
    if time.time() > time_end_move:
      break
    # limit one move with 1 sec
    time_sec = min(1, time_sec)
    print('moving:', move, "for ", round(time_sec, 3))
    a.hero.move(move)
    wait_and_click_f(time_sec, a.hero)
    # time.sleep(time_sec)
  a.hero.stop()