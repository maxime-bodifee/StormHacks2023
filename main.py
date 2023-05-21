import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.item_selected = None
        self.item_buttons = []

        self.start_point = True
        self.end_point = True

        # configure window
        self.title("StormHacks 2023 Project")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Path Finder", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Wall Piece")
        self.sidebar_button_1.configure(command=lambda btn=self.sidebar_button_1: self.select_item(btn))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.item_buttons.append(self.sidebar_button_1)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Start Point")
        self.sidebar_button_2.configure(command=lambda btn=self.sidebar_button_2: self.select_item(btn))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.item_buttons.append(self.sidebar_button_2)

        self.sidebar_button_2_label = ctk.CTkLabel(self.sidebar_frame, text=f"Remaining: {int(self.start_point)}")
        self.sidebar_button_2_label.grid(row=3, column=0, padx=20, pady=(0, 5))

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="End Point")
        self.sidebar_button_3.configure(command=lambda btn=self.sidebar_button_3: self.select_item(btn))
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=(5, 0))
        self.item_buttons.append(self.sidebar_button_3)

        self.sidebar_button_3_label = ctk.CTkLabel(self.sidebar_frame, text=f"Remaining: {int(self.end_point)}")
        self.sidebar_button_3_label.grid(row=5, column=0, padx=20, pady=(0, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(0, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.scaling_option_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=10, column=0, padx=20, pady=(0, 20))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.strip("%")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def select_item(self, item_button):
        for button in self.item_buttons:
            if button == item_button:
                button.configure(state=ctk.DISABLED)
                self.item_selected = button.cget("text")
                print(self.item_selected)
            else:
                button.configure(state=ctk.NORMAL)


if __name__ == "__main__":
    app = App()
    app.mainloop()
