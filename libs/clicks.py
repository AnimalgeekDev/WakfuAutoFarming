import pyautogui

def right_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')