import random
import tkinter as tk
import collections

original_width = 20
width = 2 * original_width + 1
window_size = 800
square_length = window_size/width


class Square(tk.Label):
    def __init__(self, color, is_cell):
        super().__init__(button_frame, background=color)
        self.is_cell = is_cell
        self.parent = ""
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = self.g_cost + self.h_cost

    def set_g_cost(self, g_cost):
        self.g_cost = g_cost
        self.f_cost = self.g_cost + self.h_cost

    def set_h_cost(self, h_cost):
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost


class Wall(Square):
    def __init__(self, x, y):
        super().__init__("black", False)
        self.x = x
        self.y = y
        self.open = False

    def open_wall(self):
        self.open = True
        super().config(background="white")


class Cell(Square):
    def __init__(self, x, y):
        super().__init__("white", True)
        self.x = x
        self.y = y
        self.visited = False
        self.is_goal = False

    def set_goal(self):
        super().config(background="red")
        self.is_goal = True


class Player(tk.Label):
    def __init__(self, x, y):
        super().__init__(root, background="lime")
        self.x = x
        self.y = y
        self.dead = False

    def move_to(self, x, y):
        self.place(x=(x * square_length), y=(y * square_length))
        self.x = x
        self.y = y

    def move(self, direction):
        if self.dead:
            return
        if direction == "left" and self.x - 1 >= 0:
            if (self.x - 1) % 2 == 1 and self.y % 2 == 1:
                self.move_to(self.x - 1, self.y)
            elif squares[self.x-1][self.y].open:
                self.move_to(self.x - 1, self.y)
        if direction == "right" and self.x + 1 < width:
            if (self.x + 1) % 2 == 1 and self.y % 2 == 1:
                self.move_to(self.x + 1, self.y)
            elif squares[self.x + 1][self.y].open:
                self.move_to(self.x + 1, self.y)
        if direction == "up" and self.y - 1 >= 0:
            if self.x % 2 == 1 and (self.y - 1) % 2 == 1:
                self.move_to(self.x, self.y - 1)
            elif squares[self.x][self.y - 1].open:
                self.move_to(self.x, self.y - 1)
        if direction == "down" and self.y + 1 >= 0:
            if self.x % 2 == 1 and (self.y + 1) % 2 == 1:
                self.move_to(self.x, self.y + 1)
            elif squares[self.x][self.y + 1].open:
                self.move_to(self.x, self.y + 1)

        if self.game_won():
            self.dead = True

    def game_won(self):
        if self.x % 2 == 1 and self.y % 2 == 1 and squares[self.x][self.y].is_goal:
            return True
        return False


root = tk.Tk()

root.geometry("800x800")
root.title("Labyrinth")

button_frame = tk.Frame(root)
for i in range(width):
    button_frame.columnconfigure(i, weight=1)
    button_frame.rowconfigure(i, weight=1)

squares = [[Cell(x, y) if y % 2 == 1 and x % 2 == 1 else Wall(x, y) for y in range(width)] for x in range(width)]
for j in range(width):
    for i in range(width):
        squares[i][j].grid(row=i, column=j, sticky=tk.W + tk.E + tk.N + tk.S)
button_frame.pack(expand=True, fill="both")


def get_non_visited_neighbours(cell):
    neighbours = []
    if cell.x - 2 > 0 and not squares[cell.x - 2][cell.y].visited:
        neighbours.append(squares[cell.x - 2][cell.y])
    if cell.y - 2 > 0 and not squares[cell.x][cell.y - 2].visited:
        neighbours.append(squares[cell.x][cell.y - 2])
    if cell.x + 2 < width and not squares[cell.x + 2][cell.y].visited:
        neighbours.append(squares[cell.x + 2][cell.y])
    if cell.y + 2 < width and not squares[cell.x][cell.y + 2].visited:
        neighbours.append(squares[cell.x][cell.y + 2])
    return neighbours


def generate_maze():
    stack = collections.deque()

    stack.append(squares[1][1])
    squares[1][1].visited = True
    while not not stack:
        current_cell = stack.pop()
        neighbours = get_non_visited_neighbours(current_cell)
        if len(neighbours) > 0 and not (current_cell.x == width-1 and current_cell.y == width-1):
            stack.append(current_cell)
            random_neighbour_index = random.randint(0, len(neighbours)-1)
            stack.append(neighbours[random_neighbour_index])
            neighbours[random_neighbour_index].visited = True
            if abs(current_cell.x - neighbours[random_neighbour_index].x) > 0:
                if current_cell.x - int((current_cell.x - neighbours[random_neighbour_index].x)/2) == 1 and current_cell.y == 2:
                    print("YES")
                squares[current_cell.x - int((current_cell.x - neighbours[random_neighbour_index].x)/2)][current_cell.y].open_wall()
            elif abs(current_cell.y - neighbours[random_neighbour_index].y) > 0:
                squares[current_cell.x][current_cell.y - int((current_cell.y - neighbours[random_neighbour_index].y)/2)].open_wall()
                if current_cell.x == 1 and current_cell.y - int((current_cell.y - neighbours[random_neighbour_index].y)/2) == 2:
                    print("YES")
                    print(squares[current_cell.x][current_cell.y - int((current_cell.y - neighbours[random_neighbour_index].y) / 2)].open)
            if neighbours[random_neighbour_index].x == width-2 and neighbours[random_neighbour_index].y == width-2:
                stack.pop().set_goal()


generate_maze()

def distance(square1, square2):
    return abs(square1.x - square2.x) + abs(square1.y - square2.y)


for j in range(width):
    for i in range(width):
        squares[i][j].set_h_cost(distance(squares[i][j], squares[width-2][width-2]))


def find_lowest_f_cost(square_list):
    lowest = square_list[0]
    for element in square_list:
        if element.f_cost < lowest.f_cost:
            lowest = element
    return lowest


def find_g_cost(square):
    if square.parent == "":
        return 0
    return 1 + find_g_cost(square.parent)


def traversable(square):
    if square.is_cell:
        return True
    return square.open


def show_path(final_cell):
    final_cell.config(background="red")
    if final_cell.parent == "":
        return
    show_path(final_cell.parent)


def find_closest_path():
    open_list = []
    closed_list = []

    open_list.append(squares[1][1])
    while True:
        current = find_lowest_f_cost(open_list)
        open_list.remove(current)
        closed_list.append(current)
        if current.is_cell and current.is_goal:
            show_path(squares[width-2][width-2])
            break
        neighbours = [squares[current.x-1][current.y], squares[current.x+1][current.y], squares[current.x][current.y-1], squares[current.x][current.y+1]]

        for neighbour in neighbours:
            if not traversable(neighbour) or closed_list.count(neighbour):
                continue
            if not open_list.count(neighbour):
                neighbour.parent = current
                neighbour.set_g_cost(find_g_cost(neighbour))
                if not open_list.count(neighbour):
                    open_list.append(neighbour)

find_closest_path()
'''
for i in range(0, 100000):
    random_id = random.randint(0, 4)
    move = ""
    match random_id:
        case 0:
            move = "left"
        case 1:
            move = "right"
        case 2:
            move = "up"
        case 3:
            move = "down"
    player.move(move)
'''

root.mainloop()
