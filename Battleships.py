from random import randint
from classesForBattleship import *

def draw_pgs(board_one, board_two):
    header = "|x\y|"
    def hider_row(row):
        row = row.replace("S", "*")
        row = row.replace("O", "*")
        return row

    for i in range(1, board_one.size_y+1):
        header += f" {i} |"
    x_line = "-" * len(header)
    print(f"{x_line}BATTLE_SHIP{x_line}")
    print(f"{header}=Y===#===Y={header[4::]}{header[3::-1]}")
    print("-"*(len(header)*2+11))
    print_list_one = list()
    print_list_two = list()
    for i, board_line in enumerate(board_one.playground):
        row_str = f"| {i+1} | {' | '.join(board_line)} |"
        if board_one.hidden == True:
            row_str = hider_row(row_str)
        print_list_one.append(row_str)
    for i, board_line in enumerate(board_two.playground):
        row_str = f"| {' | '.join(board_line)} | {i+1} |"
        if board_two.hidden == True:
            row_str = hider_row(row_str)
        print_list_two.append(row_str)
    for i in range(0, board_one.size_x):
        print(f"{print_list_one[i]}|---|{i+1}|---|{print_list_two[i]}")
        print("-"*(len(header)*2+11))

def add_ships_input(board_player_one, draw_boards):
    def add_input_ship(qwestion):
        valid = False
        d = 1
        while not valid:
            answer = input(qwestion)
            if 1 < len(answer) < 4 and answer.isdigit() == True:
                valid = True
            else:
                print("""Прошу вас ввести корректные данные, в формате [XYD], где:
                X - координата по X(сверху вниз), 
                Y - координата по Y(слева направо),  
                D - направление от опорной точки(0 - вниз, 1 - вправо).""")
        if valid == True:
            x = int(answer[0]) - 1
            y = int(answer[1]) - 1
            if len(answer) == 3:
                d = int(answer[2])
        return x, y, d
    for i in range(len(board_player_one.base_list_lenght_ship)):
        result = Game_Error.none
        while result != Game_Error.succes:
            ship_data = add_input_ship(f"Расположите корабль №{i+1}(длинна:{board_player_one.base_list_lenght_ship[i]}) [xyd]: ")
            ship = Ship(board_player_one.base_list_lenght_ship[i], ship_data[0], ship_data[1], ship_data[2] )
            result = board_player_one.add_ship_on_board(ship)
            if result == Game_Error.over_board:
                print("Неподходящее место! Корабль за пределами поля!")
            if result == Game_Error.collision:
                print("Неподходящее место! Клетка уже занята!")
            if result == Game_Error.collision_save_area:
                print("Неподходящее место! Расстояние между кораблями не должно быть меньше чем 1 клетка")
            if result == Game_Error.succes:
                draw_boards()

def add_ships_random(board):
    result = False
    def get_start_pos(lenght, direction):
        for_list = []
        for x in range(0, board.size_x):
            for y in range(0, board.size_y):
                result = board.check_can_place(x, y, lenght, direction)
                if result == Game_Error.succes:
                    for_list.append(Dot(x, y))
        return for_list
    while not result:
        copy_base_list_ship = list(board.base_list_lenght_ship.copy())
        try:
            while len(copy_base_list_ship) > 0:
                l = copy_base_list_ship.pop(randint(0, len(copy_base_list_ship) - 1))
                d = randint(0, 1)
                dots = get_start_pos(l, d)
                dot = dots.pop(randint(0, len(dots) - 1))
                ship = Ship(l, dot.x, dot.y, d)
                board.add_ship_on_board(ship)
        except ValueError:
            board.clear_playground()
        else:
            result = True

def random_shot(board):
    copy_list = board.list_of_posible_shots.copy()
    dot_for_shot = copy_list.pop(randint(0,len(board.list_of_posible_shots)-1))
    return dot_for_shot

