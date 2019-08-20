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
  keyDownUp('d')
  keyDownUp('d')
  keyDownUp('d')
  keyDownUp('d')
  keyDownUp('d')
  keyDownUp('enter')
  pyautogui.keyDown('d')
  time.sleep(2.1)
  pyautogui.keyUp('d')


def select_last_level():
  keyDownUp('a')
  keyDownUp('enter')
  pyautogui.keyDown('d')
  time.sleep(2.1)
  pyautogui.keyUp('d')


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


def reload_last_level():
  vote_reset()
  move_to_teleport()
  select_last_level()
