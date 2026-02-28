"""Configuration loader for the application.

This module reads environment variables from a .env file and provides a
typed `Config` dataclass used across the application.
"""
from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Config:
    model_path: str
    img_size: int
    confidence_threshold: float
    wakfu_process_name: str
    device: str


def load_config() -> Config:
    """Load configuration from .env located at the repository root.

    Raises:
        Exception: if required environment variables are missing.
    Returns:
        Config: typed configuration object.
    """
    load_dotenv()
    model_path = os.getenv("MODEL_PATH")
    img_size = os.getenv("IMG_SIZE")
    confidence_threshold = os.getenv("CONFIDENCE_THRESHOLD")
    wakfu_process_name = os.getenv("WAKFU_PROCESS_NAME")
    device = os.getenv("DEVICE")

    if model_path is None:
        raise Exception("load_config: MODEL_PATH is not set in .env")
    if img_size is None:
        raise Exception("load_config: IMG_SIZE is not set in .env")
    if confidence_threshold is None:
        raise Exception("load_config: CONFIDENCE_THRESHOLD is not set in .env")
    if wakfu_process_name is None:
        raise Exception("load_config: WAKFU_PROCESS_NAME is not set in .env")
    if device is None:
        raise Exception("load_config: DEVICE is not set in .env")

    try:
        img_size_int = int(img_size)
    except Exception as exc:
        raise Exception(f"load_config: IMG_SIZE invalid: {exc}")

    try:
        conf_float = float(confidence_threshold)
    except Exception as exc:
        raise Exception(f"load_config: CONFIDENCE_THRESHOLD invalid: {exc}")

    return Config(
        model_path=model_path,
        img_size=img_size_int,
        confidence_threshold=conf_float,
        wakfu_process_name=wakfu_process_name,
        device=device
    )
