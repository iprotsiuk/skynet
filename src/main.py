import pyautogui

from src import actor, menu_navigator, constants, debug_utils
import time

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
  time_end_move = time.time()+timeout
  while time.time() < time_end_move:
    hero.act()
    pyautogui.hotkey('3')
    time.sleep(0.02)

# Start and go right'
menu_navigator.reload()
pyautogui.keyDown('d')
a = actor.Actor()
time.sleep(1.8)
pyautogui.keyUp('d')

end_time = time.time() + constants.MAP_TIME_SEC
while True:
  a.update_plan()
  print("taraget: ", a.target_col, a.target_row)
  print("planned_pixel_path = ", a.planned_pixel_path)
  print("planned_directions = ", a.planned_directions)
  print("planned_directions_with_time = ", a.planned_directions_with_time)
  print("is in town = ", a.is_in_town)
  if a.is_in_map_selector:
    a.hero.stop()
    menu_navigator.escape()
    menu_navigator.reload()

  if a.is_in_town or time.time() > end_time:
    a.hero.stop()
    menu_navigator.reload()
    end_time = time.time() + constants.MAP_TIME_SEC


  # debug_utils.draw_path_on_map(a.black_map, a.planned_pixel_path, target_row=a.target_row, target_column=a.target_col)

  time_end_move = time.time() + 1.5
  for move, time_sec in a.planned_directions_with_time:
    if (time.time() > time_end_move):
      break
    print('moving:', move, "for ", round(time_sec, 3))
    a.hero.move(move)
    wait_and_click_f(time_sec, a.hero)
    # time.sleep(time_sec)
  a.hero.stop()




