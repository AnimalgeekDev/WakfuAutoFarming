"""Entrypoint for the GUI application.

This module wires together config, capture, yolo wrapper, processor and UI.
It uses a background thread to ensure the GUI remains responsive and a single
`processing_image` flag to prevent concurrent image processing.
"""
import threading
import time
import traceback
import tkinter as tk

from PIL import Image
from app.config import load_config
from app.capture import capture_wakfu_window
from app.yolo_wrapper import YoloModel
from app.processor import transform_yolo_coordinates_to_original, compute_centers, overlay_boxes, overlay_centers
from app.actions import ActionController
from app.notifier import notify
from app.ui import AppUI


def main() -> None:
    try:
        cfg = load_config()

        root = tk.Tk()
        ui = AppUI(root)

        model = YoloModel()
        model.load(cfg.model_path, device=cfg.device, img_size=cfg.img_size)

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

        def worker_loop() -> None:    
            while True:
                if actions.processing_image:
                    time.sleep(0.02)
                    continue
                actions.processing_image = True
                
                try:
                    img = capture_wakfu_window(cfg.wakfu_process_name)
                    
                    width_org, height_org = img.size
                    
                    img_resize = img.resize((model.img_size, model.img_size), Image.Resampling.LANCZOS)
    
                    scal_x = width_org / model.img_size
                    scal_y = height_org / model.img_size
                    
                    detections = model.predict(img_resize, cfg.confidence_threshold)
                    
                    detections_org = transform_yolo_coordinates_to_original(detections, width_org, height_org, scal_x, scal_y, model.img_size)
                    
                    centers = compute_centers(detections_org)

                    ### AQUI VAMOS
                    # detect capitan_miau
                    for det in detections:
                        if det["label"] == "capitan_miau":
                            try:
                                notify("Capitan miau detectado", "Capitan miau detectado, se necesita intervención")
                            except Exception:
                                pass
                            ui.var_perform_actions.set(False)
                            actions.perform_actions = False
                            actions.set_waiting(False)
                            break

                    # overlay for UI
                    if ui.var_show_centers.get():
                        out = overlay_centers(img, centers)
                    else:
                        out = overlay_boxes(img, detections_org)
                    ui.update_image(out)

                    # actions flow
                    actions.perform_actions = ui.var_perform_actions.get()
                    img_w, img_h = img.size
                    center_ref = (img_w // 2, img_h // 2)

                    # if perform_actions and not waiting_for_actions -> find nearest box and right-click
                    if actions.perform_actions and not actions.waiting_for_actions:
                        idx = find_nearest_index(centers, center_ref)
                        if idx != -1:
                            cx, cy = centers[idx]
                            try:
                                actions.simulate_right_click(cx, cy)
                            except Exception:
                                pass
                            time.sleep(1.0)
                            actions.set_waiting(True)

                    # if waiting_for_actions, look for get_seed/get_item and click left
                    if actions.waiting_for_actions:
                        # check timeout of waiting (5000 ms)
                        import time as _time

                        now = _time.time()
                        if actions.waiting_since is not None and (now - actions.waiting_since) * 1000.0 > 5000.0:
                            try:
                                notify("Sin acciones?", "Sin acciones?")
                            except Exception:
                                pass
                            actions.set_waiting(False)
                        else:
                            # find get_seed or get_item in detections
                            target_idx = -1
                            target_label = None
                            for i, det in enumerate(detections):
                                if det["label"] == "get_seed":
                                    target_idx = i
                                    target_label = "get_seed"
                                    break
                            if target_idx == -1:
                                for i, det in enumerate(detections):
                                    if det["label"] == "get_item":
                                        target_idx = i
                                        target_label = "get_item"
                                        break
                            if target_idx != -1:
                                tx1, ty1, tx2, ty2 = detections[target_idx]["xyxy"]
                                tx = int((tx1 + tx2) / 2)
                                ty = int((ty1 + ty2) / 2)
                                try:
                                    actions.simulate_left_click(tx, ty)
                                except Exception:
                                    pass
                                # pause 4 seconds after left click
                                time.sleep(4.0)
                                actions.set_waiting(False)

                except Exception:
                    traceback.print_exc()
                finally:
                    actions.processing_image = False
                time.sleep(0.05)

        # import helper now to avoid circular import
        from app.processor import find_nearest_index

        thread = threading.Thread(target=worker_loop, daemon=True)
        thread.start()

        root.mainloop()
    except Exception as exc:
        # single try/except as requested in specs
        print(f"main: fatal error: {exc}")
        raise


if __name__ == "__main__":
    main()
