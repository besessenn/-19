import tkinter as tk
from tkinter import messagebox
import time
import random

class MazeGame:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.cell_size = 30
        self.window = tk.Tk()
        self.window.title("Редактируемый лабиринт с тремя выходами")

        self.canvas = tk.Canvas(self.window, 
                               width=self.width * self.cell_size,
                               height=self.height * self.cell_size + 40,
                               bg='white')
        self.canvas.pack(pady=10)
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Найти путь", command=self.find_path).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить путь", command=self.clear_path).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Сбросить лабиринт", command=self.reset_maze).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Случайный лабиринт", command=self.generate_random_maze).pack(side=tk.LEFT, padx=5)

        self.maze = [[0 for _ in range(width)] for _ in range(height)]
        self.start_pos = (width // 2, 1)
        
        self.end_pos1 = (1, height-2)
        self.end_pos2 = (width // 2, height-2)
        self.end_pos3 = (width-2, height-2)
        
        self.maze[self.start_pos[1]][self.start_pos[0]] = 2
        self.maze[self.end_pos1[1]][self.end_pos1[0]] = 3
        self.maze[self.end_pos2[1]][self.end_pos2[0]] = 3
        self.maze[self.end_pos3[1]][self.end_pos3[0]] = 3
        
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.draw_maze()
        
    def draw_maze(self):
        self.canvas.delete("all")
        
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.maze[y][x] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='gray')
                elif self.maze[y][x] == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='gray')
                    self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text="S")
                elif self.maze[y][x] == 3:
                    if (x, y) == self.end_pos1:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='gray')
                        self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text="E1")
                    elif (x, y) == self.end_pos2:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='orange', outline='gray')
                        self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text="E2")
                    elif (x, y) == self.end_pos3:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='purple', outline='gray')
                        self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text="E3")
                elif self.maze[y][x] == 4:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightblue', outline='gray')
                elif self.maze[y][x] == 5:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='gray')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='gray')
                    
        legend_y = self.height * self.cell_size + 20
        self.canvas.create_text(50, legend_y, text="S - Старт", fill='green')
        self.canvas.create_text(150, legend_y, text="E1 - Выход 1", fill='red')
        self.canvas.create_text(250, legend_y, text="E2 - Выход 2", fill='orange')
        self.canvas.create_text(350, legend_y, text="E3 - Выход 3", fill='purple')
    
    def on_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if (x, y) != self.start_pos and (x, y) != self.end_pos1 and (x, y) != self.end_pos2 and (x, y) != self.end_pos3:
            if self.maze[y][x] == 0:
                self.maze[y][x] = 1
            elif self.maze[y][x] == 1:
                self.maze[y][x] = 0
            
            self.draw_maze()
    
    def find_path(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] in [4, 5]:
                    self.maze[y][x] = 0

        self.maze[self.start_pos[1]][self.start_pos[0]] = 2
        self.maze[self.end_pos1[1]][self.end_pos1[0]] = 3
        self.maze[self.end_pos2[1]][self.end_pos2[0]] = 3
        self.maze[self.end_pos3[1]][self.end_pos3[0]] = 3

        stack = [self.start_pos]
        visited = set()
        visited.add(self.start_pos)
        parent = {}  
        
        found = False
        found_exit = None
        
        while stack and not found:
            current = stack.pop()
            x, y = current

            if current == self.end_pos1:
                found = True
                found_exit = ("E1", "красный", self.end_pos1)
                break
            elif current == self.end_pos2:
                found = True
                found_exit = ("E2", "оранжевый", self.end_pos2)
                break
            elif current == self.end_pos3:
                found = True
                found_exit = ("E3", "фиолетовый", self.end_pos3)
                break

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    (nx, ny) not in visited and 
                    self.maze[ny][nx] != 1):
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current

            if current != self.start_pos and current not in [self.end_pos1, self.end_pos2, self.end_pos3]:
                self.maze[y][x] = 5
                self.draw_maze()
                self.window.update()
                time.sleep(0.03)
        
        if found:
            exit_name, exit_color, exit_pos = found_exit
            path = []
            current = exit_pos
            while current != self.start_pos:
                path.append(current)
                current = parent[current]
            path.reverse()

            for x, y in path:
                if (x, y) != exit_pos:
                    self.maze[y][x] = 4
            self.draw_maze()
            
            messagebox.showinfo("Успех", f"Путь найден до выхода {exit_name} ({exit_color})!")
        else:
            messagebox.showinfo("Неудача", "Путь к любому из выходов не найден!")
    
    def clear_path(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] in [4, 5]:
                    self.maze[y][x] = 0

        self.maze[self.start_pos[1]][self.start_pos[0]] = 2
        self.maze[self.end_pos1[1]][self.end_pos1[0]] = 3
        self.maze[self.end_pos2[1]][self.end_pos2[0]] = 3
        self.maze[self.end_pos3[1]][self.end_pos3[0]] = 3
        self.draw_maze()
    
    def reset_maze(self):
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.maze[self.start_pos[1]][self.start_pos[0]] = 2
        self.maze[self.end_pos1[1]][self.end_pos1[0]] = 3
        self.maze[self.end_pos2[1]][self.end_pos2[0]] = 3
        self.maze[self.end_pos3[1]][self.end_pos3[0]] = 3
        self.draw_maze()
    
    def generate_random_maze(self):
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

        stack = [self.start_pos]
        self.maze[self.start_pos[1]][self.start_pos[0]] = 0
        
        while stack:
            x, y = stack[-1]

            neighbors = []
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.maze[ny][nx] == 1):
                    neighbors.append((nx, ny, dx//2, dy//2))
            
            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)

                self.maze[y + wy][x + wx] = 0
                self.maze[ny][nx] = 0
                
                stack.append((nx, ny))
            else:
                stack.pop()

        for exit_pos in [self.end_pos1, self.end_pos2, self.end_pos3]:
            x, y = exit_pos
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.maze[ny][nx] = 0

        self.maze[self.start_pos[1]][self.start_pos[0]] = 2
        self.maze[self.end_pos1[1]][self.end_pos1[0]] = 3
        self.maze[self.end_pos2[1]][self.end_pos2[0]] = 3
        self.maze[self.end_pos3[1]][self.end_pos3[0]] = 3
        self.draw_maze()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = MazeGame(25, 20)
    game.run()
