import tkinter as tk
from tkinter import messagebox
import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []
        self.hits = 0
        self.direction = 'h'
        self.placed = False
        self.color = f"#{min(100 + size * 50, 255):02x}{min(100, 255):02x}{min(200 - size * 30, 255):02x}"
    
    def is_sunk(self):
        return self.hits == self.size

class SeaBattle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской Бой")
        self.root.resizable(False, False)
        
        self.BOARD_SIZE = 10
        self.CELL_SIZE = 30
        self.MARGIN = 2
        self.BOARD1_X = 50
        self.BOARD2_X = 400
        self.BOARD_Y = 80
        
        self.player_board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.enemy_board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        self.player_ships = [Ship(4)] + [Ship(3) for _ in range(2)] + [Ship(2) for _ in range(3)] + [Ship(1) for _ in range(4)]
        self.current_ship_index = 0
        self.placing_ships = True
        
        self.enemy_ships = [Ship(4)] + [Ship(3) for _ in range(2)] + [Ship(2) for _ in range(3)] + [Ship(1) for _ in range(4)]
        
        self.enemy_target_mode = False
        self.last_hit = None
        self.target_direction = None
        self.potential_targets = []
        
        self.game_over = False
        self.winner = None
        self.message = "Расставьте ваши корабли"
        
        self.setup_ui()
        self.place_enemy_ships()
        
    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightgray')
        self.canvas.pack()
        
        self.restart_btn = tk.Button(self.root, text="Перезапуск (R)", command=self.reset_game)
        self.restart_btn.pack(pady=5)
        
        self.root.bind('<KeyPress-r>', lambda e: self.reset_game())
        self.root.bind('<KeyPress-R>', lambda e: self.reset_game())
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        
        self.canvas.focus_set()
        
    def reset_game(self):
        self.player_board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.enemy_board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        self.player_ships = [Ship(4)] + [Ship(3) for _ in range(2)] + [Ship(2) for _ in range(3)] + [Ship(1) for _ in range(4)]
        self.current_ship_index = 0
        self.placing_ships = True
        
        self.enemy_ships = [Ship(4)] + [Ship(3) for _ in range(2)] + [Ship(2) for _ in range(3)] + [Ship(1) for _ in range(4)]
        
        self.enemy_target_mode = False
        self.last_hit = None
        self.target_direction = None
        self.potential_targets = []
        
        self.place_enemy_ships()
        
        self.game_over = False
        self.winner = None
        self.message = "Расставьте ваши корабли"
        
        self.draw_game()
    
    def place_enemy_ships(self):
        for ship in self.enemy_ships:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, self.BOARD_SIZE - 1)
                col = random.randint(0, self.BOARD_SIZE - 1)
                direction = random.choice(['h', 'v'])
                
                if self.can_place_ship(self.enemy_board, ship.size, row, col, direction):
                    self.place_ship_on_board(self.enemy_board, ship, row, col, direction)
                    placed = True
                attempts += 1
            
            if not placed:
                self.enemy_board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
                for s in self.enemy_ships:
                    s.positions = []
                    s.placed = False
                self.place_enemy_ships()
                return
    
    def can_place_ship(self, board, size, row, col, direction):
        if direction == 'h':
            if col + size > self.BOARD_SIZE:
                return False
            for i in range(size):
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r, c = row + dr, col + i + dc
                        if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                            if board[r][c] == 1:
                                return False
        else:
            if row + size > self.BOARD_SIZE:
                return False
            for i in range(size):
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        r, c = row + i + dr, col + dc
                        if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                            if board[r][c] == 1:
                                return False
        return True
    
    def place_ship_on_board(self, board, ship, row, col, direction):
        ship.positions = []
        ship.direction = direction
        
        if direction == 'h':
            for i in range(ship.size):
                board[row][col + i] = 1
                ship.positions.append((row, col + i))
        else:
            for i in range(ship.size):
                board[row + i][col] = 1
                ship.positions.append((row + i, col))
        
        ship.placed = True
    
    def draw_board(self, board, x_offset, show_ships=True):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x = x_offset + col * (self.CELL_SIZE + self.MARGIN)
                y = self.BOARD_Y + row * (self.CELL_SIZE + self.MARGIN)
                
                if board[row][col] == 0:
                    color = 'white'
                elif board[row][col] == 1 and show_ships:
                    color = 'blue'
                elif board[row][col] == 2:
                    color = 'lightgray'
                elif board[row][col] == 3:
                    color = 'red'
                else:
                    color = 'white'
                
                self.canvas.create_rectangle(x, y, x + self.CELL_SIZE, y + self.CELL_SIZE, 
                                           fill=color, outline='black')
                
                if board[row][col] == 2:
                    self.canvas.create_line(x + 5, y + 5, x + self.CELL_SIZE - 5, y + self.CELL_SIZE - 5, 
                                          width=2, fill='black')
                    self.canvas.create_line(x + self.CELL_SIZE - 5, y + 5, x + 5, y + self.CELL_SIZE - 5, 
                                          width=2, fill='black')
    
    def draw_ship_preview(self, x, y):
        if self.placing_ships and self.current_ship_index < len(self.player_ships):
            ship = self.player_ships[self.current_ship_index]
            col = (x - self.BOARD1_X) // (self.CELL_SIZE + self.MARGIN)
            row = (y - self.BOARD_Y) // (self.CELL_SIZE + self.MARGIN)
            
            if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
                can_place = self.can_place_ship(self.player_board, ship.size, row, col, ship.direction)
                color = 'lightgreen' if can_place else 'pink'
                
                if ship.direction == 'h':
                    for i in range(ship.size):
                        if col + i < self.BOARD_SIZE:
                            x_pos = self.BOARD1_X + (col + i) * (self.CELL_SIZE + self.MARGIN)
                            y_pos = self.BOARD_Y + row * (self.CELL_SIZE + self.MARGIN)
                            self.canvas.create_rectangle(x_pos, y_pos, 
                                                       x_pos + self.CELL_SIZE, 
                                                       y_pos + self.CELL_SIZE, 
                                                       fill=color, outline='black', width=2)
                else:
                    for i in range(ship.size):
                        if row + i < self.BOARD_SIZE:
                            x_pos = self.BOARD1_X + col * (self.CELL_SIZE + self.MARGIN)
                            y_pos = self.BOARD_Y + (row + i) * (self.CELL_SIZE + self.MARGIN)
                            self.canvas.create_rectangle(x_pos, y_pos, 
                                                       x_pos + self.CELL_SIZE, 
                                                       y_pos + self.CELL_SIZE, 
                                                       fill=color, outline='black', width=2)
    
    def draw_text(self):
        self.canvas.create_text(400, 30, text="МОРСКОЙ БОЙ", 
                               font=("Arial", 20, "bold"), fill='black')
        
        self.canvas.create_text(self.BOARD1_X + 150, self.BOARD_Y - 30, 
                               text="ВАШЕ ПОЛЕ", font=("Arial", 14, "bold"), fill='black')
        self.canvas.create_text(self.BOARD2_X + 150, self.BOARD_Y - 30, 
                               text="ПОЛЕ ПРОТИВНИКА", font=("Arial", 14, "bold"), fill='black')
        
        self.canvas.create_text(400, 500, text=self.message, 
                               font=("Arial", 14), fill='black')
        
        if self.placing_ships:
            instructions = "ЛКМ - разместить корабль, ПКМ - повернуть"
        else:
            instructions = "ЛКМ - выстрел"
        
        self.canvas.create_text(400, 550, text=instructions, 
                               font=("Arial", 10), fill='darkgray')
    
    def on_click(self, event):
        if self.game_over:
            return
            
        if self.placing_ships:
            self.handle_placing_ships(event.x, event.y)
        else:
            self.handle_player_shot(event.x, event.y)
        
        self.draw_game()
    
    def on_right_click(self, event):
        if self.placing_ships and self.current_ship_index < len(self.player_ships) and not self.game_over:
            ship = self.player_ships[self.current_ship_index]
            ship.direction = 'v' if ship.direction == 'h' else 'h'
            self.draw_game()
    
    def on_mouse_move(self, event):
        if self.placing_ships and not self.game_over:
            self.draw_game()
            self.draw_ship_preview(event.x, event.y)
    
    def handle_placing_ships(self, x, y):
        if self.current_ship_index >= len(self.player_ships):
            self.placing_ships = False
            self.message = "Ваш ход! Стреляйте по полю противника"
            return
        
        ship = self.player_ships[self.current_ship_index]

        col = (x - self.BOARD1_X) // (self.CELL_SIZE + self.MARGIN)
        row = (y - self.BOARD_Y) // (self.CELL_SIZE + self.MARGIN)
        
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.can_place_ship(self.player_board, ship.size, row, col, ship.direction):
                self.place_ship_on_board(self.player_board, ship, row, col, ship.direction)
                self.current_ship_index += 1
                
                if self.current_ship_index < len(self.player_ships):
                    ship_type = ""
                    if self.player_ships[self.current_ship_index].size == 4:
                        ship_type = "линкор"
                    elif self.player_ships[self.current_ship_index].size == 3:
                        ship_type = "крейсер"
                    elif self.player_ships[self.current_ship_index].size == 2:
                        ship_type = "эсминец"
                    else:
                        ship_type = "катер"
                    
                    self.message = f"Разместите {ship_type} размером {self.player_ships[self.current_ship_index].size}"
                else:
                    self.placing_ships = False
                    self.message = "Ваш ход! Стреляйте по полю противника"
    
    def handle_player_shot(self, x, y):
        col = (x - self.BOARD2_X) // (self.CELL_SIZE + self.MARGIN)
        row = (y - self.BOARD_Y) // (self.CELL_SIZE + self.MARGIN)
        
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.enemy_board[row][col] in [2, 3]:
                self.message = "Вы уже стреляли в эту клетку!"
                return False

            if self.enemy_board[row][col] == 1:
                self.enemy_board[row][col] = 3
                self.message = "Попадание!"

                for ship in self.enemy_ships:
                    if (row, col) in ship.positions:
                        ship.hits += 1
                        ship_type = ""
                        if ship.size == 4:
                            ship_type = "линкор"
                        elif ship.size == 3:
                            ship_type = "крейсер"
                        elif ship.size == 2:
                            ship_type = "эсминец"
                        else:
                            ship_type = "катер"
                        
                        if ship.is_sunk():
                            self.message = f"Вы потопили {ship_type} размером {ship.size}!"
                        break

                if all(ship.is_sunk() for ship in self.enemy_ships):
                    self.game_over = True
                    self.winner = "player"
                    self.message = "ПОЗДРАВЛЯЕМ! ВЫ ВЫИГРАЛИ!"
                    messagebox.showinfo("Победа!", "Поздравляем! Вы выиграли!")
                
                return True
            else:
                self.enemy_board[row][col] = 2
                self.message = "Промах!"
                
                self.enemy_turn()
                return True
        
        return False
    
    def enemy_turn(self):
        if self.enemy_target_mode and self.last_hit:
            row, col = self.get_target_shot()
        else:
            possible_moves = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) 
                             if self.player_board[r][c] not in [2, 3]]
            
            if possible_moves:
                row, col = random.choice(possible_moves)
            else:
                return
        
        if self.player_board[row][col] in [2, 3]:
            if self.enemy_target_mode:
                if self.potential_targets:
                    self.potential_targets.pop(0)
            self.enemy_turn()
            return
        
        if self.player_board[row][col] == 1:
            self.player_board[row][col] = 3
            self.message = "Противник попал!"

            self.enemy_target_mode = True
            self.last_hit = (row, col)
            
            self.add_potential_targets(row, col)

            for ship in self.player_ships:
                if (row, col) in ship.positions:
                    ship.hits += 1
                    ship_type = ""
                    if ship.size == 4:
                        ship_type = "линкор"
                    elif ship.size == 3:
                        ship_type = "крейсер"
                    elif ship.size == 2:
                        ship_type = "эсминец"
                    else:
                        ship_type = "катер"
                    
                    if ship.is_sunk():
                        self.message = f"Противник потопил ваш {ship_type} размером {ship.size}!"
                        self.enemy_target_mode = False
                        self.last_hit = None
                        self.target_direction = None
                        self.potential_targets = []
                    break

            if all(ship.is_sunk() for ship in self.player_ships):
                self.game_over = True
                self.winner = "enemy"
                self.message = "ВЫ ПРОИГРАЛИ!"
                messagebox.showinfo("Поражение", "Вы проиграли! Попробуйте еще раз.")
        else:
            self.player_board[row][col] = 2
            if self.enemy_target_mode:
                if self.potential_targets:
                    self.potential_targets.pop(0)
    
    def add_potential_targets(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if self.player_board[r][c] not in [2, 3] and (r, c) not in self.potential_targets:
                    self.potential_targets.append((r, c))
    
    def get_target_shot(self):
        self.potential_targets = [(r, c) for r, c in self.potential_targets 
                                if self.player_board[r][c] not in [2, 3]]
        
        if self.potential_targets:
            return self.potential_targets[0]
        
        self.enemy_target_mode = False
        self.last_hit = None
        possible_moves = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) 
                         if self.player_board[r][c] not in [2, 3]]
        return random.choice(possible_moves) if possible_moves else (0, 0)
    
    def draw_game(self):
        self.canvas.delete("all")
        
        self.draw_board(self.player_board, self.BOARD1_X, show_ships=True)
        self.draw_board(self.enemy_board, self.BOARD2_X, show_ships=False)
        
        self.draw_text()
    
    def run(self):
        self.draw_game()
        self.root.mainloop()

if __name__ == "__main__":
    game = SeaBattle()
    game.run()
