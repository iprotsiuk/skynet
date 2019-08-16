from src import actor
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
print ("!Satrted!")

a = actor.Actor()
a.update_plan()
while True:
  time.sleep(3)

  dirs = a.planned_directions_with_time
  print("taraget: ", a._cur_target_x, a._cur_target_y)
  print("target_square: ", a._cur_target_square)
  print("planned_directions_with_time = ", dirs)

  debug_utils.draw_path_on_map(a.black_map, a.planned_pixel_path, a._cur_target_x, a._cur_target_y)

  for move, time_sec in dirs:
    a.hero.move(move)
    time.sleep(time_sec)



