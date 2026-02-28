"""Tkinter-based user interface for the WakfuAutoFarming app.

The UI implements the layout described in the spec: 4 vertical sections,
controls and an image preview area. The actual image updating logic is
handled by `main.py` which will call into UI methods to update the preview.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from PIL import Image, ImageTk


class AppUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("WakfuAutoFarming")
        self.root.geometry("450x500")
        # Mantener la ventana siempre en primer plano
        self.root.attributes("-topmost", True)
        self._position_bottom_right()

        # State variables
        self.var_perform_actions = tk.BooleanVar(value=False)
        self.var_show_centers = tk.BooleanVar(value=False)

        # Widgets
        self._build_widgets()

    def _position_bottom_right(self) -> None:
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = 450
        win_h = 500
        x = screen_w - win_w
        y = screen_h - win_h
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    def _build_widgets(self) -> None:
        # Area 1: checkboxes
        frame_top = ttk.Frame(self.root)
        frame_top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Checkbutton(frame_top, text="Realizar acciones", variable=self.var_perform_actions).pack(anchor=tk.W)
        ttk.Checkbutton(frame_top, text="Mostrar centros", variable=self.var_show_centers).pack(anchor=tk.W)

        # Area 2: instruction text (hidden until actions enabled)
        self.instruction = ttk.Label(self.root, text="presione Q para detener acciones")
        self.instruction.pack(padx=8, pady=4)
        self._update_instruction_visibility()

        # Area 3: image preview
        self.preview_container = ttk.Frame(self.root, width=450, height=250)
        self.preview_container.pack_propagate(False)
        self.preview_container.pack(padx=8, pady=6)
        self.preview_label = ttk.Label(self.preview_container, text="NO IMAGE")
        self.preview_label.pack(expand=True)

        # Area 4: exit button
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=8, pady=10)
        ttk.Button(btn_frame, text="Salir", command=self.root.quit).pack()

        # Bind variable trace
        self.var_perform_actions.trace_add("write", lambda *_: self._update_instruction_visibility())

    def _update_instruction_visibility(self) -> None:
        if self.var_perform_actions.get():
            self.instruction.configure(text="presione Q para detener acciones")
            self.instruction.pack_configure()
        else:
            self.instruction.pack_forget()

    def update_image(self, pil_image: Optional[Image.Image]) -> None:
        """Update the preview area with a PIL image or show NO IMAGE if None.

        Args:
            pil_image: image to show, or None.
        """
        if pil_image is None:
            self.preview_label.configure(text="NO IMAGE", image="")
            return
        # Resize to fit preview (450x250) while preserving aspect
        img_resized = pil_image.resize((450, 250))
        tk_img = ImageTk.PhotoImage(img_resized)
        self.preview_label.configure(image=tk_img, text="")
        self.preview_label.image = tk_img
