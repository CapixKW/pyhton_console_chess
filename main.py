from math import gcd
from pieces import *

# '\033[1m' / '\x1B[3m'

boards = ['Standard']

piece_string_to_class = {
    '_': Empty,
    "Pawn": Pawn,
    "Rook": Rook,
    "Knight": Knight,
    "Bishop": Bishop,
    "Queen": Queen,
    "King": King
}

row_index = lambda r: 56 - ord(r)
column_index = lambda c: ord(c) - 97


def start_game():
    board = load_board()
    game_loop(board)


def load_board():
    _ = True
    while _:
        print("Choose your board:")
        for i in range(len(boards)):
            print(f"{i + 1} - {boards[i]}")
        choice = input()

        try:
            choice = int(choice) - 1
            _ = False
        except ValueError:
            print("Choice must be an integer from the list!")
            continue
        if choice not in range(len(boards)):
            print("Choice must be an integer from the list!")
            _ = True

    with open("boards/" + boards[choice].lower() + ".txt") as f:
        start_lines = [line.split() for line in f.read().split('\n')]
    start_lines.reverse()
    r = len(start_lines)

    board = [[None] * 8 for _ in range(8)]

    for i in range(r):
        for j in range(8):
            board[i][j] = piece_string_to_class[start_lines[i][j]]("black")
            board[7 - i][j] = piece_string_to_class[start_lines[i][j]]("white")

    for i in range(r, 8 - r):
        for j in range(8):
            board[i][j] = Empty()

    return board


def board_print(board):
    print(" \ta\tb\tc\td\te\tf\tg\th")
    for i in range(8):
        line = str(8 - i)
        for j in range(8):
            piece = board[i][j]
            if piece.selectable:
                line += '\t' + '\x1B[3m' + str(board[i][j]) + '\x1B[0m'
            else:
                line += '\t' + str(board[i][j])
        print(line)


def available_moves(row, colum, board, check_for_checks=True):
    piece = board[row][colum]
    moves = []
    for move in piece.moves():
        if move.first_only and piece.has_moved:
            continue

        r = 0
        move_blocked = False
        while not move_blocked and r < move.range:
            if not move.jump:
                step_numbers = gcd(move.x, move.y)
            else:
                step_numbers = 1

            y_step = move.y // step_numbers
            x_step = move.x // step_numbers
            for step in range(1, step_numbers):
                if board[row - y_step * step - r * move.y][colum + x_step * step + r * move.x].blocks_movement:
                    move_blocked = True
                    break
            else:
                r += 1
                target_row = row - r * move.y
                target_column = colum + r * move.x
                if target_row not in range(8) or target_column not in range(8):
                    break
                target_piece = board[target_row][target_column]
                if target_piece.color == piece.color or \
                        (move.attack_only and type(target_piece) == Empty) \
                        or (move.move_only and type(target_piece) != Empty):
                    break

                board[target_row][target_column] = piece
                board[row][colum] = Empty()
                if not check_for_checks or not is_checked(piece.color, board):
                    moves.append((target_row, target_column))
                board[row][colum] = piece
                board[target_row][target_column] = target_piece

                if target_piece.blocks_movement:
                    break

    return moves


def is_checked(color, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if type(piece) != Empty and piece.color != color:
                for move in available_moves(row, column, board, check_for_checks=False):
                    if board[move[0]][move[1]].can_be_checked:
                        return True
    return False


def is_check_mated(color, board):
    for row in range(8):
        for column in range(8):
            if board[row][column].color == color and available_moves(row, column, board):
                return False
    return True


def game_loop(board):
    turn_color = "white"
    turn_count = 0

    while True:
        if is_check_mated(turn_color, board):
            print(f"Game over - {turn_color.title()} lost!")
            break
        valid_choice = False
        board_print(board)
        while not valid_choice:
            print(f"{turn_color.title()} chooses their piece: ")
            chosen_tile = input()
            if len(chosen_tile) != 2 or column_index(chosen_tile[0]) not in range(8) or row_index(
                    chosen_tile[1]) not in range(8):
                print("Choice must be a tile on the board, eg. a1!")
            else:
                row = row_index(chosen_tile[1])
                column = column_index(chosen_tile[0])
                chosen_piece = board[row][column]
                moves = available_moves(row, column, board)

                if chosen_piece.color != turn_color:
                    print(f"Chosen tile must have a {turn_color} piece on it!")
                elif not moves:
                    print("No available moves for that piece!")
                else:
                    valid_choice = True
                    for move in moves:
                        board[move[0]][move[1]].selectable = True

        valid_move = False
        board_print(board)
        while not valid_move:
            print("Choose your move (press enter to choose another piece):")
            chosen_move = input()
            if not chosen_move:
                valid_move = True
                for move in moves:
                    board[move[0]][move[1]].selectable = False
            elif len(chosen_move) != 2 or column_index(chosen_move[0]) not in range(8) or row_index(
                    chosen_move[1]) not in range(8):
                print("Choice must be a tile on the board, eg. a1!")
            else:
                move_row = row_index(chosen_move[1])
                move_column = column_index(chosen_move[0])

                if (move_row, move_column) not in moves:
                    print("You must choose a valid move!")
                else:
                    valid_move = True
                    turn_count += 1
                    turn_color = "black" if turn_color == "white" else "white"
                    for move in moves:
                        board[move[0]][move[1]].selectable = False

                    chosen_piece.has_moved = True
                    board[move_row][move_column] = chosen_piece
                    board[row][column] = Empty()


if __name__ == '__main__':
    start_game()
