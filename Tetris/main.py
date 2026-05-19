from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class TetrisGame:

    def __init__(self, root):

        self.root = root

        # НАСТРОЙКИ ИГРЫ
        self.WIDTH = 10
        self.HEIGHT = 20
        self.CELL = 30

        self.score = 0
        self.lines_cleared = 0

        self.level = 1
        self.speed = 500

        self.game_running = False
        # ОКНО

        self.root.title("Тетрис")
        self.root.geometry("470x630")
        self.root.resizable(0, 0)

        # ФОН
        try:

            image = Image.open(
                "large_134324.jpg"
            )

            image = image.resize((470, 630))

            self.background_image = ImageTk.PhotoImage(image)

            self.background_label = Label(
                self.root,
                image=self.background_image
            )

            self.background_label.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

        except:

            self.root.configure(bg="gray")

        # МЕНЮ
        self.menu_frame = Frame(self.root, bg="black")

        self.menu_frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER
        )

        self.title_label = Label(
            self.menu_frame,
            text="ТЕТРИС",
            font=("Arial", 28, "bold"),
            bg="black",
            fg="white"
        )

        self.title_label.pack(pady=20)

        # ИГРОВОЙ ЭКРАН
        self.game_frame = Frame(self.root, bg="black")

        # CANVAS
        self.canvas = Canvas(
            self.game_frame,
            width=self.WIDTH * self.CELL,
            height=self.HEIGHT * self.CELL,
            bg="black",
            highlightthickness=2,
            highlightbackground="white"
        )

        self.canvas.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        # БОКОВАЯ ПАНЕЛЬ
        self.side_frame = Frame(
            self.game_frame,
            bg="black"
        )

        self.side_frame.grid(
            row=0,
            column=0,
            sticky="n",
            padx=10
        )

        self.score_label = Label(
            self.side_frame,
            text="Очки: 0",
            font=("Arial", 16),
            bg="black",
            fg="white"
        )

        self.score_label.pack(pady=10)

        self.level_label = Label(
            self.side_frame,
            text="Уровень: 1",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )

        self.level_label.pack(pady=10)

        self.restart_btn = Button(
            self.side_frame,
            text="Заново",
            command=self.start_game,
            font=("Arial", 14),
            width=10,
            bd=0
        )

        self.restart_btn.pack(pady=15)

        self.exit_game_btn = Button(
            self.side_frame,
            text="Выйти",
            command=self.exit_game,
            font=("Arial", 14),
            width=10,
            bd=0
        )

        self.exit_game_btn.pack(pady=15)

        # КНОПКИ МЕНЮ
        self.btn = Button(
            self.menu_frame,
            text="Играть",
            command=self.start_game,
            font=("Arial", 18),
            width=12,
            bd=0
        )

        self.btn.pack(pady=20)

        self.btn_exit = Button(
            self.menu_frame,
            text="Выйти",
            command=self.exit_game,
            font=("Arial", 18),
            width=12,
            bd=0
        )

        self.btn_exit.pack(pady=20)

        # ИГРОВОЕ ПОЛЕ
        self.board = []

        for y in range(self.HEIGHT):

            row = []

            for x in range(self.WIDTH):
                row.append(0)

            self.board.append(row)

        # ФИГУРЫ
        self.shapes = [

            [[1, 1, 1, 1]],

            [[1, 1],
             [1, 1]],

            [[0, 1, 0],
             [1, 1, 1]],

            [[1, 0, 0],
             [1, 1, 1]],

            [[0, 0, 1],
             [1, 1, 1]],

            [[1, 1, 0],
             [0, 1, 1]],

            [[0, 1, 1],
             [1, 1, 0]]
        ]

        self.colors = [
            "cyan",
            "yellow",
            "purple",
            "blue",
            "orange",
            "green",
            "red"
        ]

        # ТЕКУЩАЯ ФИГУРА
        self.current_shape = None
        self.current_color = None

        self.current_x = 0
        self.current_y = 0

        # КЛАВИШИ
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Down>", self.move_fast)
        self.root.bind("<Up>", self.rotate)

    # СОЗДАНИЕ ФИГУРЫ
    def new_shape(self):

        index = random.randint(0, len(self.shapes) - 1)

        self.current_shape = self.shapes[index]
        self.current_color = self.colors[index]

        self.current_x = (
            self.WIDTH // 2 - len(self.current_shape[0]) // 2
        )

        self.current_y = 0

        if self.collision(self.current_x, self.current_y):
            self.game_over()

    # ПРОВЕРКА СТОЛКНОВЕНИЯ
    def collision(self, x, y):

        for row in range(len(self.current_shape)):

            for col in range(len(self.current_shape[row])):

                if self.current_shape[row][col]:

                    new_x = x + col
                    new_y = y + row

                    if new_x < 0 or new_x >= self.WIDTH:
                        return True

                    if new_y >= self.HEIGHT:
                        return True

                    if (
                        new_y >= 0 and
                        self.board[new_y][new_x]
                    ):
                        return True

        return False

    # ФИКСАЦИЯ ФИГУРЫ
    def fix_shape(self):

        for row in range(len(self.current_shape)):

            for col in range(len(self.current_shape[row])):

                if self.current_shape[row][col]:

                    self.board[
                        self.current_y + row
                    ][
                        self.current_x + col
                    ] = self.current_color

        self.clear_lines()

        self.new_shape()

    # УДАЛЕНИЕ ЛИНИЙ
    def clear_lines(self):

        new_board = []

        cleared = 0

        for row in self.board:

            if 0 not in row:
                cleared += 1
            else:
                new_board.append(row)

        while len(new_board) < self.HEIGHT:
            new_board.insert(0, [0] * self.WIDTH)

        self.board = new_board

        if cleared > 0:

            self.lines_cleared += cleared

            self.score += cleared * 100

            self.score_label.config(
                text=f"Очки: {self.score}"
            )

            self.level = (
                self.lines_cleared // 5
            ) + 1

            self.level_label.config(
                text=f"Уровень: {self.level}"
            )

            self.speed = 500 - (self.level - 1) * 50

            if self.speed < 100:
                self.speed = 100

    # РИСОВАНИЕ
    def draw(self):

        self.canvas.delete("all")

        for y in range(self.HEIGHT):

            for x in range(self.WIDTH):

                color = self.board[y][x]

                if color:
                    self.draw_cell(x, y, color)

        for row in range(len(self.current_shape)):

            for col in range(len(self.current_shape[row])):

                if self.current_shape[row][col]:

                    self.draw_cell(
                        self.current_x + col,
                        self.current_y + row,
                        self.current_color
                    )

    # РИСОВАНИЕ КЛЕТКИ
    def draw_cell(self, x, y, color):

        x1 = x * self.CELL
        y1 = y * self.CELL

        x2 = x1 + self.CELL
        y2 = y1 + self.CELL

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline="white"
        )

    # ДВИЖЕНИЕ ВНИЗ
    def move_down(self):

        if not self.game_running:
            return

        if not self.collision(
            self.current_x,
            self.current_y + 1
        ):

            self.current_y += 1

        else:

            self.fix_shape()

        self.draw()

        self.root.after(self.speed, self.move_down)

    # УПРАВЛЕНИЕ
    def move_left(self, event):

        if self.game_running:

            if not self.collision(
                self.current_x - 1,
                self.current_y
            ):

                self.current_x -= 1

            self.draw()

    def move_right(self, event):

        if self.game_running:

            if not self.collision(
                self.current_x + 1,
                self.current_y
            ):

                self.current_x += 1

            self.draw()

    def move_fast(self, event):

        if self.game_running:

            if not self.collision(
                self.current_x,
                self.current_y + 1
            ):

                self.current_y += 1

            self.draw()

    # ПОВОРОТ
    def rotate(self, event):

        if not self.game_running:
            return

        rotated = list(zip(*self.current_shape[::-1]))

        rotated = [list(row) for row in rotated]

        old_shape = self.current_shape

        self.current_shape = rotated

        if self.collision(
            self.current_x,
            self.current_y
        ):

            self.current_shape = old_shape

        self.draw()

    # GAME OVER

    def game_over(self):

        self.game_running = False

        messagebox.showinfo(
            "Игра окончена",
            f"Ты проиграл!\n\n"
            f"Очки: {self.score}\n"
            f"Уровень: {self.level}"
        )

    # СТАРТ ИГРЫ
    def start_game(self):

        self.menu_frame.place_forget()

        self.game_frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER
        )

        self.board = []

        for y in range(self.HEIGHT):

            row = []

            for x in range(self.WIDTH):
                row.append(0)

            self.board.append(row)

        self.score = 0
        self.lines_cleared = 0

        self.level = 1
        self.speed = 500

        self.score_label.config(text="Очки: 0")

        self.level_label.config(text="Уровень: 1")

        self.game_running = True

        self.new_shape()
        self.draw()
        self.move_down()

    # ВЫХОД
    def exit_game(self):

        self.root.destroy()

# ЗАПУСК
root = Tk()

app = TetrisGame(root)

root.mainloop()