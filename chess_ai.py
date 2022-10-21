from board import Board
from constants import *
from time import perf_counter

pygame.quit()


class ModifiedBoard(Board):
    def __init__(self):
        self.start_move = (None, None)
        self.destination_move = (None, None)
        self.delay = -1
        self.white_turn = True
        self.last_move = [(None, None), (None, None)]
        self.move_made = []
        self.move_made_in_uci = []
        self.en_passant = (None, None)
        self.en_passant_history = []
        # uppercase : black side
        # lowercase : white side
        self.board = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.board_history = []

    def move(self, start_move, destination_move):
        start_row, start_col = start_move
        end_row, end_col, promote = destination_move
        # check if the move is castle or not,if it is,move the rook and king to a specific square
        if promote == 'k':
            if (end_row, end_col) == (7, 2):
                self.board[7][0], self.board[7][3] = '', self.board[7][0]
            elif (end_row, end_col) == (7, 6):
                self.board[7][7], self.board[7][5] = '', self.board[7][7]
        elif promote == 'K':
            if (end_row, end_col) == (0, 2):
                self.board[0][0], self.board[0][3] = '', self.board[0][0]
            elif (end_row, end_col) == (0, 6):
                self.board[0][7], self.board[0][5] = '', self.board[0][7]
        # check for en passant
        if self.board[start_row][start_col].lower() == 'p' and self.en_passant != (None, None):
            r, c = self.en_passant
            if self.white_turn and end_row == r - 1 and end_col == c:
                self.board[r][c] = ''
            elif (not self.white_turn) and end_row == r + 1 and end_col == c:
                self.board[r][c] = ''
        if self.board[start_row][start_col].lower() == 'p' and abs(end_row - start_row) == 2:
            self.en_passant = (end_row, end_col)
            self.en_passant_history.append(self.en_passant)
        else:
            self.en_passant = (None, None)
            self.en_passant_history.append(self.en_passant)

        self.board[start_row][start_col], self.board[end_row][end_col] = '', self.board[start_row][
            start_col]
        self.last_move = [start_move, destination_move]
        self.move_made.append(self.last_move)
        self.move_made_in_uci.append(SQUARES[start_move] + SQUARES[(destination_move[0], destination_move[1])])
        if self.board[end_row][end_col].lower() == 'p' and (end_row == 7 or end_row == 0):
            self.board[end_row][end_col] = promote
            self.move_made_in_uci[-1] += self.board[end_row][end_col]
        self.copy_board()
        self.white_turn = not self.white_turn

        self.start_move = (None, None)
        self.destination_move = (None, None)
        self.delay = 0

    def get_legal_moves(self, row, col, white_turn):
        legal_moves = []
        if row is None or col is None:
            return []
        if self.board[row][col] == 'p' and white_turn:
            legal_moves = self.get_legal_moves_white_pawn(row, col)
        elif self.board[row][col] == 'P' and not white_turn:
            legal_moves = self.get_legal_moves_black_pawn(row, col)
        # legal moves of white rook and black rook
        elif (self.board[row][col] == 'r' and white_turn) or (self.board[row][col] == 'R' and not white_turn):
            legal_moves = self.get_legal_moves_rook(row, col)
        # legal moves of white bishop and black bishop
        elif (self.board[row][col] == 'b' and white_turn) or (self.board[row][col] == 'B' and not white_turn):
            legal_moves = self.get_legal_moves_bishop(row, col)
        # legal moves of black and white knight
        elif (self.board[row][col] == 'n' and white_turn) or (self.board[row][col] == 'N' and not white_turn):
            legal_moves = self.get_legal_moves_knight(row, col)
        # legal moves of white and black king
        elif (self.board[row][col] == 'k' and white_turn) or (self.board[row][col] == 'K' and not white_turn):
            legal_moves = self.get_legal_moves_king(row, col)
        # legal moves of white queen and black queen
        elif (self.board[row][col] == 'q' and white_turn) or (self.board[row][col] == 'Q' and not white_turn):
            legal_moves = self.get_legal_moves_queen(row, col)

        final_legal_moves = []
        for move in legal_moves:
            r, c = row, col
            r1, c1 = move
            temp_1, temp_2 = self.board[r][c], self.board[r1][c1]
            self.board[r][c], self.board[r1][c1] = '', self.board[r][c]
            white_turn = not white_turn
            if white_turn:
                if self.get_king_position('BLACK') not in self.get_white_attack_square():
                    final_legal_moves.append(move)
            else:
                if self.get_king_position('WHITE') not in self.get_black_attack_square():
                    final_legal_moves.append(move)
            self.board[r][c], self.board[r1][c1] = temp_1, temp_2
            white_turn = not white_turn
        # check if it can be a castling move or not
        f_legal_moves = []
        if self.board[row][col] == 'k':
            check_long_castle, check_short_castle = self.check_castling_right()
            if check_long_castle:
                f_legal_moves.append((7, 2, 'k'))
            if check_short_castle:
                f_legal_moves.append((7, 6, 'k'))
        elif self.board[row][col] == 'K':
            check_long_castle, check_short_castle = self.check_castling_right()
            if check_long_castle:
                f_legal_moves.append((0, 2, 'K'))
            if check_short_castle:
                f_legal_moves.append((0, 6, 'K'))
        for i in range(len(final_legal_moves)):
            if final_legal_moves[i][0] == 0 and self.board[row][col] == 'p':
                r2, c2 = final_legal_moves[i]
                f_legal_moves.append((r2, c2, 'q'))
                f_legal_moves.append((r2, c2, 'r'))
                f_legal_moves.append((r2, c2, 'n'))
                f_legal_moves.append((r2, c2, 'b'))
            elif final_legal_moves[i][0] == 7 and self.board[row][col] == 'P':
                r2, c2 = final_legal_moves[i]
                f_legal_moves.append((r2, c2, 'Q'))
                f_legal_moves.append((r2, c2, 'R'))
                f_legal_moves.append((r2, c2, 'N'))
                f_legal_moves.append((r2, c2, 'B'))
            else:
                r2, c2 = final_legal_moves[i]
                f_legal_moves.append((r2, c2, ''))
        return f_legal_moves


def evaluate(board):
    total_points_white = 0
    total_points_black = 0
    point_dict = {
        'q': 9,
        'r': 5,
        'n': 3,
        'b': 3,
        'p': 1,
        'k': 999
    }
    for i in range(8):
        for j in range(8):
            if board[i][j] != '':
                if board[i][j].islower():
                    total_points_white += point_dict[board[i][j].lower()]
                else:
                    total_points_black += point_dict[board[i][j].lower()]
    return total_points_white - total_points_black


board = ModifiedBoard()
time_get_legal = 0


def minimax(depth, is_white_turn):
    if board.is_checkmate():
        if is_white_turn:
            return -9999999
        else:
            return 9999999
    if depth == 0:
        return evaluate(board.board)
    else:
        global time_get_legal
        t0 = perf_counter()
        legal_moves = board.get_all_legal_moves(is_white_turn)
        time_get_legal = time_get_legal + (perf_counter() - t0)
        # print(legal_moves)
        global time_move, time_undo
        if is_white_turn:
            ans = -9999999
            for move in legal_moves:
                start, end = move
                board.move(start, end)
                ans = max(ans, minimax(depth - 1, not is_white_turn))
                board.undo_move()

        else:
            ans = 9999999
            for move in legal_moves:
                start, end = move
                board.move(start, end)
                ans = min(ans, minimax(depth - 1, not is_white_turn))
                board.undo_move()
        return ans


print(minimax(4, True))
print(time_get_legal)
