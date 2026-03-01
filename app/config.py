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
    threshold: float
    wakfu_process_name: str
    device: str
    script_use: str
    template_items_path: str
    template_actions_path: str
    template_captain_miau_path: str
    opencv_method: str
    threshold: float
    max_overlap: float
    time_wait_search_action: float
    time_wait_new_action: float


def load_config() -> Config:
    load_dotenv()
    
    script_use = os.getenv("SCRIPT_USE")
    wakfu_process_name = os.getenv("WAKFU_PROCESS_NAME")
    threshold_raw = os.getenv("THRESHOLD")
    
    model_path = os.getenv("MODEL_PATH")
    img_size_raw = os.getenv("IMG_SIZE")
    device = os.getenv("DEVICE")
    
    template_items_path = os.getenv("TEMPLATE_ITEMS_PATH")
    template_actions_path = os.getenv("TEMPLATE_ACTIONS_PATH")
    template_captain_miau_path = os.getenv("TEMPLATE_CAPTAIN_MIAU_PATH")
    opencv_method = os.getenv("OPENCV_METHOD")
    max_overlap_raw = os.getenv("MAX_OVERLAP")
    time_wait_search_action_raw = os.getenv("TIME_WAIT_SEARCH_ACTION")
    time_wait_new_action_raw = os.getenv("TIME_WAIT_NEW_ACTION")

    if script_use is None:
        raise Exception("load_config: SCRIPT_USE is not set in .env")
    if wakfu_process_name is None:
        raise Exception("load_config: WAKFU_PROCESS_NAME is not set in .env")
    if threshold_raw is None:
        raise Exception("load_config: THRESHOLD is not set in .env")
    try:
        threshold = float(threshold_raw)
    except Exception as exc:
        raise Exception(f"load_config: THRESHOLD invalid: {exc}")
    
    if model_path is None:
        raise Exception("load_config: MODEL_PATH is not set in .env")
    if img_size_raw is None:
        raise Exception("load_config: IMG_SIZE is not set in .env")
    if device is None:
        raise Exception("load_config: DEVICE is not set in .env")
    try:
        img_size = int(img_size_raw)
    except Exception as exc:
        raise Exception(f"load_config: IMG_SIZE invalid: {exc}")
    
    if template_items_path is None:
        raise Exception("load_config: TEMPLATE_ITEMS_PATH is not set in .env")
    if template_actions_path is None:
        raise Exception("load_config: TEMPLATE_ACTIONS_PATH is not set in .env")
    if template_captain_miau_path is None:
        raise Exception("load_config: TEMPLATE_CAPTAIN_MIAU_PATH is not set in .env")
    if opencv_method is None:
        raise Exception("load_config: OPENCV_METHOD is not set in .env")
    if max_overlap_raw is None:
        raise Exception("load_config: MAX_OVERLAP is not set in .env")
    try:
        max_overlap = float(max_overlap_raw)
    except Exception as exc:
        raise Exception(f"load_config: IMG_SIZE invalid: {exc}")
    if time_wait_search_action_raw is None:
        raise Exception("load_config: TIME_WAIT_SEARCH_ACTION is not set in .env")
    try:
        time_wait_search_action = float(time_wait_search_action_raw)
    except Exception as exc:
        raise Exception(f"load_config: IMG_SIZE invalid: {exc}")
    if time_wait_new_action_raw is None:
        raise Exception("load_config: TIME_WAIT_NEW_ACTION is not set in .env")
    try:
        time_wait_new_action = float(time_wait_new_action_raw)
    except Exception as exc:
        raise Exception(f"load_config: IMG_SIZE invalid: {exc}")

    return Config(
        script_use=script_use,
        wakfu_process_name=wakfu_process_name,
        threshold=threshold,
        model_path=model_path,
        img_size=img_size,
        device=device,
        template_items_path=template_items_path,
        template_actions_path=template_actions_path,
        template_captain_miau_path=template_captain_miau_path,
        opencv_method=opencv_method,
        max_overlap=max_overlap,
        time_wait_search_action=time_wait_search_action,
        time_wait_new_action=time_wait_new_action
    )
