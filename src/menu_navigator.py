import time
import pyautogui


def move_to_map():
	pyautogui.keyDown('d')
	time.sleep(0.5)
	pyautogui.keyUp('d')
	pyautogui.hotkey('f')


def select_level():
	move_to_map()
	pyautogui.hotkey('up')
	pyautogui.hotkey('up')
	pyautogui.hotkey('right')


def vote_reset():
	pyautogui.hotkey('escape')
	pyautogui.hotkey('down')
	pyautogui.hotkey('down')
	pyautogui.hotkey('enter')
	time.sleep(2.8)


vote_reset()
select_level()