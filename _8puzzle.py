import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq

# Đồ thị chuyển trạng thái của trò chơi
GRAPH = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

# Trạng thái mục tiêu
GOAL_STATE = [1, 2, 3, 6, 5, 4, 7, 8, 0]

class PuzzleGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("8 Puzzle")
        self.geometry("640x460")

        self.cell_size = 120
        self.gap_size = 10

        self.font = ("Helvetica", 35)
        self.font_size = ("Helvetica", 16)

        self.start_state = [1, 2, 3, 0, 8, 7, 6, 4, 5]
        self.step_count = 0

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="red")
        self.canvas.pack()

        self.draw_board()

        self.function_frame = tk.Frame(self)
        self.function_frame.pack(side=tk.RIGHT, padx=10)

        btn_solve_a_star = tk.Button(self.function_frame, text="A*", command=lambda: self.solve_puzzle("A*"), font=("Helvetica", 14, "bold"), bg="NavajoWhite2", width=18)
        btn_solve_a_star.pack(side=tk.TOP, pady=10)

        btn_solve_greedy = tk.Button(self.function_frame, text="Greedy", command=lambda: self.solve_puzzle("Greedy"), font=("Helvetica", 14, "bold"), bg="Aquamarine1", width=18)
        btn_solve_greedy.pack(side=tk.TOP, pady=10)

        btn_solve_bfs = tk.Button(self.function_frame, text="BFS", command=lambda: self.solve_puzzle("BFS"), font=("Helvetica", 14, "bold"), bg="OliveDrab1", width=18)
        btn_solve_bfs.pack(side=tk.TOP, pady=10)

        btn_solve_ucs = tk.Button(self.function_frame, text="UCS", command=lambda: self.solve_puzzle("UCS"), font=("Helvetica", 14, "bold"), bg="RosyBrown2", width=18)
        btn_solve_ucs.pack(side=tk.TOP, pady=10)

        btn_solve_dfs = tk.Button(self.function_frame, text="DFS", command=lambda: self.solve_puzzle("DFS"), font=("Helvetica", 14, "bold"), bg="Orchid1", width=18)
        btn_solve_dfs.pack(side=tk.TOP, pady=10)

        btn_reset = tk.Button(self.function_frame, text="Reset", command=self.reset_puzzle, font=("Helvetica", 14, "bold"), bg="Turquoise1", width=18)
        btn_reset.pack(side=tk.TOP, pady=10)

        self.step_label = tk.Label(self.function_frame, text=f"Bước: {self.step_count}", font=self.font_size, fg="white", bg="red", width=19)
        self.step_label.pack(side=tk.TOP, pady=10)

        self.explored_label = tk.Label(self.function_frame, text="Đỉnh đã duyệt: 0", font=self.font_size, fg="white", bg="red", width=19)
        self.explored_label.pack(side=tk.TOP, pady=10)

        self.bind("<Up>", lambda event: self.move(0, -1))
        self.bind("<Down>", lambda event: self.move(0, 1))
        self.bind("<Left>", lambda event: self.move(-1, 0))
        self.bind("<Right>", lambda event: self.move(1, 0))

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(3):
            for j in range(3):
                value = self.start_state[i * 3 + j]
                if value != 0:
                    x = j * self.cell_size + (j + 1) * self.gap_size
                    y = i * self.cell_size + (i + 1) * self.gap_size
                    self.canvas.create_rectangle(
                        x, y, x + self.cell_size, y + self.cell_size, fill="white"
                    )
                    self.canvas.create_text(
                        x + self.cell_size // 2,
                        y + self.cell_size // 2,
                        text=str(value),
                        font=self.font,
                        fill="green",
                    )

    def move(self, dx, dy):
        zero_index = self.start_state.index(0)
        target_index = zero_index + dy * 3 + dx

        if 0 <= target_index < 9:
            self.start_state[zero_index], self.start_state[target_index] = (
                self.start_state[target_index],
                self.start_state[zero_index],
            )
            self.step_count += 1
            self.draw_board()

            if self.start_state == GOAL_STATE:
                messagebox.showinfo("Chúc mừng!", "Câu đố đã được giải!")

            # Cập nhật số bước đi trên nhãn
            self.step_label.config(text=f"Bước: {self.step_count}")

    def solve_puzzle(self, algorithm):
        if algorithm == "A*":
            solution, explored_nodes = self.a_star_8puzzle(self.start_state, GOAL_STATE)
        elif algorithm == "Greedy":
            solution, explored_nodes = self.greedy_8puzzle(self.start_state, GOAL_STATE)
        elif algorithm == "BFS":
            solution, explored_nodes = self.bfs_8puzzle(self.start_state, GOAL_STATE)
        elif algorithm == "UCS":
            solution, explored_nodes = self.ucs_8puzzle(self.start_state, GOAL_STATE)
        elif algorithm == "DFS":
            solution, explored_nodes = self.dfs_8puzzle(self.start_state, GOAL_STATE)
        else:
            messagebox.showerror("Lỗi", "Thuật toán không hợp lệ.")
            return

        if solution:
            self.after(500, lambda: self.animate_solution(solution, explored_nodes, 0))

    def reset_puzzle(self):
        self.start_state = [1, 2, 3, 0, 8, 7, 6, 4, 5]
        self.step_count = 0
        self.draw_board()
        self.step_label.config(text=f"Bước: {self.step_count}")
        self.explored_label.config(text="Đỉnh đã duyệt: 0")

    def a_star_8puzzle(self, start_state, goal_state):
        queue = deque([(start_state, [], 0)])
        visited = set()
        explored_nodes = 0

        while queue:
            current_state, path, cost = queue.popleft()
            visited.add(tuple(current_state))
            explored_nodes += 1

            if current_state == goal_state:
                return path, explored_nodes

            possible_moves = self.get_possible_moves(current_state)
            for new_state in possible_moves:
                if tuple(new_state) not in visited:
                    new_cost = cost + 1
                    heuristic = self.calculate_heuristic(new_state, goal_state)
                    total_cost = new_cost + heuristic
                    queue.append((new_state, path + [new_state], new_cost))

            queue = deque(sorted(queue, key=lambda x: len(x[1]) + self.calculate_heuristic(x[0], goal_state)))

        return None, explored_nodes

    def greedy_8puzzle(self, start_state, goal_state):
        queue = deque([(start_state, [], 0)])
        visited = set()
        explored_nodes = 0

        while queue:
            current_state, path, cost = queue.popleft()
            visited.add(tuple(current_state))
            explored_nodes += 1

            if current_state == goal_state:
                return path, explored_nodes

            possible_moves = self.get_possible_moves(current_state)
            for new_state in possible_moves:
                if tuple(new_state) not in visited:
                    heuristic = self.calculate_heuristic(new_state, goal_state)
                    queue.append((new_state, path + [new_state], heuristic))

            queue = deque(sorted(queue, key=lambda x: x[2]))

        return None, explored_nodes

    def bfs_8puzzle(self, start_state, goal_state):
        queue = deque([(start_state, [], 0)])
        visited = set()
        explored_nodes = 0

        while queue:
            current_state, path, cost = queue.popleft()
            visited.add(tuple(current_state))
            explored_nodes += 1

            if current_state == goal_state:
                return path, explored_nodes

            possible_moves = self.get_possible_moves(current_state)
            for new_state in possible_moves:
                if tuple(new_state) not in visited:
                    new_cost = cost + 1
                    queue.append((new_state, path + [new_state], new_cost))

        return None, explored_nodes

    def dfs_8puzzle(self, start_state, goal_state, max_depth=30):
        stack = [(start_state, [], 0)]
        visited = set()
        explored_nodes = 0

        while stack:
            current_state, path, depth = stack.pop()
            visited.add(tuple(current_state))
            explored_nodes += 1

            if current_state == goal_state:
                return path, explored_nodes

            if depth < max_depth:
                possible_moves = self.get_possible_moves(current_state)
                for new_state in possible_moves:
                    if tuple(new_state) not in visited:
                        stack.append((new_state, path + [new_state], depth + 1))

        return None, explored_nodes

    def ucs_8puzzle(self, start_state, goal_state):
        heap = [(0, start_state, [])]
        visited = set()
        explored_nodes = 0

        while heap:
            cost, current_state, path = heapq.heappop(heap)
            visited.add(tuple(current_state))
            explored_nodes += 1

            if current_state == goal_state:
                return path, explored_nodes

            possible_moves = self.get_possible_moves(current_state)
            for new_state in possible_moves:
                if tuple(new_state) not in visited:
                    new_cost = cost + 1
                    heapq.heappush(heap, (new_cost, new_state, path + [new_state]))

        return None, explored_nodes

    def get_possible_moves(self, state):
        zero_index = state.index(0)
        possible_moves = []
        for neighbor in GRAPH[zero_index]:
            new_state = state[:]
            new_state[zero_index], new_state[neighbor] = new_state[neighbor], new_state[zero_index]
            possible_moves.append(new_state)
        return possible_moves

    def calculate_heuristic(self, state, goal_state):
        heuristic = 0
        for i in range(1, 9):
            if state.index(i) != goal_state.index(i):
                heuristic += 1
        return heuristic

    def animate_solution(self, solution, explored_nodes, step_index):
        if step_index < len(solution):
            self.start_state = solution[step_index]
            self.step_count += 1
            self.draw_board()
            self.step_label.config(text=f"Bước: {self.step_count}")
            self.explored_label.config(text=f"Đỉnh đã duyệt: {explored_nodes}")
            self.after(50, lambda: self.animate_solution(solution, explored_nodes, step_index + 1))

if __name__ == "__main__":
    app = PuzzleGame()
    app.resizable(width=False, height=False) 
    app.mainloop()
