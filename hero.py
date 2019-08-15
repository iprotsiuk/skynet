import pyautogui

import directions


class Character(object):
  current_direction = directions.Direction.HOLD

  def move(self, new_dir: directions.Direction):
    if self.current_direction == new_dir:
      return
    # print("MOOOVE!!!", new_dir)
    self.stop()
    self.current_direction = new_dir
    if new_dir == directions.Direction.UP:
      pyautogui.keyDown('w')
      pyautogui.keyDown('up')
    if new_dir == directions.Direction.UP_RIGHT:
      pyautogui.keyDown('w')
      pyautogui.keyDown('d')
      pyautogui.keyDown('up')
      pyautogui.keyDown('right')
    if new_dir == directions.Direction.RIGHT:
      pyautogui.keyDown('d')
      pyautogui.keyDown('right')
    if new_dir == directions.Direction.DOWN_RIGHT:
      pyautogui.keyDown('d')
      pyautogui.keyDown('s')
      pyautogui.keyDown('down')
      pyautogui.keyDown('right')
    if new_dir == directions.Direction.DOWN:
      pyautogui.keyDown('s')
      pyautogui.keyDown('down')
    if new_dir == directions.Direction.DOWN_LEFT:
      pyautogui.keyDown('s')
      pyautogui.keyDown('a')
      pyautogui.keyDown('down')
      pyautogui.keyDown('left')
    if new_dir == directions.Direction.LEFT:
      pyautogui.keyDown('a')
      pyautogui.keyDown('left')
    if new_dir == directions.Direction.UP_LEFT:
      pyautogui.keyDown('a')
      pyautogui.keyDown('w')
      pyautogui.keyDown('up')
      pyautogui.keyDown('left')


  def stop(self):
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')
    pyautogui.keyUp('left')
    pyautogui.keyUp('up')
    pyautogui.keyUp('down')
    pyautogui.keyUp('right')
    self.current_direction = directions.Direction.HOLD


@staticmethod
def act():
  pyautogui.hotkey('f')
