import tkinter as tk
from tkinter import messagebox
 
class TicTacToe:
   def __init__(self):
       self.window = tk.Tk()
       self.window.title("Крестики-нолики")
       self.current_player = "X"
       self.board = [["" for _ in range(3)] for _ in range(3)]
       self.buttons = [[None for _ in range(3)] for _ in range(3)]
       self.create_board()
       
   def create_board(self):
       for row in range(3):
           for col in range(3):
               button = tk.Button(
                   self.window,
                   text="",
                   font=("normal", 20),
                   width=6,
                   height=3,
                   command=lambda r=row, c=col: self.on_click(r, c)
               )
               button.grid(row=row, column=col)
               self.buttons[row][col] = button
 
   def on_click(self, row, col):
       if self.board[row][col] == "" and not self.check_game_over():
           self.make_move(row, col, "X")
           if not self.check_game_over():
               self.bot_move()
 
   def make_move(self, row, col, player):
       self.board[row][col] = player
       self.buttons[row][col].config(text=player, state="disabled")
 
   def bot_move(self):
       best_score = float('-inf')
       best_move = None
       
       for row in range(3):
           for col in range(3):
               if self.board[row][col] == "":
                   self.board[row][col] = "O"
                   score = self.minimax(False)
                   self.board[row][col] = ""
                   
                   if score > best_score:
                       best_score = score
                       best_move = (row, col)
       
       if best_move:
           self.make_move(best_move[0], best_move[1], "O")
       self.check_game_over()
 
   def minimax(self, is_maximizing):
       winner = self.check_winner()
       if winner == "O":
           return 1
       elif winner == "X":
           return -1
       elif self.is_board_full():
           return 0
 
       if is_maximizing:
           best_score = float('-inf')
           for row in range(3):
               for col in range(3):
                   if self.board[row][col] == "":
                       self.board[row][col] = "O"
                       score = self.minimax(False)
                       self.board[row][col] = ""
                       best_score = max(score, best_score)
           return best_score
       else:
           best_score = float('inf')
           for row in range(3):
               for col in range(3):
                   if self.board[row][col] == "":
                       self.board[row][col] = "X"
                       score = self.minimax(True)
                       self.board[row][col] = ""
                       best_score = min(score, best_score)
           return best_score
 
   def check_winner(self):
       for row in range(3):
           if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
               return self.board[row][0]

       for col in range(3):
           if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
               return self.board[0][col]
       
       if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
           return self.board[0][0]
       if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
           return self.board[0][2]
       
       return None
 
   def is_board_full(self):
       for row in range(3):
           for col in range(3):
               if self.board[row][col] == "":
                   return False
       return True
 
   def check_game_over(self):
       winner = self.check_winner()
       if winner:
           messagebox.showinfo("Игра окончена", f"Победил {winner}!")
           self.reset_game()
           return True
       elif self.is_board_full():
           messagebox.showinfo("Игра окончена", "Ничья!")
           self.reset_game()
           return True
       return False

   def reset_game(self):
       self.current_player = "X"
       self.board = [["" for _ in range(3)] for _ in range(3)]
       for row in range(3):
           for col in range(3):
               self.buttons[row][col].config(text="", state="normal")
 
   def run(self):
       self.window.mainloop()
 
if __name__ == "__main__":
   game = TicTacToe()
   game.run()
