import os
import tkinter as tk
from tkinter import font
from tkinter.font import Font

class Authorization(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Реверси by Иван Коцан")
        self.canvas = tk.Canvas(self, width=400, height=550)
        self.canvas.pack()
        x = (self.winfo_screenwidth() - 400) // 2
        y = (self.winfo_screenheight() - 550) // 2
        self.geometry(f"400x550+{x}+{y}")
        bold_font = Font(family="Arial", size=12, weight="bold")
        self.label = tk.Label(self,
                         text="Добро пожаловать в игру Реверси!\nДля начала игры пройдите процедуру\nавторизации/регистрации",
                         font=bold_font)
        self.label.config(justify=tk.CENTER)
        self.label_username = tk.Label(self, text="Введите имя пользователя:")
        self.label_password = tk.Label(self, text="Введите пароль:")
        self.login = tk.Entry(self, width=30)
        self.password = tk.Entry(self, width=30, show="•")
        self.button_register = tk.Button(self, text="Регистрация/авторизация", command=self.regist)

        self.label.place(x=42, y=100)
        self.login.place(x=112, y=300)
        self.password.place(x=112, y=350)
        self.label_username.place(x=125, y=280)
        self.label_password.place(x=155, y=330)
        self.button_register.place(x=125, y=400)

    def regist(self):
        getlogin = self.login.get()
        getpass = self.password.get()
        if (len(getpass) == 0 or len(getlogin) == 0):
            self.show_info('Вы оставили пустым поле "Логин" и/или "Пароль"', "Повторить ввод")
        else:
            f_reg = False
            file_path = 'accounts.txt'
            if os.path.exists(file_path):
                file = open(file_path, "r+")
                text = file.read().split("\n")
                for j in range(len(text) - 1):
                    if (text[j] == ""):
                        continue
                    str = text[j].split();
                    if str[0] == getlogin and str[1] == getpass:
                        f_reg = True
                        break
                    elif str[0] == getlogin and str[1] != getpass:
                        f_reg = "nopass"
                file.close()
            else:
                with open(file_path, 'w') as file:
                    file.write('')
            if (f_reg == "nopass"):
                self.show_info(getlogin + ", Вы указали неверный пароль.", "Повторить попытку")
            else:
                if not f_reg:
                    file = open(file_path, "r+")
                    file.seek(0, os.SEEK_END)
                    file.write(getlogin + ' ' + getpass + '\n')
                    file.close()
                    self.show_info("Добро пожаловать, " + getlogin + ". Вы успешно зарегистрировались.", "Начать игру!")
                else:
                    self.show_info("С возвращением, " + getlogin + ". Вы успешно авторизовались.", "Начать игру!")
                self.label_username.place_forget()
                self.label_password.place_forget()
                self.login.place_forget()
                self.password.place_forget()
                self.button_register.place_forget()

    def press(self, win_t, auth):  # функция нажатия кнопки в информационном окне
        win_t.grab_release()
        win_t.destroy()
        if auth == 1:
            self.destroy()
            game = ReversiGame()
            game.mainloop()

    def show_info(self, text0, button0): #функция отображения информации при авторизации/регистрации
        if button0 == "Начать игру!":
            auth = 1
        else:
            auth = 0
        info = tk.Toplevel(self)
        info.title("Информация")
        screen_width = info.winfo_screenwidth()
        screen_height = info.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (200 // 2)
        info.geometry(f'500x200+{x}+{y}')
        info.minsize(width=500, height=200)
        info.maxsize(width=500, height=200)
        info.protocol("WM_DELETE_WINDOW", lambda: self.press(info, auth))
        bold_font = Font(family="Arial", size=12, weight="bold")
        label = tk.Label(info, text=text0, font=bold_font)
        label.pack()
        label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        but = tk.Button(info, text=button0, command=lambda: self.press(info, auth))
        but.place(x=200, y=125)
        info.grab_set()

BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

class ReversiGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.kol_black = 2 # кол-во чёрных шашек
        self.kol_white = 2 # кол-во белых шашек
        self.symma = 4 # сумма всех шашек
        self.win = "" # игрок, у которого больше шашек
        self.yes = 0 # может ли текущий игрок сделать ход
        self.mode_ii = "none" # уровень ИИ (none, lite, medium)
        custom_font = font.Font(family="Times New Roman", size=14)
        custom_font2 = font.Font(family="Times New Roman", size=12)
        self.title("Реверси by Иван Коцан")
        self.canvas = tk.Canvas(self, width=400, height=550)
        self.canvas.pack()
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current_player = BLACK
        self.infowhite = tk.Label(self, text="Белые - 2", font=custom_font)
        self.infowhite.place(x=50, y=405)
        self.infoblack = tk.Label(self, text="Чёрные - 2", font=custom_font)
        self.infoblack.place(x=250, y=405)
        self.odds = tk.Label(self, text="=", font=custom_font)
        self.odds.place(x=198, y=405)
        self.thelp = tk.Label(self, text="Подсказка: чёрные делают ход", font=custom_font2)
        self.thelp.place(x=5, y=435)
        self.button = tk.Button(self, text="Новая игра",command=self.new_game)
        self.button.place(x=150, y=500, width=100, height=30)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        x = (self.winfo_screenwidth() - 400) // 2
        y = (self.winfo_screenheight() - 550) // 2
        self.geometry(f"400x550+{x}+{y}")

    def new_game(self):
        self.destroy()
        self.__init__()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                if self.board[row][col] == BLACK:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black")
                elif self.board[row][col] == WHITE:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")

    def on_click(self, event):
        if event.y > 400:
            return
        row = event.y // 50
        col = event.x // 50
        if self.is_valid_move(row, col):
            self.make_move(row, col)
            self.draw_board()

    def is_valid_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == self.get_opponent():
                x += dx
                y += dy
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == self.current_player:
                    return True
        return False

    def get_opponent(self):
        return WHITE if self.current_player == BLACK else BLACK

    def check_move(self):
        self.yes = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == EMPTY:
                    if self.is_valid_move(row, col):
                        self.yes = 1
                        self.movex, self.movey = row, col
                        break
        return True if self.yes == 1 else False

    def make_ii_move(self):
        if self.mode_ii == "lite":
            if self.check_move():
                self.make_move(self.movex, self.movey)

    def cur_player(self):
        return "белые" if self.current_player == WHITE else "чёрные"
    def other_player(self):
        return "чёрные" if self.current_player == WHITE else "белые"

    def make_move(self, row, col):
        if self.current_player == WHITE:
            self.kol_white = self.kol_white + 1
        else:
            self.kol_black = self.kol_black + 1
        self.board[row][col] = self.current_player
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == self.get_opponent():
                x += dx
                y += dy
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == self.current_player:
                    while (x, y) != (row, col):
                        x -= dx
                        y -= dy
                        if self.board[x][y] != self.current_player:
                            if self.current_player == WHITE:
                                self.kol_white += 1
                                self.kol_black -= 1
                            else:
                                self.kol_white -= 1
                                self.kol_black += 1
                        self.board[x][y] = self.current_player
        self.current_player = self.get_opponent()
        self.infowhite.config(text="Белые - " + str(self.kol_white))
        self.infoblack.config(text="Чёрные - " + str(self.kol_black))
        if self.kol_white > self.kol_black:
            self.odds.config(text=">")
            self.win = "Белые"
            self.infowhite.config(fg="green")
            self.infoblack.config(fg="black")
        elif self.kol_white < self.kol_black:
            self.odds.config(text="<")
            self.win = "Чёрные"
            self.infoblack.config(fg="green")
            self.infowhite.config(fg="black")
        else:
            self.odds.config(text="=")
            if self.win == "Чёрные":
                self.infoblack.config(fg="black")
            else:
                self.infowhite.config(fg="black")
        self.symma = self.kol_white + self.kol_black
        if self.symma == 64:
            if self.kol_black != self.kol_white:
                self.thelp.config(text="Игра окончена: " + self.win + " победили!")
            else:
                self.thelp.config(text="Игра окончена в ничью!")
            return
        else:
            if not self.check_move():
                self.thelp.config(text="Подсказка: " + self.cur_player() + " не могут сделать ход,\nпоэтому сейчас ходят " + self.other_player())
                self.current_player = self.get_opponent()
                if not self.check_move(): #никто не может сделать ход
                    self.thelp.config(text="Игра окончена: " + self.win + " победили!\nТак как никто не мог сделать ход")
                    return
                if self.current_player == WHITE and self.mode_ii != "none":
                    self.make_ii_move()
                return
            if self.kol_white == 0:
                self.thelp.config(text="Игра окончена: Чёрные победили,\nтак как у белых не осталось шашек на поле")
                return
            elif self.kol_black == 0:
                self.thelp.config(text="Игра окончена: Белые победили,\nтак как у чёрных не осталось шашек на поле")

        if self.current_player == WHITE:
            self.thelp.config(text="Подсказка: белые делают ход")
            if self.mode_ii != "none":
                self.make_ii_move()
        else:
            self.thelp.config(text="Подсказка: чёрные делают ход")

if __name__ == "__main__":
    auth = Authorization()
    auth.mainloop()