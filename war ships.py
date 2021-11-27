import random


class ShipWithoutBoard(Exception):
    pass


class CordsWithoutField(Exception):
    def __str__(self):
        return 'Координаты за пределами поля'


class PlaceUsed(Exception):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        return Dot(self.x + other.x, self.y + other.y)


class Ship:  # корабли и их характеристики
    def __init__(self, length, zero_point: Dot, orientation: (0, 1), health):
        self.length = length
        self.zero_point = zero_point
        self.orientation = orientation
        self.health = health
        self.ship_dots = []

    def ship_points(self):  # список координат корабля
        return self.ship_dots


class Board:
    def __init__(self, hide=True):
        self.field = ['*' for _ in range(100)]
        self.hide = hide
        self.digits_grid = list(range(1, 11))
        self.simbols_grid = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.cords_s = (Dot(-1, -1), Dot(-1, 0), Dot(-1, 1),
                        Dot(0, -1), Dot(0, 0), Dot(0, 1),
                        Dot(1, -1), Dot(1, 0), Dot(1, 1))
        self.dict_ships = {}

    def __repr__(self):  # рисуем доску
        if not self.hide:
            print('  ', end='')
            for d in self.digits_grid:
                print('|', f'{d:^3}', end='')
            print('|')
            for i in range(10):
                print(' ', '-'*51)
                print(f'{self.simbols_grid[i]:<2}', end='')
                for j in range(10):
                    print('|', f'{self.field[i*10+j]:^3}', end='')
                print('|')
        else:
            for coord in [i for j in self.dict_ships.values() for i in j]:
                i = coord.x
                j = coord.y
                if self.field[i*10+j] == 'X':
                    continue
                self.field[i*10+j] = '■'
            print('  ', end='')
            for d in self.digits_grid:
                print('|', f'{d:^3}', end='')
            print('|')
            for i in range(10):
                print(' ', '-'*51)
                print(f'{self.simbols_grid[i]:<2}', end='')
                for j in range(10):
                    print('|', f'{self.field[i*10+j]:^3}', end='')
                print('|')
        print(' ', '-'*51)

    def add_ship(self, ship):  # ставим корабль
        ship.ship_dots.append(ship.zero_point)
        x_pos = ship.zero_point.x
        y_pos = ship.zero_point.y
        if ship.orientation == 0:
            for i in range(ship.length-1):
                x_pos += 1
                ship.ship_dots.append(Dot(x_pos, y_pos))
        else:
            for i in range(ship.length-1):
                y_pos += 1
                ship.ship_dots.append(Dot(x_pos, y_pos))
        if Board.check_coords(ship) and self.contour_cross_ships(ship):
            self.dict_ships[ship] = ship.ship_points()
            return True
        else:
            raise ShipWithoutBoard

    def contour_cross_ships(self, ship):
        if not self.dict_ships.values():
            return True
        # 1 нет ли пересечений с кораблями
        for cords in [i for j in self.dict_ships.values() for i in j]:
            if cords in ship.ship_points():
                return False
        # 2 не стоят ли корабли бок о бок
        for cords_s in ship.ship_points():
            for elem in self.cords_s:
                if (cords_s + elem) in [i for j in self.dict_ships.values() for i in j]:
                    return False
        return True

    def draw_contour(self, ship, contour_ship=False):
        if not contour_ship:
            pass
        else:
            for coord in ship.ship_points():
                for disp in self.cords_s:
                    if ((coord + disp) in ship.ship_points()) or Board.inspect_coord(coord + disp):
                        continue
                    else:
                        i = (coord + disp).x
                        j = (coord + disp).y
                        self.field[i*10+j] = '●'

    def shot(self, co):
        if Board.inspect_coord(co):
            raise CordsWithoutField
        if not self.hide:
            if self.field[co.x*10+co.y] != '*':  # для закрытой карты
                raise PlaceUsed
        else:
            if (self.field[co.x*10+co.y] == 'X') or (self.field[co.x*10+co.y] == '●'):  # для открытой карты
                raise PlaceUsed
        for ship in self.dict_ships.items():
            if co in ship[1]:
                ship[0].health -= 1
                self.field[co.x*10+co.y] = 'X'
                if ship[0].health == 0:
                    self.draw_contour(ship[0], contour_ship=True)
                    print('Корабль уничтожен')
                    return True
                else:
                    print('Корабь ранен')
                    return True
        self.field[co.x*10+co.y] = '●'
        print('Мимо')
        return False

    def nuclear_weapon(self, fi):
        for co in self.cords_s:
            try:
                self.shot(co+fi)
            except PlaceUsed:
                pass
            except CordsWithoutField:
                pass

    @staticmethod
    def inspect_coord(c):
        if (c.x >= 10) or (c.y >= 10) or (c.x < 0) or (c.y < 0):
            return True

    @staticmethod
    def check_coords(ship):  # вхождение корабля на доску
        for coord in ship.ship_points():
            if (coord.x in range(10)) and (coord.y in range(10)):
                continue
            else:
                return False
        return True


