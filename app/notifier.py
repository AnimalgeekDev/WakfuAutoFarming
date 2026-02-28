"""Simple Windows notifier wrapper.

This module provides a `notify` function that attempts to use `win10toast`.
If the library is not available, the function will raise an exception so the
caller can handle fallbacks.
"""
from typing import Any


def notify(title: str, message: str) -> None:
    """Show a Windows toast notification.

    Args:
        title: notification title.
        message: notification body.

    Raises:
        Exception: if notification cannot be shown.
    """
    try:
        from win10toast import ToastNotifier

        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)
    except Exception as exc:
        raise Exception(f"notifier.notify: {exc}")
