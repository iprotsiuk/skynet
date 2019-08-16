from src import actor
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
print ("!Satrted!")

a = actor.Actor()

while True:
  time.sleep(3)
  a.update_plan()
  dirs = a.planned_directions
  print("taraget: ", a._cur_target_x, a._cur_target_y)
  print("target_square: ", a._cur_target_square)
  print("new direction = ", dirs[0])
  a.hero.move(dirs[0])



