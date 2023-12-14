import threading

import tkinter as tk
from time import time
from tkinter import ttk

from libs.gui import WakfuFarmingGUI
from libs.window_capture import WindowCapture
from libs.search_on_img import SearchOnImg
from libs.load_files import LoadFiles
from libs.delay_bolean import DelayBolean
from libs.utils import Utils
from libs import clicks

class Farming:
    threshold_resource = 0.05
    threshold_action = 0.05
    match_type = '1'
    fps_label = "FPS"
    state_label = "STATE"
    last_detection_label = "LAST DETECTION"

    window_name = "WAKFU"
    dir_resources="resource_img"
    dir_actions="farming_actions"
    max_results = 1000

    groupThreshold=1
    eps=0.5
    window_width=1920
    window_height=1080
    run_autofarming=True

    app = None
    capturer = None
    seacher = None
    delay = None
    utils = None

    routes_resources = []
    img_resources = []
    routes_actions = []
    img_actions = []

    loop_time = time()
    state = 0

    HMax=0
    VMax=0
    SMax=0
    HMin=0
    VMin=0
    SMin=0

    def __init__(self, app: WakfuFarmingGUI):
        self.app = app

        app.threshold_resource_var.set(self.threshold_resource)
        app.threshold_action_var.set(self.threshold_action)
        app.match_type_var.set(self.match_type)
        app.window_name_var.set(self.window_name)
        app.fps_label_var.set(self.fps_label)
        app.state_label_var.set(self.state_label)
        app.dir_resources_var.set(self.dir_resources)
        app.dir_actions_var.set(self.dir_actions)
        app.max_results_var.set(self.max_results)
        app.groupThreshold_var.set(self.groupThreshold)
        app.eps_var.set(self.eps)
        app.window_width_var.set(self.window_width)
        app.window_height_var.set(self.window_height)
        app.run_autofarming_var.set(self.run_autofarming)

        self.seacher = SearchOnImg()
        self.delay = DelayBolean()
        self.utils = Utils()

        self.load_assets()

        self.thread = threading.Thread(target=self.start_capture, daemon=True)
        self.thread.start()

    def load_assets(self):
        loader = LoadFiles()
        self.routes_resources = loader.get_templates(self.dir_resources)
        self.img_resources = loader.import_templates(self.routes_resources)

        self.routes_actions = loader.get_templates(self.dir_actions)
        self.img_actions = loader.import_templates(self.routes_actions)
    
    def start_capture(self):
        self.app.threshold_resource_slider.set(self.threshold_resource)
        self.app.threshold_action_slider.set(self.threshold_action)
        self.app.HMax_slider.set(self.HMax)
        self.app.VMax_slider.set(self.VMax)
        self.app.SMax_slider.set(self.SMax)
        self.app.HMin_slider.set(self.HMin)
        self.app.VMin_slider.set(self.VMin)
        self.app.SMin_slider.set(self.SMin)

        while(True):
            self.capturer = WindowCapture(self.window_name)
            self.capturer.w = self.window_width
            self.capturer.h = self.window_height
            
            capture = self.capturer.get_screenshot()

            self.state = self.app.state

            self.threshold_resource = float(self.app.threshold_resource_var.get()) if self.utils.is_float(self.app.threshold_resource_var.get()) else 0
            self.threshold_action = float(self.app.threshold_action_var.get()) if self.utils.is_float(self.app.threshold_action_var.get()) else 0
            self.HMax = int(float(self.app.HMax_var.get()) // 1) if self.utils.is_int(self.app.HMax_var.get()) else 0
            self.VMax = int(float(self.app.VMax_var.get()) // 1) if self.utils.is_int(self.app.VMax_var.get()) else 0
            self.SMax = int(float(self.app.SMax_var.get()) // 1) if self.utils.is_int(self.app.SMax_var.get()) else 0
            self.HMin = int(float(self.app.HMin_var.get()) // 1) if self.utils.is_int(self.app.HMin_var.get()) else 0
            self.VMin = int(float(self.app.VMin_var.get()) // 1) if self.utils.is_int(self.app.VMin_var.get()) else 0
            self.SMin = int(float(self.app.SMin_var.get()) // 1) if self.utils.is_int(self.app.SMin_var.get()) else 0
            
            self.match_type = self.app.match_type_var.get()
            
            self.max_results = int(float(self.app.max_results_var.get()) // 1) if self.utils.is_int(self.app.max_results_var.get()) else 0
            self.groupThreshold = int(float(self.app.groupThreshold_var.get()) // 1) if self.utils.is_int(self.app.groupThreshold_var.get()) else 0
            self.eps = float(self.app.eps_var.get()) if self.utils.is_float(self.app.eps_var.get()) else 0
            self.window_width = int(float(self.app.window_width_var.get()) // 1) if self.utils.is_int(self.app.window_width_var.get()) else 0
            self.window_height = int(float(self.app.window_height_var.get()) // 1) if self.utils.is_int(self.app.window_height_var.get()) else 0
            self.run_autofarming = bool(int(self.app.run_autofarming_var.get()))
            
            if self.app is not None and self.app.state != 0:
                self.seacher.match_type = self.match_type
                self.seacher.max_result = self.max_results
                self.seacher.groupThreshold = self.groupThreshold
                self.seacher.eps = self.eps

                if self.state == 1 and self.delay.wait():
                    for resource in self.img_resources:
                        x, y, match, multi_math, result_match, matches = self.seacher.search_template_on_img(capture, resource, self.threshold_resource)
                        
                        self.app.rectangle_match = match
                        self.app.multi_rectangle_match = multi_math
                        self.app.result_match = result_match

                        self.app.matches_label_var.set(f'{self.last_detection_label}: {matches}')
                        
                    if x > 0 and y > 0:
                        if self.run_autofarming:
                            clicks.right_click(x, y)
                            self.app.state = 2
                            self.delay.set_seconds(1)

                if self.state == 2 and self.delay.wait():
                    for resource in self.img_actions:
                        x, y, match, multi_math, result_match, matches = self.seacher.search_template_on_img(capture, resource, self.threshold_action)
                        
                        self.app.rectangle_match = match
                        self.app.multi_rectangle_match = multi_math
                        self.app.result_match = result_match

                        self.app.matches_label_var.set(f'{self.last_detection_label}: {matches}')
                        
                    if x > 0 and y > 0:
                        if self.run_autofarming:
                            clicks.right_click(x, y)
                            self.app.state = 1
                            self.delay.set_seconds(4)

            self.app.fps_label_var.set(f'{self.fps_label}: {1/(time() - self.loop_time if time() - self.loop_time > 0 else 1):.2f}')
            self.app.state_label_var.set(f'{self.state_label}: {"Search Resource" if self.state == 1 else "Search Action" if self.state == 2 else "Waiting"}')

            self.loop_time = time()            
            self.app.plain_img = capture

            if self.app.reset_flag:
                self.load_assets()

                self.app.reset_flag = False

def main():
    root = tk.Tk()
    app = WakfuFarmingGUI(root)
    Farming(app)

    root.mainloop()

if __name__ == "__main__":
    main()
