import threading

import tkinter as tk
from time import time
from tkinter import ttk

from libs.gui import WakfuFarmingGUI
from libs.window_capture import WindowCapture
from libs.search_on_img import SearchOnImg
from libs.load_files import LoadFiles
from libs.delay_bolean import DelayBolean
from libs import clicks

class Farming:
    threshold = 0.05
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

    app = None
    seacher = None
    delay = None

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

        app.threshold_var.set(self.threshold)
        app.match_type_var.set(self.match_type)
        app.window_name_var.set(self.window_name)
        app.fps_label_var.set(self.fps_label)
        app.state_label_var.set(self.state_label)
        app.dir_resources_var.set(self.dir_resources)
        app.dir_actions_var.set(self.dir_actions)
        app.max_results_var.set(self.max_results)
        app.groupThreshold_var.set(self.groupThreshold)
        app.eps_var.set(self.eps)

        self.seacher = SearchOnImg()
        self.delay = DelayBolean()

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
        capturer = WindowCapture(self.window_name)

        self.app.threshold_slider.set(self.threshold)
        self.app.HMax_slider.set(self.HMax)
        self.app.VMax_slider.set(self.VMax)
        self.app.SMax_slider.set(self.SMax)
        self.app.HMin_slider.set(self.HMin)
        self.app.VMin_slider.set(self.VMin)
        self.app.SMin_slider.set(self.SMin)

        while(True):
            capture = capturer.get_screenshot()

            self.state = self.app.state
            self.threshold = float(self.app.threshold_var.get())
            self.match_type = self.app.match_type_var.get()
            self.max_results = int(self.app.max_results_var.get()) if self.app.max_results_var.get() else 0
            self.groupThreshold = int(self.app.groupThreshold_var.get()) if self.app.groupThreshold_var.get() else 0
            self.eps = float(self.app.eps_var.get()) if self.app.eps_var.get() else 0

            self.HMax = float(self.app.HMax_var.get()) // 1 if self.app.HMax_var.get() else 0
            self.VMax = float(self.app.VMax_var.get()) // 1 if self.app.VMax_var.get() else 0
            self.SMax = float(self.app.SMax_var.get()) // 1 if self.app.SMax_var.get() else 0
            self.HMin = float(self.app.HMin_var.get()) // 1 if self.app.HMin_var.get() else 0
            self.VMin = float(self.app.VMin_var.get()) // 1 if self.app.VMin_var.get() else 0
            self.SMin = float(self.app.SMin_var.get()) // 1 if self.app.SMin_var.get() else 0
            
            if self.app is not None and self.app.state != 0:
                self.seacher.threshold = self.threshold
                self.seacher.match_type = self.match_type
                self.seacher.max_result = self.max_results
                self.seacher.groupThreshold = self.groupThreshold
                self.seacher.eps = self.eps

                if self.state == 1 and self.delay.wait():
                    for resource in self.img_resources:
                        x, y, match, multi_math, result_match, matches = self.seacher.search_template_on_img(capture, resource)
                        
                        self.app.rectangle_match = match
                        self.app.multi_rectangle_match = multi_math
                        self.app.result_match = result_match

                        self.app.matches_label_var.set(f'{self.last_detection_label}: {matches}')
                        
                    if x > 0 and y > 0:
                        clicks.right_click(x, y)
                        self.app.state = 2
                        self.delay.set_seconds(1)

                if self.state == 2 and self.delay.wait():
                    for resource in self.img_actions:
                        x, y, match, multi_math, result_match, matches = self.seacher.search_template_on_img(capture, resource)
                        
                        self.app.rectangle_match = match
                        self.app.multi_rectangle_match = multi_math
                        self.app.result_match = result_match

                        self.app.matches_label_var.set(f'{self.last_detection_label}: {matches}')
                        
                    if x > 0 and y > 0:
                        clicks.right_click(x, y)
                        self.app.state = 1
                        self.delay.set_seconds(4)

            self.app.fps_label_var.set(f'{self.fps_label}: {1/(time() - self.loop_time):.2f}')
            self.app.state_label_var.set(f'{self.state_label}: {self.state}')

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