class Player:
    def __init__(self):
        self.dict_simb = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
                          'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}

    def ask(self):
        pass

    def move(self, player):
        while True:
            try:
                fire = self.ask()
                while player.shot(fire):
                    if g.ai_board.field.count('X') == 20:
                        print('Игрок победил!')
                        return True
                    if g.user_board.field.count('X') == 20:
                        g.ai_board.__repr__()
                        print('Противник победил!')
                        return True
                    print('Поле Игрока')
                    g.user_board.__repr__()
                    print('Поле Противника')
                    g.ai_board.__repr__()
                    fire = self.ask()
                break
            except CordsWithoutField as e:
                print(e)
            except PlaceUsed as e:
                print(e)


class AI(Player):
    def ask(self):
        enemy_fire = Dot(random.randint(0, 9), random.randint(0, 9))
        print('Ход AI =', enemy_fire)
        return enemy_fire


class User(Player):
    def ask(self):
        we = input('Введите координаты выстрела').split(',')
        if we[0] in self.dict_simb.keys():
            for key in self.dict_simb.keys():
                if we[0] == key:
                    we[0] = self.dict_simb[key]
        else:
            raise CordsWithoutField
        user_fire = Dot(we[0], int(we[1])-1)
        return user_fire


class Game:
    def __init__(self, user, user_board, ai, ai_board):
        self.user = user
        self.user_board = user_board
        self.ai = ai
        self.ai_board = ai_board

    def random_board(self, board):
        kit_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for length in kit_ships:
            while True:
                zero_point = Dot(random.randint(0, 9), random.randint(0, 9))
                orientation = random.randint(0, 1)
                s = Ship(length, zero_point, orientation, health=length)
                try:
                    board.add_ship(s)
                    board.draw_contour(s)  # рисуем контур
                    break
                except ShipWithoutBoard:
                    pass

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода(без пробелов): x,y ")
        print(" x - буква строки  ")
        print(" y - номер столбца ")

    def loop(self):
        index_2 = True
        index = 0
        g.random_board(self.user_board)
        g.random_board(self.ai_board)
        while True:
            print('Поле Игрока')
            self.user_board.__repr__()
            print('Поле Противника')
            self.ai_board.__repr__()
            if index % 2 == 0:
                if index_2:
                    a = input('Применить супер заряд?  (только y или n)')
                    if a == 'y':
                        fi = self.user.ask()
                        self.ai_board.nuclear_weapon(fi)
                        index_2 = False
                        print('Поле Игрока')
                        self.user_board.__repr__()
                        print('Поле Противника')
                        self.ai_board.__repr__()
                if self.user.move(self.ai_board):
                    break
                index += 1

            else:
                if self.ai.move(self.user_board):
                    break
                index += 1


    def start(self):
        self.greet()
        self.loop()


g = Game(user=User(), user_board=Board(hide=True), ai=AI(), ai_board=Board(hide=False))
g.start()
