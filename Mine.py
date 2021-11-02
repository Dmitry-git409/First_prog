import random
A = int(input('input format field'))
M = int(input('input mine count'))


def create_field_mine(mine_pole):
    '''функция отрисовки игрового поля'''
    for i in range(A):
        for j in range(A):
            print(f'{mine_pole[i*A+j]:>5}', end='')
        print('\n')


def player_tap(mine_pole, game_pole):
    '''ход игрока и сравнения с полем мин'''
    coun_T = True
    while coun_T:
        player_step_x = input('input column position')
        player_step_y = input('input string position')
        try:
            player_step_x = int(player_step_x)
            player_step_y = int(player_step_y)
        except:
            print('only digit!')
            continue
        if 1 <= player_step_x <= A and 1 <= player_step_y <= A:
            i = player_step_x - 1
            j = player_step_y - 1
            if mine_pole[i*A+j] != -1:
                game_pole[i*A+j] = mine_pole[i*A+j]
                return True
            else:
                return False
        else:
            print('1 to %d' % A)
            continue


def create_field(game_pole):
    '''функция отрисовки игрового поля'''
    for i in range(A):
        a = 1
        for j in range(A):
            if game_pole[i*A+j] == '*':
                print(f'{game_pole[i*A+j]:>5}' + '%d' % a, end='')
                a += 1
            else:
                print('%c' % ' ' + f'{game_pole[i*A+j]:>5}', end='')
                a += 1
        print('\n')


def aggregate(mine_pole):
    for i in range(A):
        for j in range(A):
            if mine_pole[i*A+j] != -1:
                n = 0
                for x in range(i-1, i+2):
                    if x < 0 or x > A-1:
                        continue
                    for y in range(j-1, j+2):
                        if y < 0 or y > A-1:
                            continue
                        if mine_pole[x*A+y] == -1:
                            n += 1
                mine_pole[i*A+j] = n


def main_game(M):
    '''основной механизм и создание минного поля'''
    mine_pole = [0] * A * A
    game_pole = ['*'] * A * A
    n = M
    win = True
    while n > 0:
        i = random.randrange(A)
        j = random.randrange(A)
        if mine_pole[i*A+j] == -1:
            continue
        mine_pole[i*A+j] = -1
        n -= 1
    aggregate(mine_pole)
    create_field(game_pole)
    while win:
        if player_tap(mine_pole, game_pole):
            j = 0
            for i in game_pole:
                if i == '*':
                    continue
                else:
                    j += 1
            if j == A * A - M:
                print('You WIN!!!')
                break
            # create_field_mine(mine_pole)
            create_field(game_pole)
            continue
        else:
            print('You are failed!!!')
            create_field_mine(mine_pole)
            win = False


main_game(M)
