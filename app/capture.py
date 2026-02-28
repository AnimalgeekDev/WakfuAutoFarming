"""Capture utilities for wakfu window.

The implementation here provides a best-effort capture. If a per-window
capture is required later we can extend this module to use `win32gui` and
`mss` to capture the specific window rectangle.
"""
from typing import Tuple
from PIL import Image
import mss
import mss.tools
import win32gui
import win32process
import psutil
import time


def _find_window_by_process_name(process_name: str):
    """Return the first top-level window handle matching process name.

    Args:
        process_name: process filename (e.g. 'wakfu.exe')

    Returns:
        hwnd or None if not found
    """
    found = None

    def _enum(hwnd, _):
        nonlocal found
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                proc = psutil.Process(pid)
                if proc.name().lower() == process_name.lower():
                    found = hwnd
            except Exception:
                return
        except Exception:
            return

    win32gui.EnumWindows(_enum, None)
    return found


def capture_wakfu_window(process_name: str) -> Image.Image:
    """Capture the wakfu window by process name; fallback to full screen.

    Args:
        process_name: process filename (e.g. 'wakfu.exe').

    Returns:
        PIL.Image.Image

    Raises:
        Exception: if mss capture fails.
    """
    hwnd = _find_window_by_process_name(process_name)
    with mss.mss() as sct:
        try:
            if hwnd is None:
                # fallback to full screen
                monitor = sct.monitors[0]
                img = sct.grab(monitor)
            else:
                try:
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                except Exception:
                    # fallback to full screen
                    monitor = sct.monitors[0]
                    img = sct.grab(monitor)
                else:
                    bbox = {"left": left, "top": top, "width": right - left, "height": bottom - top}
                    img = sct.grab(bbox)
            pil = Image.frombytes("RGB", img.size, img.rgb)
            return pil
        except Exception as exc:
            raise Exception(f"capture_wakfu_window: mss capture failed: {exc}")
