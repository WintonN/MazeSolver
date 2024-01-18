import tkinter as tk
import time

from maze_env import MazeEnv

"""
Graphical Visualiser for a maze.
"""


class GUI:

    TILE_W = 32
    TILE_H = 32
    TILE_W_SMALL = 16
    TILE_H_SMALL = 16

    UPDATE_DELAY = 0.5
    TWEEN_STEPS = 16
    TWEEN_DELAY = 0.005

    def __init__(self, maze_env):
        self.maze_env = maze_env
        init_state = maze_env.get_init_state()
        self.last_state = init_state
        self.last_searched = None
        self.cost = 0

        # choose small or large mode
        self.window = tk.Tk()
        screen_width, screen_height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        if (screen_width < self.maze_env.n_cols * self.TILE_W) or (screen_height < self.maze_env.n_rows * self.TILE_H):
            small_mode = True
            self.tile_w = self.TILE_W_SMALL
            self.tile_h = self.TILE_H_SMALL
        else:
            small_mode = False
            self.tile_w = self.TILE_W
            self.tile_h = self.TILE_H

        self.window.title("Maze Solver Visualiser")
        self.window.geometry(f'{self.maze_env.n_cols * self.tile_w}x{(self.maze_env.n_rows * self.tile_h) + 20}')

        # Create a label widget
        self.label = tk.Label(self.window, text=f"Optimal Path Cost: {self.maze_env.optimal_cost} || Current Path Cost: {self.cost}", width=100, anchor="center", fg="black", bg="white", font=('Helvetica 15'))

        # Pack the label widget to display it
        self.label.pack()
        self.canvas = tk.Canvas(self.window)
        self.canvas.configure(bg="white")
        self.canvas.pack(fill="both", expand=True)

        # load images
        if small_mode:
            self.tile_current = tk.PhotoImage(file='gui_assets/tile_current_search_small.png')
            self.tile_path = tk.PhotoImage(file='gui_assets/tile_path_small.png')
            self.tile_searched = tk.PhotoImage(file='gui_assets/tile_searched_small.png')
            self.tile_exit = tk.PhotoImage(file='gui_assets/tile_exit_small.png')
            self.wall = tk.PhotoImage(file='gui_assets/wall_small.png')
            self.tile_empty = tk.PhotoImage(file='gui_assets/tile_empty_small.png')
            self.player = tk.PhotoImage(file='gui_assets/player_small.png')
        else:
            self.tile_current = tk.PhotoImage(file='gui_assets/tile_current_search.png')
            self.tile_path = tk.PhotoImage(file='gui_assets/tile_path.png')
            self.tile_searched = tk.PhotoImage(file='gui_assets/tile_searched.png')
            self.tile_exit = tk.PhotoImage(file='gui_assets/tile_exit.png')
            self.wall = tk.PhotoImage(file='gui_assets/wall.png')
            self.tile_empty = tk.PhotoImage(file='gui_assets/tile_empty.png')
            self.player = tk.PhotoImage(file='gui_assets/player.png')
        
        # draw background (all permanent features, i.e. everything except player)
        for r in range(self.maze_env.n_rows):
            for c in range(self.maze_env.n_cols):
                if self.maze_env.grid_data[r][c] == MazeEnv.SOLID_TILE:
                    self.canvas.create_image((c * self.tile_w), (r * self.tile_h), image=self.wall, anchor=tk.NW)
                if self.maze_env.grid_data[r][c] == MazeEnv.AIR_TILE:
                    self.canvas.create_image((c * self.tile_w), (r * self.tile_h), image=self.tile_empty, anchor=tk.NW)
                if r == self.maze_env.exit_row and c == self.maze_env.exit_col:
                    self.canvas.create_image((c * self.tile_w), (r * self.tile_h), image=self.tile_exit, anchor=tk.NW)

        # draw player position for initial state
        self.player_image = None
        self.add_path(self.last_state.row, self.last_state.col)
        self.draw_player(init_state.row, init_state.col)

        self.window.update()
        self.last_update_time = time.time()

    def update_state(self, state):
        self.cost += 1
        self.label.configure(text=f"Optimal Path Cost: {self.maze_env.optimal_cost} || Current Path Cost: {self.cost}")
        # remove and re-draw player
        self.canvas.delete(self.player_image)
        # tween player to new position
        self.add_path(state.row, state.col)
        for i in range(1, self.TWEEN_STEPS + 1):
            time.sleep(self.TWEEN_DELAY)
            self.canvas.delete(self.player_image)
            r1 = self.last_state.row + (i / self.TWEEN_STEPS) * (state.row - self.last_state.row)
            c1 = self.last_state.col + (i / self.TWEEN_STEPS) * (state.col - self.last_state.col)
            # remove old player position, draw new player position
            self.draw_player(r1, c1)
            self.window.update()
        self.last_state = state

        # delay until next update
        self.window.update()

        time_since_last_update = time.time() - self.last_update_time
        time.sleep(max(self.UPDATE_DELAY - time_since_last_update, 0))
        self.last_update_time = time.time()

    def add_path(self, row, col):
        self.canvas.create_image((col * self.tile_w), (row * self.tile_h), image=self.tile_path, anchor=tk.NW)

    def draw_player(self, row, col):
        self.player_image = self.canvas.create_image((col * self.tile_w), (row * self.tile_h),
                                                     image=self.player, anchor=tk.NW)
    
    def remove_player(self):
        self.player_image = None
        if self.cost == self.maze_env.optimal_cost:
            text = f"Maze Completed - Path Cost: {self.cost} || Optimal Path Taken"
        else:
            text = f"Maze Completed - Path Cost: {self.cost} || Optimal Path Not Taken - Optimal Path Cost: " + \
            f"{self.maze_env.optimal_cost}"
        self.label.configure(text=text)
        self.window.update()