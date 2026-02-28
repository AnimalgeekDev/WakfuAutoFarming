"""Actions simulation: click helpers and flow flags.

This module provides a small `ActionController` which holds flags used by the
GUI loop and helper methods to simulate mouse clicks.
"""
from dataclasses import dataclass
import pyautogui
from typing import Optional


@dataclass
class ActionController:
    processing_image: bool = False
    waiting_for_actions: bool = False
    perform_actions: bool = False
    waiting_since: Optional[float] = None

    def simulate_right_click(self, x: int, y: int) -> None:
        """Move the mouse to (x,y) and simulate a right-click.

        Raises:
            Exception: if pyautogui operations fail.
        """
        try:
            pyautogui.moveTo(x, y)
            pyautogui.click(button="right")
        except Exception as exc:
            raise Exception(f"ActionController.simulate_right_click: {exc}")

    def simulate_left_click(self, x: int, y: int) -> None:
        """Move the mouse to (x,y) and simulate a left-click.

        Raises:
            Exception: if pyautogui operations fail.
        """
        try:
            pyautogui.moveTo(x, y)
            pyautogui.click(button="left")
        except Exception as exc:
            raise Exception(f"ActionController.simulate_left_click: {exc}")

    def set_waiting(self, flag: bool) -> None:
        """Set the waiting_for_actions flag and record timestamp when set True."""
        self.waiting_for_actions = flag
        if flag:
            import time

            self.waiting_since = time.time()
        else:
            self.waiting_since = None
