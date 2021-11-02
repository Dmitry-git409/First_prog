field = list(range(1, 10))


def create_field(field):
    print('-------------')
    for i in range(3):
        print('|', field[i*3+0], '|', field[i*3+1], '|', field[i*3+2], '|')
        print('-------------')


def rewritten_field(field, sign):
    c_ount = True
    while c_ount:
        answer_user = input('input your answer...' + sign)
        try:
            answer_user = int(answer_user)
        except:
            print('please input digit...')
            continue
        if 1 <= answer_user <= 9:
            if str(field[answer_user-1]) not in 'XO':
                field[answer_user-1] = sign
                c_ount = False
            else:
                print('this\'s place use')
        else:
            print('digit only 1 to 9')
            continue


def main_programm(field):
    win = False
    count = 0
    while not win:
        create_field(field)
        if count % 2 == 0:
            sign = 'X'
            rewritten_field(field, sign)
        else:
            sign = 'O'
            rewritten_field(field, sign)
        count += 1
        if count > 4:
            if check_win(field):
                print('Winner ' + sign + '!')
                win = True
                create_field(field)
                continue
            if count == 9:
                print('Not winners!')
                break


def check_win(field):
    win_comb = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for i in win_comb:
        if field[i[0]] == field[i[1]] == field[i[2]]:
            return True
    return False


main_programm(field)