def shot_players(board_shot, board_fired_upon, draw):
    miss = False
    score_counter = 1

    def shot(answer, score_counter, board, miss):
        print(f"Выстрел по координатам: X:{answer.x+1} Y:{answer.y+1}")
        cord_x, cord_y = answer.x, answer.y
        if Dot(answer.x, answer.y) not in board.list_of_posible_shots:
            print("Переход хода! Вы уже стреляли в эти координаты!")
            miss = True
            return score_counter, miss
        if board.playground[answer.x][answer.y] == "O":
            board.playground[answer.x][answer.y] = "T"
            print(f"Эх, промах! счёт за ход: +{score_counter}")
            draw()
            board.list_of_posible_shots.remove(Dot(answer.x, answer.y))
            miss = True
        if board.playground[answer.x][answer.y] == "S":
            board.playground[answer.x][answer.y] = "X"
            score_counter *= 2
            print("Есть пробитие!")
            board.list_of_posible_shots.remove(Dot(answer.x, answer.y))
            draw()
            print(f"Счет: {score_counter}")
        return score_counter, miss

    while not miss:
        game_end = not board_fired_upon.check_active_ships()
        if game_end == True:
            return score_counter, game_end
        if board_shot.player == True:
            player_answer = input("Куда будем стрелять? ")
            try:
                player_answer = Dot(int(player_answer[0])-1, int(player_answer[1])-1)
            except:
                print("Я вас не понимаю, введите координаты [XY]:")
                continue
            else:
                score_counter, miss = shot(player_answer, score_counter, board_fired_upon, miss)
        else:
            bot_answer = random_shot(board_fired_upon)
            score_counter, miss = shot(bot_answer, score_counter, board_fired_upon, miss)
    return score_counter, game_end

def play_battleship(board_one, board_two, draw):
    game_end = False
    score_player_one = 0
    score_player_two = 0
    step_counter = 0
    while not game_end:
        if step_counter % 2 == 0:
            print("Ходит игрок:")
            score, game_end = shot_players(board_one, board_two, draw)
            score_player_one += score
        else:
            print("Ходит компьютер:")
            score, game_end = shot_players(board_two, board_one, draw)
            score_player_two += score
        step_counter += 1
    if game_end == True:
        print(f"Game Over!\nWin:{f'Player! Набрано очков:{score_player_one} ' if score_player_one > score_player_two else f'Comp! Набрано очков: {score_player_two}'}")

def next_play():
    next_play = input("Сыграем еще? [Y/y/1]/[N/n/0]? ")
    if next_play == "Y" or next_play == "y" or next_play == "1":
        return True
    else:
        print("Удачи на дорогах, *ПУФ*")
        return False

def get_intro(draw_boards, board_one, board_two):
    reg_yn = input("Будем сами расставлять кораблики? Y=1/N=0... ")
    if reg_yn == "Y" or reg_yn == "y" or reg_yn == "1":
        draw_boards()
        add_ships_input(board_one, draw_boards)
    elif reg_yn == "N" or reg_yn == "n" or reg_yn == "0":
        add_ships_random(board_one)
    else:
        print("Буду считать это неудачной попыткой!")
    if reg_yn in "Yy1Nn0":
        add_ships_random(board_two)
        print("Корабли на позициях! Да начнется битва!")
        draw_boards()
        play_battleship(board_one, board_two, draw_boards)

def game():
    pg_size_x = 6
    pg_size_y = 6
    board_player_one = Board(pg_size_x, pg_size_y, True)
    board_player_two = Board(pg_size_x, pg_size_y, False, True)
    draw_boards = lambda: draw_pgs(board_player_one, board_player_two)
    print("""---------------------------------------------------------------------    
|   Добро пожаловать на битву кораблей!                             |
---------------------------------------------------------------------
|   Бой идет против компьютера!                                     |
---------------------------------------------------------------------
|   Для игрока предусмотрены 2 режима расстановки   | Условные      |
|   кораблей, ручной или автоматический.            | обозначения:  |
|   Ввод координат для расстановки кораблей         | S - Корабль   |
|   производится в формате [XYD], где:              | X - Подбит(S) |
|     \ X - координата по X(сверху вниз),           | O - Пустота   |
|     \ Y - координата по Y(слева направо),         | T - Промах    |
|     \ D - направление от опорной точки:           | * - Туман     |
|           \ 0 - вниз,                             |               |
|           \ 1 - вправо(по умолчанию - 1)          |               |
|           \ Возможны ответы формата: [XY]         |               |
---------------------------------------------------------------------                
|   Формат для ввода координат ведения огня: [XY]                   |
---------------------------------------------------------------------
|   Поле следующего вида:                                           |""")
    draw_pgs(board_player_one, board_player_one)
    get_intro(draw_boards, board_player_one, board_player_two)
    while True:
        if not next_play():
            break
        get_intro(draw_boards, board_player_one,board_player_two)

game()

