"""Entrypoint for the GUI application.

This module wires together config, capture, yolo wrapper, processor and UI.
It uses a background thread to ensure the GUI remains responsive and a single
`processing_image` flag to prevent concurrent image processing.
"""
import cv2
import threading
import time
import traceback
import tkinter as tk

from PIL import Image
from app.config import load_config
from app.capture import capture_wakfu_window
from app.yolo_wrapper import YoloModel
from app.images_processor import TemplateMatcher
from app.processor import transform_yolo_coordinates_to_original, compute_centers, overlay_boxes, overlay_centers
from app.actions import ActionController
from app.notifier import notify
from app.ui import AppUI


def main() -> None:
    try:
        cfg = load_config()

        root = tk.Tk()
        ui = AppUI(root, cfg.threshold)
        actions = ActionController()

        def on_key(event) -> None:
            # stop actions when user presses Q or q
            try:
                if event.keysym.lower() == "q":
                    ui.var_perform_actions.set(False)
                    actions.perform_actions = False
                    actions.set_waiting(False)
            except Exception:
                pass

        root.bind_all("<Key>", on_key)
        
        if cfg.script_use == 'YOLO':
            model = YoloModel()
            model.load(cfg.model_path, device=cfg.device, img_size=cfg.img_size)
        else:
            items_matcher= TemplateMatcher(cfg.template_items_path)
            actions_matcher= TemplateMatcher(cfg.template_actions_path)
            captain_miau_matcher= TemplateMatcher(cfg.template_captain_miau_path)

        def worker_loop() -> None:
            while True:
                if actions.processing_image:
                    time.sleep(0.02)
                    continue
                actions.processing_image = True
                
                try:
                    img = capture_wakfu_window(cfg.wakfu_process_name)
                    threshold = ui.var_threshold.get()
                    
                    if cfg.script_use == 'YOLO':
                        width_org, height_org = img.size
                        
                        img_resize = img.resize((model.img_size, model.img_size), Image.Resampling.LANCZOS)
        
                        scal_x = width_org / model.img_size
                        scal_y = height_org / model.img_size
                        
                        detections_model = model.predict(img_resize, threshold)
                        
                        detections = transform_yolo_coordinates_to_original(detections_model, width_org, height_org, scal_x, scal_y, model.img_size)
                    elif cfg.script_use == 'OPENCV':
                        detections_captain_miau = captain_miau_matcher.template_match(img, getattr(cv2, cfg.opencv_method), threshold, cfg.max_overlap)
                        
                        if actions.waiting_for_actions:
                            detections = actions_matcher.template_match(img, getattr(cv2, cfg.opencv_method), threshold, cfg.max_overlap)
                        else:
                            detections = items_matcher.template_match(img, getattr(cv2, cfg.opencv_method), threshold, cfg.max_overlap)
                        
                    centers = compute_centers(detections)

                    if ui.var_show_centers.get():
                        out = overlay_centers(img, centers)
                    else:
                        out = overlay_boxes(img, detections)
                    ui.update_image(out)

                    actions.perform_actions = ui.var_perform_actions.get()
                    img_w, img_h = img.size
                    center_ref = (img_w // 2, img_h // 2)
                    
                    if actions.perform_actions:
                        for det in detections_captain_miau:
                            if det["class"] == "captain_miau" or det["class"] == "captain_miau_2":
                                try:
                                    notify("Capitan miau detectado", "Capitan miau detectado, se necesita intervención")
                                except Exception:
                                    pass
                                ui.var_perform_actions.set(False)
                                actions.perform_actions = False
                                actions.set_waiting(False)
                                break

                    if actions.perform_actions and not actions.waiting_for_actions:
                        idx = find_nearest_index(centers, center_ref)
                        if idx != -1:
                            cx, cy = centers[idx]
                            try:
                                actions.simulate_right_click(cx, cy)
                            except Exception:
                                pass
                            time.sleep(cfg.time_wait_search_action)
                            actions.set_waiting(True)

                    if actions.waiting_for_actions:
                        import time as _time

                        now = _time.time()
                        if actions.waiting_since is not None and (now - actions.waiting_since) * 1000.0 > 5000.0:
                            try:
                                notify("Sin acciones?", "No se detectaron acciones en la pantalla")
                            except Exception:
                                pass
                            actions.set_waiting(False)
                        else:
                            target_idx = -1
                            for i, det in enumerate(detections):
                                if det["class"] == "get_seed":
                                    target_idx = i
                                    break
                            if target_idx == -1:
                                for i, det in enumerate(detections):
                                    if det["class"] == "get_item" or det["class"] == "get_item_2":
                                        target_idx = i
                                        break
                            if target_idx != -1:
                                tx1, ty1, tx2, ty2 = detections[target_idx]["box"]
                                tx = int((tx1 + tx2) / 2)
                                ty = int((ty1 + ty2) / 2)
                                try:
                                    actions.simulate_right_click(tx, ty)
                                except Exception:
                                    pass
                                time.sleep(cfg.time_wait_new_action)
                                actions.set_waiting(False)

                except Exception:
                    traceback.print_exc()
                finally:
                    actions.processing_image = False
                time.sleep(0.05)

        from app.processor import find_nearest_index

        thread = threading.Thread(target=worker_loop, daemon=True)
        thread.start()

        root.mainloop()
    except Exception as exc:
        print(f"main: fatal error: {exc}")
        raise


if __name__ == "__main__":
    main()
