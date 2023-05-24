import customtkinter as ctk
import time

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.start_point = None
        self.end_point = None
        self.delay = 0.1
        self.stop_search_flag = False

        # configure window
        self.title("The Path Pioneers")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="The Path Pioneers", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.credits = ctk.CTkLabel(self.sidebar_frame, text="Created by Max Bodifee & Louis Luu")
        self.credits.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")

        self.start_button = ctk.CTkButton(self.sidebar_frame, text="Start", command=self.start_search)
        self.start_button.grid(row=2, column=0, padx=20, pady=10)

        self.stop_button = ctk.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_search)
        self.stop_button.grid(row=3, column=0, padx=20, pady=10)

        self.reset_grid_button = ctk.CTkButton(self.sidebar_frame, text="Reset Grid", command=self.reset_grid)
        self.reset_grid_button.grid(row=4, column=0, padx=20, pady=10)

        self.timer_label = ctk.CTkLabel(self.sidebar_frame, text="Timer: 0 seconds")
        self.timer_label.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=8, column=0, padx=20, pady=(0, 10))
        self.appearance_mode_option_menu.set("System")

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.scaling_option_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=10, column=0, padx=20, pady=(0, 20))
        self.scaling_option_menu.set("100%")

        self.grid_display = ctk.CTkFrame(self)
        self.grid_display.grid(row=0, column=1, padx=50, pady=25, sticky="w")
        self.grid_display.grid_columnconfigure(tuple(range(15)), weight=1)

        # frame for grid controls
        self.grid_controls = ctk.CTkFrame(self, corner_radius=20)
        self.grid_controls.grid(row=0, column=2, sticky="nw")

        # item selector, *Don't Modify Values Argument*
        self.items = ctk.CTkSegmentedButton(self.grid_controls)
        self.items.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="ew")
        self.items.configure(values=["Wall Piece", "Start Tile", "End Tile"])
        self.items.set("Wall Piece")

        # slider for user to decide how to big the square grid should be
        self.grid_size = ctk.CTkSlider(self.grid_controls, from_=3, to=15, number_of_steps=12, command=self.update_label)
        self.grid_size.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="ew")
        self.new_grid()

        # label to show grid size
        self.grid_size_label = ctk.CTkLabel(self.grid_controls, text="Grid Size: 9")
        self.grid_size_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # button to generate new grid
        self.new_grid_button = ctk.CTkButton(self.grid_controls, text="Create New Grid", command=self.new_grid)
        self.new_grid_button.grid(row=1, column=1, padx=(0, 20), pady=(20, 0), sticky="ew")

        self.set_delay = ctk.CTkEntry(self.grid_controls, placeholder_text="0.1")
        self.set_delay.grid(row=3, column=0, padx=(20, 0), pady=10, sticky="w")
        self.set_delay.bind('<Button-1>', lambda event: self.set_delay.focus_set())
        self.set_delay.bind('<Escape>', lambda event: self.focus_set())

        self.set_delay_button = ctk.CTkButton(self.grid_controls, text="Set Delay", command=self.update_delay)
        self.set_delay_button.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.strip("%")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def update_label(self, *args):
        self.grid_size_label.configure(text=f"Grid Size: {int(self.grid_size.get())}")

    def update_delay(self):
        self.set_delay_button.focus_set()

        try:
            self.delay = float(self.set_delay.get())

        except ValueError:
            pass

    # overwrite and generate new grid
    def new_grid(self):
        n = 9

        if int(self.grid_size.get()) != n:
            n = int(self.grid_size.get())

        self.reset_grid()

        for child in self.grid_display.winfo_children():
            child.grid_forget()

        for row in range(n):
            for column in range(n):
                tile = ctk.CTkButton(self.grid_display, width=40, height=40, corner_radius=2, fg_color="white",
                                     text_color="black", text_color_disabled="black", hover=False,
                                     text="", font=ctk.CTkFont(size=15))
                tile.configure(command=lambda tle=tile: self.tile_click(tle))
                tile.grid(row=row, column=column, padx=2, pady=2)
                tile.bind("<B1-Motion>", self.tile_drag)

    def tile_click(self, tile):
        item = self.items.get()
        tile_position = (tile.grid_info()['column'], tile.grid_info()['row'])

        if item == "Wall Piece":
            if tile_position == self.start_point:
                self.reset_tile(self.start_point)

            if tile_position == self.end_point:
                self.reset_tile(self.end_point)

            if tile.cget("fg_color") == "black":
                self.reset_tile(tile_position)

            else:
                tile.configure(fg_color="black")

        elif item == "Start Tile":
            if self.start_point is not None:
                self.reset_tile(self.start_point)

            self.start_point = tile_position
            tile.configure(text="Start", fg_color="light blue")
            if self.start_point == self.end_point:
                self.end_point = None

        elif item == "End Tile":
            if self.end_point is not None:
                self.reset_tile(self.end_point)

            self.end_point = tile_position
            tile.configure(text="End", fg_color="light blue")

            if self.end_point == self.start_point:
                self.start_point = None

    def tile_drag(self, event):
        self.tile_click(event.widget)

    def reset_tile(self, position):
        column, row = position
        self.grid_display.grid_slaves(row=row, column=column)[0].configure(fg_color="white", text="")

    def astar_search(self, nodes: dict):
        tic = time.perf_counter()
        open_nodes = set()
        closed_nodes = set()

        open_nodes.add(nodes[self.start_point])

        while open_nodes:
            toc = time.perf_counter()
            self.timer_label.configure(text=f"Timer: {toc - tic:0.4f} seconds")

            if self.stop_search_flag:
                return

            current_node = min(open_nodes, key=lambda node: node.f())
            if current_node.position == self.end_point:
                self.trace_steps(current_node)
                self.timer_label.configure(text=f"Timer: {toc - tic:0.4f} seconds")
                return

            open_nodes.remove(current_node)
            closed_nodes.add(current_node)

            x, y = current_node.position

            if current_node.position != self.start_point:
                self.grid_display.grid_slaves(row=y, column=x)[0].configure(fg_color="red")

            successors = [nodes.get((x + dx, y + dy), None) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                          if not (dx, dy) == (0, 0)]

            for successor in successors:
                if successor in closed_nodes or successor is None:
                    continue

                successor_x, successor_y = successor.position
                dx, dy = abs(successor_x - x), abs(successor_y - y)
                cost = 10 if dx == 0 or dy == 0 else 14
                if current_node.g + cost < successor.g or successor not in open_nodes:
                    successor.g = current_node.g + cost
                    successor.h_cost(self.end_point)
                    successor.parent = current_node

                    if successor not in open_nodes:
                        open_nodes.add(successor)
                        if successor.position not in [self.start_point, self.end_point]:
                            self.grid_display.grid_slaves(row=successor_y, column=successor_x)[0].configure(fg_color="green")

            self.update()
            time.sleep(self.delay)

    def trace_steps(self, node):
        if node.parent is None:
            return

        x, y = node.position
        self.grid_display.grid_slaves(row=y, column=x)[0].configure(fg_color="light blue")
        self.update_idletasks()
        time.sleep(self.delay)
        self.trace_steps(node.parent)

    def start_search(self):
        self.stop_search()
        self.stop_search_flag = False

        self.start_button.configure(state=ctk.DISABLED)
        if self.start_point is not None and self.end_point is not None:
            nodes = {}
            for tile in self.grid_display.grid_slaves():
                tile.configure(state=ctk.DISABLED)
                tile_position = (tile.grid_info()['column'], tile.grid_info()['row'])

                if tile.cget("fg_color") != "black":
                    nodes[tile_position] = Node(tile_position)

            self.astar_search(nodes)

        self.start_button.configure(state=ctk.NORMAL)

    def stop_search(self):
        self.stop_search_flag = True
        for tile in self.grid_display.grid_slaves():
            tile_position = (tile.grid_info()['column'], tile.grid_info()['row'])
            if tile.cget("fg_color") != "black" and tile_position not in [self.start_point, self.end_point]:
                tile.configure(fg_color="white")

            tile.configure(state=ctk.NORMAL)

    def reset_grid(self):
        self.start_point, self.end_point = None, None
        for tile in self.grid_display.grid_slaves():
            tile.configure(fg_color="white", text="", state=ctk.NORMAL)


class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h

    def f(self):
        return self.g + self.h

    def h_cost(self, goal_state):
        x1, y1 = self.position
        x2, y2 = goal_state

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        self.h = 14 * min(dx, dy) + 10 * max(dx, dy) - min(dx, dy)


if __name__ == "__main__":
    app = App()
    app.mainloop()