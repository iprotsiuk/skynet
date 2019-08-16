import pyautogui

from src import enums


class Character(object):
  current_direction = enums.Direction.HOLD

  def move(self, new_dir: enums.Direction):
    if self.current_direction == new_dir:
      return
    # print("MOOOVE!!!", new_dir)
    self.stop()
    self.current_direction = new_dir
    if new_dir == enums.Direction.UP:
      pyautogui.keyDown('w')
      pyautogui.keyDown('up')
    if new_dir == enums.Direction.UP_RIGHT:
      pyautogui.keyDown('w')
      pyautogui.keyDown('d')
      pyautogui.keyDown('up')
      pyautogui.keyDown('right')
    if new_dir == enums.Direction.RIGHT:
      pyautogui.keyDown('d')
      pyautogui.keyDown('right')
    if new_dir == enums.Direction.DOWN_RIGHT:
      pyautogui.keyDown('d')
      pyautogui.keyDown('s')
      pyautogui.keyDown('down')
      pyautogui.keyDown('right')
    if new_dir == enums.Direction.DOWN:
      pyautogui.keyDown('s')
      pyautogui.keyDown('down')
    if new_dir == enums.Direction.DOWN_LEFT:
      pyautogui.keyDown('s')
      pyautogui.keyDown('a')
      pyautogui.keyDown('down')
      pyautogui.keyDown('left')
    if new_dir == enums.Direction.LEFT:
      pyautogui.keyDown('a')
      pyautogui.keyDown('left')
    if new_dir == enums.Direction.UP_LEFT:
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
    self.current_direction = enums.Direction.HOLD

  @staticmethod
  def act():
    pyautogui.hotkey('f')
