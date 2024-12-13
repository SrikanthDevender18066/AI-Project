import tkinter as tk
import heapq, math, random

ROW, COL, CELL_SIZE = 9, 10, 50

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return [row, col] == dest

def h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)

def trace_path(cell_details, dest, canvas):
    row, col = dest
    path = []
    while cell_details[row][col] != (row, col):
        path.append((row, col))
        row, col = cell_details[row][col]
    path.reverse()
    for r, c in path:
        canvas.itemconfig(f"cell_{r}_{c}", fill="blue")
    print(f"Path traced: {path}")  # Debug output

def a_star(grid, src, dest, canvas):
    open_list = [(0, *src)]
    closed_list = [[False] * COL for _ in range(ROW)]
    cell_details = [[(i, j) for j in range(COL)] for i in range(ROW)]
    g = [[float('inf')] * COL for _ in range(ROW)]
    g[src[0]][src[1]] = 0

    while open_list:
        _, i, j = heapq.heappop(open_list)
        if is_destination(i, j, dest):
            trace_path(cell_details, dest, canvas)
            return
        closed_list[i][j] = True

        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if is_valid(ni, nj) and is_unblocked(grid, ni, nj) and not closed_list[ni][nj]:
                g_new = g[i][j] + 1
                f_new = g_new + h_value(ni, nj, dest)
                if g_new < g[ni][nj]:
                    g[ni][nj] = g_new
                    heapq.heappush(open_list, (f_new, ni, nj))
                    cell_details[ni][nj] = (i, j)
    print("No path found.")  # Debug output if no path is found

def generate_grid(src, dest):
    grid = [[1 if random.random() > 0.3 else 0 for _ in range(COL)] for _ in range(ROW)]
    grid[src[0]][src[1]] = 1
    grid[dest[0]][dest[1]] = 1
    return grid

class AStarGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A* Pathfinding")
        self.src, self.dest = [8, 0], [0, 9]
        self.grid = generate_grid(self.src, self.dest)
        self.canvas = tk.Canvas(self, width=COL * CELL_SIZE, height=ROW * CELL_SIZE)
        self.canvas.pack()
        self.draw_grid()
        tk.Button(self, text="Start A*", command=self.start_search).pack()
        tk.Button(self, text="Restart", command=self.restart).pack()
        self.bind_keys()

    def draw_grid(self):
        for i in range(ROW):
            for j in range(COL):
                color = "white" if self.grid[i][j] else "black"
                self.canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE, fill=color, tags=f"cell_{i}_{j}")
        self.color_start_end()

    def color_start_end(self):
        self.canvas.itemconfig(f"cell_{self.src[0]}_{self.src[1]}", fill="green")
        self.canvas.itemconfig(f"cell_{self.dest[0]}_{self.dest[1]}", fill="red")

    def start_search(self):
        print("Starting A* search...")  # Debug output
        a_star(self.grid, self.src, self.dest, self.canvas)
        
    def restart(self):
        self.grid = generate_grid(self.src, self.dest)
        self.canvas.delete("all")
        self.draw_grid()

    def move(self, dy, dx):
        new_src = [self.src[0] + dy, self.src[1] + dx]
        if is_valid(new_src[0], new_src[1]) and is_unblocked(self.grid, new_src[0], new_src[1]):
            self.canvas.itemconfig(f"cell_{self.src[0]}_{self.src[1]}", fill="white")
            self.src = new_src
            self.color_start_end()

    def bind_keys(self):
        for k, (dy, dx) in {"<Left>": (0, -1), "<Right>": (0, 1), "<Up>": (-1, 0), "<Down>": (1, 0)}.items():
            self.bind(k, lambda e, d=(dy, dx): self.move(*d))
        self.focus_set()

if __name__ == "__main__":
    AStarGUI().mainloop()
