import autopy
import time
import random
import keyboard
from pprint import pprint

print("....")
time.sleep(0.3)
print("...")
time.sleep(0.3)
print("..")
time.sleep(0.3)
print(".")
time.sleep(0.3)
print ("Satrted!")

#autopy.mouse.move(1032, 700)


# while time.time() < timeout:
#   autopy.mouse.click()
#   autopy.key.tap(key=autopy.key.Code.UP_ARROW, modifiers=[])
#   # autopy.key.toggle(key='a', down=True, modifiers=[])
#   # autopy.key.toggle(key='a', down=False, modifiers=[])
#   # autopy.key.toggle(key=autopy.key.Code.SPACE, down=False, modifiers=[])
#   keyboard.press_and_release('a')
#   time.sleep(random.uniform(0.001, 0.003))

# timeout = time.time() + 3   # 5 seconds from now
# while time.time() < timeout:
#   # keyboard.press_and_release('8 down')
#   keyboard.press('4')
#   var k
#   k.scan_code = '7'
#   keyboard.play([k], speed_factor=3)
#   time.sleep(random.uniform(0.1, 0.3a))

# Record events until 'esc' is pressed.
# recorded = keyboard.record(until='esc')
# #
# print(recorded[0].__dict__)
# print(recorded[1].__dict__)
# keyboard.play(recorded, speed_factor=3)
# {'event_type': 'down', 'scan_code': 30, 'time': 1565679358.164229, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'a'}
# {'event_type': 'up', 'scan_code': 31, 'time': 1565680129.8547351, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 's'}
# {'event_type': 'down', 'scan_code': 17, 'time': 1565680130.1306477, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'w'}
# {'event_type': 'down', 'scan_code': 32, 'time': 1565680168.4957724, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'd'}
# {'event_type': 'down', 'scan_code': 75, 'time': 1565680626.7518094, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'left'}
# {'event_type': 'up', 'scan_code': 77, 'time': 1565680645.2064247, 'device': None, 'is_keypad': False, 'modifiers': None, 'name': 'right'}

def pressCodeWithInterrupts(time_sec, code, hold_code):
  iters = round(time_sec*10)
  for i in range(iters):
    keyboard.press_and_release('f')
    keyboard.press_and_release('space')
    keyboard.press_and_release('f')
    pressCode(time_sec, code, hold_code, event_type=keyboard.KEY_DOWN)
    keyboard.press_and_release('f')
    time.sleep(0.1)
  pressCode(time_sec, code, hold_code, event_type=keyboard.KEY_UP)


def pressCode(time_sec, code, hold_code, event_type):
  keyboard.start_recording()
  down=keyboard.KeyboardEvent(scan_code=code, event_type=event_type)
  attak=keyboard.KeyboardEvent(scan_code=hold_code, event_type=event_type)
  keyboard.play([down, attak], speed_factor=3)

def holdLeft(time_sec):
  pressCodeWithInterrupts(time_sec, 30, 75)
def holdRight(time_sec):
  pressCodeWithInterrupts(time_sec, 32, 77)
def holdUp(time_sec):
  pressCodeWithInterrupts(time_sec, 17, 77)
def holdDown(time_sec):
  pressCodeWithInterrupts(time_sec, 31, 77)

# i = 0
# while True:
#   i += 1
#   if (i%5 == 0):
#     holdDown(0.2)
#   else:
#     holdUp(0.1)
#   timeout = time.time() + 30*60   # 30 min from now
#   while time.time() < timeout:
#     holdRight(4)
#     holdLeft(4)



import pyautogui

pyautogui.keyDown('left')
pyautogui.keyDown('s')
pyautogui.keyDown('a')

# while True:
#   pyautogui.keyDown('left')
#   time.sleep(random.uniform(0.1, 3))
#   pyautogui.keyUp('left')
#   pyautogui.press('4')
#
#   pyautogui.keyDown('up')
#   time.sleep(random.uniform(0.1, 2))
#   pyautogui.press('1')
#   pyautogui.keyUp('up')
#
#   pyautogui.keyDown('down')
#   time.sleep(random.uniform(0.1, 0.3))
#   pyautogui.keyUp('down')
