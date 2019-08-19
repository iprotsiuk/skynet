import time

import pyautogui


def escape():
  pyautogui.hotkey('escape')


def move_to_teleport():
  pyautogui.keyDown('d')
  time.sleep(0.35)
  pyautogui.keyUp('d')
  pyautogui.hotkey('f')

def keyDownUp(str):
  pyautogui.keyDown(str)
  pyautogui.keyUp(str)


def select_level():
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('a')
  # keyDownUp('enter')
  pyautogui.keyDown('d')
  pyautogui.keyUp('d')
  pyautogui.keyDown('d')
  pyautogui.keyUp('d')
  pyautogui.keyDown('d')
  pyautogui.keyUp('d')
  pyautogui.keyDown('d')
  pyautogui.keyUp('d')
  pyautogui.keyDown('d')
  pyautogui.keyUp('d')

  pyautogui.keyDown('enter')
  pyautogui.keyUp('enter')
  time.sleep(2.1)


def vote_reset():
  pyautogui.hotkey('escape')
  pyautogui.hotkey('down')
  pyautogui.hotkey('down')
  pyautogui.hotkey('enter')
  time.sleep(3.3)


def reload():
  vote_reset()
  move_to_teleport()
  select_level()
