import cv2
import threading

import tkinter as tk

from tkinter import ttk
from PIL import Image, ImageTk

class WakfuFarmingGUI:
    rectangle_match = None
    multi_rectangle_match = None
    result_match = None
    plain_img = None

    threshold_max = 1

    HMax=179
    VMax=255
    SMax=255
    HMin=179
    VMin=255
    SMin=255

    state = 0

    threshold_var = None
    match_type_var = None
    fps_label_var = None
    state_label_var = None
    matches_label_var = None

    window_name_var = None
    dir_resources_var = None
    dir_actions_var = None
    max_results_var = None
    groupThreshold_var = None
    eps_var = None
    window_width_var = None
    window_height_var = None

    reset_flag = False

    def __init__(self, root):
        self.root = root
        self.root.title("Wakfu Autofarming")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        self.tab_1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1, text="Threshold")
        self.create_tab_1()

        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="Match Type")
        self.create_tab_2()

        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text="Configuration")
        self.create_tab_3()

        self.notebook.select(self.tab_1)

        self.create_bottom_frame()

        self.capture_thread = threading.Thread(target=self.update_image, daemon=True)
        self.capture_thread.start()

    def create_tab_1(self):
        threshold_label = ttk.Label(self.tab_1, text="Threshold")
        self.threshold_var = tk.StringVar()
        self.threshold_slider = ttk.Scale(self.tab_1, from_=0, to=self.threshold_max, orient="horizontal", variable=self.threshold_var)
        threshold_input = ttk.Entry(self.tab_1, textvariable=self.threshold_var)
        threshold_label.grid(row=0, column=0, pady=5)
        self.threshold_slider.grid(row=0, column=1, pady=10)
        threshold_input.grid(row=0, column=2, pady=5)

        #HVS
        HMax_label = ttk.Label(self.tab_1, text="HMax")
        self.HMax_var = tk.StringVar()
        self.HMax_slider = ttk.Scale(self.tab_1, from_=0, to=self.HMax, orient="horizontal", variable=self.HMax_var)
        HMax_input = ttk.Entry(self.tab_1, textvariable=self.HMax_var)
        HMax_label.grid(row=1, column=0, pady=5)
        self.HMax_slider.grid(row=1, column=1, pady=10)
        HMax_input.grid(row=1, column=2, pady=5)
        
        VMax_label = ttk.Label(self.tab_1, text="VMax")
        self.VMax_var = tk.StringVar()
        self.VMax_slider = ttk.Scale(self.tab_1, from_=0, to=self.VMax, orient="horizontal", variable=self.VMax_var)
        VMax_input = ttk.Entry(self.tab_1, textvariable=self.VMax_var)
        VMax_label.grid(row=2, column=0, pady=5)
        self.VMax_slider.grid(row=2, column=1, pady=10)
        VMax_input.grid(row=2, column=2, pady=5)
        
        SMax_label = ttk.Label(self.tab_1, text="SMax")
        self.SMax_var = tk.StringVar()
        self.SMax_slider = ttk.Scale(self.tab_1, from_=0, to=self.SMax, orient="horizontal", variable=self.SMax_var)
        SMax_input = ttk.Entry(self.tab_1, textvariable=self.SMax_var)
        SMax_label.grid(row=3, column=0, pady=5)
        self.SMax_slider.grid(row=3, column=1, pady=10)
        SMax_input.grid(row=3, column=2, pady=5)

        #HSV - Min
        HMin_label = ttk.Label(self.tab_1, text="HMin")
        self.HMin_var = tk.StringVar()
        self.HMin_slider = ttk.Scale(self.tab_1, from_=0, to=self.HMin, orient="horizontal", variable=self.HMin_var)
        HMin_input = ttk.Entry(self.tab_1, textvariable=self.HMin_var)
        HMin_label.grid(row=4, column=0, pady=5)
        self.HMin_slider.grid(row=4, column=1, pady=10)
        HMin_input.grid(row=4, column=2, pady=5)
        
        VMin_label = ttk.Label(self.tab_1, text="VMin")
        self.VMin_var = tk.StringVar()
        self.VMin_slider = ttk.Scale(self.tab_1, from_=0, to=self.VMin, orient="horizontal", variable=self.VMin_var)
        VMin_input = ttk.Entry(self.tab_1, textvariable=self.VMin_var)
        VMin_label.grid(row=5, column=0, pady=5)
        self.VMin_slider.grid(row=5, column=1, pady=10)
        VMin_input.grid(row=5, column=2, pady=5)
        
        SMin_label = ttk.Label(self.tab_1, text="SMin")
        self.SMin_var = tk.StringVar()
        self.SMin_slider = ttk.Scale(self.tab_1, from_=0, to=self.SMin, orient="horizontal", variable=self.SMin_var)
        SMin_input = ttk.Entry(self.tab_1, textvariable=self.SMin_var)
        SMin_label.grid(row=6, column=0, pady=5)
        self.SMin_slider.grid(row=6, column=1, pady=10)
        SMin_input.grid(row=6, column=2, pady=5)

    def create_tab_2(self):
        match_type_label = ttk.Label(self.tab_2, text="Match type:")
        
        self.match_type_var = tk.StringVar()
        self.match_type_var.set(1)
        self.radio_TM_SQDIFF_NORMED = tk.Radiobutton(self.tab_2, text="TM_SQDIFF_NORMED", variable=self.match_type_var, value=1)
        self.radio_TM_CCORR_NORMED = tk.Radiobutton(self.tab_2, text="TM_CCORR_NORMED", variable=self.match_type_var, value=2)
        self.radio_TM_CCOEFF_NORMED = tk.Radiobutton(self.tab_2, text="TM_CCOEFF_NORMED", variable=self.match_type_var, value=3)

        match_type_label.grid(row=0, column=0)
        
        self.radio_TM_SQDIFF_NORMED.grid(row=1, column=0, padx=10)
        self.radio_TM_CCORR_NORMED.grid(row=1, column=1, padx=10)
        self.radio_TM_CCOEFF_NORMED.grid(row=1, column=2, padx=10)

    def create_tab_3(self):
        window_name_label = ttk.Label(self.tab_3, text="Process Name")
        self.window_name_var = tk.StringVar()
        window_name_text = ttk.Entry(self.tab_3, textvariable=self.window_name_var)
        window_name_label.grid(row=0, column=0)
        window_name_text.grid(row=0, column=1)

        dir_resources_label = ttk.Label(self.tab_3, text="Directory resources imgs")
        self.dir_resources_var = tk.StringVar()
        dir_resources_text = ttk.Entry(self.tab_3, textvariable=self.dir_resources_var)
        dir_resources_label.grid(row=1, column=0)
        dir_resources_text.grid(row=1, column=1)

        dir_actions_label = ttk.Label(self.tab_3, text="Directory actions imgs")
        self.dir_actions_var = tk.StringVar()
        dir_actions_text = ttk.Entry(self.tab_3, textvariable=self.dir_actions_var)
        dir_actions_label.grid(row=2, column=0)
        dir_actions_text.grid(row=2, column=1)
        
        max_results_label = ttk.Label(self.tab_3, text="Max results accept")
        self.max_results_var = tk.StringVar()
        max_results_text = ttk.Entry(self.tab_3, textvariable=self.max_results_var)
        max_results_label.grid(row=3, column=0)
        max_results_text.grid(row=3, column=1)

        max_groupThreshold_label = ttk.Label(self.tab_3, text="groupThreshold")
        self.groupThreshold_var = tk.StringVar()
        max_groupThreshold_text = ttk.Entry(self.tab_3, textvariable=self.groupThreshold_var)
        max_groupThreshold_label.grid(row=4, column=0)
        max_groupThreshold_text.grid(row=4, column=1)

        max_eps_label = ttk.Label(self.tab_3, text="eps")
        self.eps_var = tk.StringVar()
        max_eps_text = ttk.Entry(self.tab_3, textvariable=self.eps_var)
        max_eps_label.grid(row=5, column=0)
        max_eps_text.grid(row=5, column=1)

        max_window_width_label = ttk.Label(self.tab_3, text="Window width")
        self.window_width_var = tk.StringVar()
        max_window_width_text = ttk.Entry(self.tab_3, textvariable=self.window_width_var)
        max_window_width_label.grid(row=6, column=0)
        max_window_width_text.grid(row=6, column=1)

        max_window_height_label = ttk.Label(self.tab_3, text="Window height")
        self.window_height_var = tk.StringVar()
        max_window_height_text = ttk.Entry(self.tab_3, textvariable=self.window_height_var)
        max_window_height_label.grid(row=7, column=0)
        max_window_height_text.grid(row=7, column=1)

    def create_bottom_frame(self):
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(expand=1, fill="both")

        self.type_view_radio = tk.StringVar()
        self.type_view_radio.set(1)
        self.math_radio = tk.Radiobutton(self.bottom_frame, text="Match", variable=self.type_view_radio, value=1)
        self.multi_math_radio = tk.Radiobutton(self.bottom_frame, text="Multi Match", variable=self.type_view_radio, value=2)
        self.result_match_radio = tk.Radiobutton(self.bottom_frame, text="Result Match", variable=self.type_view_radio, value=3)
        self.plain_img_radio = tk.Radiobutton(self.bottom_frame, text="Plain Img", variable=self.type_view_radio, value=4)

        self.math_radio.grid(row=0, column=0, padx=10)
        self.multi_math_radio.grid(row=0, column=1, padx=10)
        self.result_match_radio.grid(row=0, column=2, padx=10)
        self.plain_img_radio.grid(row=0, column=3, padx=10)

        self.start_button = ttk.Button(self.bottom_frame, text="Start", command=self.start_action)
        self.start_button.grid(row = 1, column=1)

        self.start_button = ttk.Button(self.bottom_frame, text="Stop", command=self.stop_action)
        self.start_button.grid(row = 1, column=2)

        self.reset_button = ttk.Button(self.bottom_frame, text="Reload", command=self.reset_action)
        self.reset_button.grid(row = 1, column=3)

        self.image_label = ttk.Label(self.bottom_frame)
        self.image_label.grid(row=2, column=0, columnspan=4, pady=10)

        self.fps_label_var = tk.StringVar()
        self.fps_label = ttk.Label(self.bottom_frame, textvariable=self.fps_label_var)
        self.fps_label.grid(row=3, column=0)

        self.state_label_var = tk.StringVar()
        self.state_label = ttk.Label(self.bottom_frame, textvariable=self.state_label_var)
        self.state_label.grid(row=3, column=1)
        
        self.matches_label_var = tk.StringVar()
        self.matches_label = ttk.Label(self.bottom_frame, textvariable=self.matches_label_var)
        self.matches_label.grid(row=3, column=2)

    def update_image(self):
        while(True):
            img = self.get_image_to_show(self.type_view_radio.get())

            if img is not None:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (img.shape[1] // 4, img.shape[0] // 4))

                photo = ImageTk.PhotoImage(Image.fromarray(image))
                self.image_label.config(image=photo)
                self.image_label.image = photo

    def get_image_to_show(self, option):
        show = None
        
        if option == '1':
            show = self.rectangle_match
        elif option == '2':
            show = self.multi_rectangle_match
        elif option == '3':
            show = self.result_match
        elif option == '4':
            show = self.plain_img

        return show
    
    def start_action(self):
        self.state = 1
    
    def stop_action(self):
        self.state = 0
    
    def reset_action(self):
        self.state = 0
        self.reset_flag = True

def main():
    root = tk.Tk()
    app = WakfuFarmingGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()