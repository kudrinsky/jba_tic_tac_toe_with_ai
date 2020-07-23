import random
import copy

field_state = [' '] * 9
coordinates = ['1 3', '2 3', '3 3', '1 2', '2 2', '3 2', '1 1', '2 1', '3 1']
avail_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def render(state):
    result = '-' * 9 + '\n'
    while len(state) > 0:
        result += '| ' + ' '.join(state[:3]) + ' |\n'
        state = state[3:]
    result += '-' * 9
    print(result)


def dict_for_analyze(state):
    states = {
        '012': '',
        '345': '',
        '678': '',
        '036': '',
        '147': '',
        '258': '',
        '048': '',
        '246': ''
    }
    for key in states:
        val = ''
        for i in range(3):
            val += state[int(key[i])]
        states[key] = val
    return states


def analyze_win(state):
    states = dict_for_analyze(state)
    if 'XXX' in states.values():
        return 'X wins\n'
    if 'OOO' in states.values():
        return 'O wins\n'
    if state.count(' ') == 0:
        return 'Draw\n'
    return None


def analyze_move(state, sign):
    states = dict_for_analyze(state)
    win = {}
    block = {}
    for key in states:
        if states[key].count(' ') == 1 and states[key].count('X') == 2:
            if sign == 'X':
                win[key] = states[key]
            else:
                block[key] = states[key]
        if states[key].count(' ') == 1 and states[key].count('O') == 2:
            if sign == 'O':
                win[key] = states[key]
            else:
                block[key] = states[key]
    if len(win) > 0:
        keys = list(win)
        return int(keys[0][win[keys[0]].index(' ')])
    if len(block) > 0:
        keys = list(block)
        return int(keys[0][block[keys[0]].index(' ')])
    return None


def user_move(sign):
    global field_state, avail_moves
    numbers = '0123456789'
    while True:
        xy = input('Enter the coordinates: ').split()
        if xy[0] not in numbers or xy[1] not in numbers:
            print('You should enter numbers!')
        elif not 1 <= int(xy[0]) <= 3 or not 1 <= int(xy[1]) <= 3:
            print('Coordinates should be from 1 to 3!')
        elif field_state[coordinates.index(' '.join(xy))] != ' ':
            print('This cell is occupied! Choose another one!')
        else:
            break
    field_state[coordinates.index(' '.join(xy))] = sign
    avail_moves.remove(coordinates.index(' '.join(xy)))
    render(field_state)


def random_move(sign):
    xy = random.choice(avail_moves)
    field_state[xy] = sign
    avail_moves.remove(xy)
    render(field_state)


def ai_move_easy(sign):
    global field_state, avail_moves
    print('Making move level "easy"')
    random_move(sign)


def ai_move_medium(sign):
    global field_state, avail_moves
    print('Making move level "medium"')
    smart_move = analyze_move(field_state, sign)
    if smart_move is not None:
        field_state[smart_move] = sign
        avail_moves.remove(smart_move)
        render(field_state)
    else:
        random_move(sign)


def minimax_alg(state, sign):
    current_state = copy.deepcopy(state)
    if analyze_win(current_state) is None:
        pass
    elif analyze_win(current_state) == 'Draw\n':
        return [-1, 0]
    elif analyze_win(current_state).startswith(sign):
        return [-1, 10]
    elif analyze_win(current_state).endswith('wins\n'):
        return [-1, -10]
    avail_cell = [i for i in range(9) if current_state[i] == ' ']
    moves = []
    for i in range(len(avail_cell)):
        cell_index = avail_cell[i]
        current_state[avail_cell[i]] = sign
        if sign == 'X':
            result = minimax_alg(current_state, 'O')
            score = result[1]
        else:
            result = minimax_alg(current_state, 'X')
            score = result[1]
        current_state[avail_cell[i]] = ' '
        moves.append([cell_index, score])
    best_move = None
    if sign == 'X':
        best_score = -10000
        for i in range(len(moves)):
            if moves[i][1] > best_score:
                best_score = moves[i][1]
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if moves[i][1] < best_score:
                best_score = moves[i][1]
                best_move = i
    return moves[best_move]


def ai_move_hard(sign):
    global field_state, avail_moves
    print('Making move level "hard"')
    if field_state == [' '] * 9:
        random_move(sign)
    else:
        res = minimax_alg(field_state, sign)
        if res[0] == -1:
            pass
        else:
            field_state[res[0]] = sign
            avail_moves.remove(res[0])
            render(field_state)


def move(player, sign):
    if player == 'user':
        user_move(sign)
    elif player == 'easy':
        ai_move_easy(sign)
    elif player == 'medium':
        ai_move_medium(sign)
    elif player == 'hard':
        ai_move_hard(sign)


def game_loop(player_1, player_2):
    global avail_moves
    render(field_state)
    avail_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while True:
        move(player_1, 'X')
        if analyze_win(field_state) is None:
            move(player_2, 'O')
            if analyze_win(field_state) is None:
                continue
        print(analyze_win(field_state))
        break
    main_menu()


def main_menu():
    command = input('Input command: ').split()
    commands = ['user', 'easy', 'medium', 'hard']
    if command[0] == 'exit':
        pass
    elif len(command) != 3 or command[0] != 'start' or command[1] \
            not in commands or command[2] not in commands:
        print('Bad parameters')
        main_menu()
    else:
        game_loop(command[1], command[2])


main_menu()
