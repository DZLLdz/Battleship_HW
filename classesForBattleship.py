import enum

class Game_Error(enum.Enum):
    none = 0
    succes = 1
    collision = 2
    collision_save_area = 3
    over_board = 4

class Board:
    def __init__(self, size_x, size_y, player_bool, hidden=False):
        self.player = player_bool
        self.size_x = size_x
        self.size_y = size_y
        self.playground = [["O"] * size_y for i in range(size_x)]
        self.hidden = hidden
        self.base_list_lenght_ship = [3,2,2,1,1,1,1]
        self.list_of_ships = list()
        self.create_posible_shots()

    def __str__(self):
        return f'Ship: {self.list_of_ships}'

    def get_list_ships(self):
        return self.list_of_ships

    def clear_playground(self):
        self.playground = [["O"] * self.size_y for i in range(self.size_x)]
        self.list_of_ships.clear()

    def check_save_area(self, dot):
        for ship in self.list_of_ships:
            if dot in ship.safepoints:
                return False
        return True
    def check_can_place(self, x, y , lenght, dir):
        for i in range(lenght):
            if x < 0 or x > self.size_x-1 or y < 0 or y > self.size_y-1 :
                return Game_Error.over_board
            if not self.check_save_area(Dot(x, y)):
                return Game_Error.collision_save_area
            if self.playground[x][y] != "O":
                return Game_Error.collision
            if lenght > 1:
                if dir == 0:
                    x += 1
                if dir == 1:
                    y += 1
        return Game_Error.succes

    def create_posible_shots(self):
        self.list_of_posible_shots = []
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                self.list_of_posible_shots.append(Dot(x, y))

    def add_ship_on_board(self, ship):
        add_result = self.check_can_place(ship.ship_x, ship.ship_y, ship.lenght, ship.direction)
        if add_result != Game_Error.succes:
            return add_result
        for point in ship.points:
            self.playground[point.x][point.y] = "S"
        self.list_of_ships.append(ship)
        return add_result

    def check_active_ships(self):
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                if self.playground[x][y] == "S":
                    return True
        return False

class Ship:
    def __init__(self, lenght, ship_x, ship_y, dir):
        self.lenght = lenght
        self.ship_x = ship_x
        self.ship_y = ship_y
        self.direction = dir
        self.points = []
        self.create_points()
        self.create_safe_area()

    def __str__(self):
        ship_info = f"Ship:L={self.lenght}, X:Y={self.ship_x+1}:{self.ship_y+1}, D={self.direction}, P={len(self.points)}"
        return ship_info

    def create_points(self):
        cur_x = self.ship_x
        cur_y = self.ship_y
        for i in range(self.lenght):
            self.points.append(Dot(cur_x, cur_y))
            if self.lenght > 1:
                if self.direction == 0:
                    cur_x += 1
                if self.direction == 1:
                    cur_y += 1
    def create_safe_area(self):
        self.safepoints = set()
        for point in self.points:
            for i in range(point.x-1, point.x+2):
                for j in range(point.y-1, point.y+2):
                    self.safepoints.add(Dot(i, j))
        for point in self.points:
            if point in self.safepoints:
                self.safepoints.remove(Dot(point.x, point.y))

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return f"{self.x, self.y}"
    def __hash__(self):
        return hash(self.x + 7*self.y)