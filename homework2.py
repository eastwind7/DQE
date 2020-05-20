import re

cell_num = list(range(1, 10))


def draw_board(board):
    print("-------------")
    for i in range(3):
        print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
        print("-------------")


def process_input(player_token, board):
    valid = False
    while not valid:
        player_answer = input("Chose cell: " + player_token + "? ")
        if re.match(r"[1-9]", player_answer):
            player_answer = int(player_answer)
            if str(board[player_answer - 1]) not in "XO":
                board[player_answer - 1] = player_token
                valid = True
            else:
                print("Please, chose free cell")
        else:
            print("There is no such number on the board. Try again.")


def check_win(board):
    win_comb = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_comb:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False


counter = 0
win = False
while not win:
    draw_board(cell_num)
    if counter % 2 == 0:
        process_input("X", cell_num)
    else:
        process_input("O", cell_num)
    counter += 1
    if counter > 4:
        tmp = check_win(cell_num)
        if tmp:
            print(tmp, "Wins!")
            win = True
    if counter == 9:
        print("Draw!")
        break
draw_board(cell_num)