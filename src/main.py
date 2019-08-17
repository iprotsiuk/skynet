from src import actor, menu_navigator, constants
import time
from src import debug_utils

print("....")
time.sleep(0.3)
print("...")
time.sleep(0.3)
print("..")
time.sleep(0.3)
print(".")
time.sleep(0.3)
print (" Satrted ")


def wait_and_click_f(timeout, hero):
  iters = round(timeout * 20)
  for i in range(iters):
    # hero.act()
    time.sleep(0.05)

menu_navigator.reload()
a = actor.Actor()
end_time = time.time() + constants.MAP_TIME_SEC
while True:
  a.update_plan()
  print("taraget: ", a.target_col, a.target_row)
  print("planned_directions = ", a.planned_directions)
  print("planned_directions_with_time = ", a.planned_directions_with_time)
  print("is in town = ", a.is_in_town)
  if a.is_in_town or time.time() > end_time:
    a.hero.stop()
    menu_navigator.reload()
    end_time = time.time() + constants.MAP_TIME_SEC


  # debug_utils.draw_path_on_map(a.black_map, a.planned_pixel_path, target_row=a.target_row, target_column=a.target_col)

  for move, time_sec in a.planned_directions_with_time:
    a.hero.move(move)
    wait_and_click_f(time_sec, a.hero)
    time.sleep(time_sec)




