import time
from copy import deepcopy
from utils import *
from engine import Engine
import pygame
import math


class Board:
    def __init__(self, is_playing_bot=False, time_control=10, bonus_time=0):
        self.start_move = (None, None)
        self.destination_move = (None, None)
        self.delay = -1
        self.white_turn = True
        self.last_move = [(None, None), (None, None)]
        self.move_made = []
        self.move_made_in_uci = []
        self.en_passant = (None, None)
        self.en_passant_history = []
        self.is_playing_bot = is_playing_bot
        self.white_time = time_control
        self.black_time = time_control
        self.bonus_time = bonus_time
        self.time_start = time.perf_counter()
        if is_playing_bot:
            self.bot = Engine()
            self.bot.uci()
            self.bot.set_difficulty()
        self.black_bishop_img = pygame.transform.scale(pygame.image.load('resources/resources/black_bishop.png'),
                                                       (WIDTH // 9, HEIGHT // 9))
        self.white_bishop_img = pygame.transform.scale(pygame.image.load('resources/resources/white_bishop.png'),
                                                       (WIDTH // 9, HEIGHT // 9))
        self.black_knight_img = pygame.transform.scale(pygame.image.load('resources/resources/black_knight.png'),
                                                       (WIDTH // 9, HEIGHT // 9))
        self.white_knight_img = pygame.transform.scale(pygame.image.load('resources/resources/white_knight.png'),
                                                       (WIDTH // 9, HEIGHT // 9))
        self.black_rook_img = pygame.transform.scale(pygame.image.load('resources/resources/black_rook.png'),
                                                     (WIDTH // 10, HEIGHT // 10))
        self.white_rook_img = pygame.transform.scale(pygame.image.load('resources/resources/white_rook.png'),
                                                     (WIDTH // 10, HEIGHT // 10))
        self.black_queen_img = pygame.transform.scale(pygame.image.load('resources/resources/black_queen.png'),
                                                      (WIDTH // 9, HEIGHT // 9))
        self.white_queen_img = pygame.transform.scale(pygame.image.load('resources/resources/white_queen.png'),
                                                      (WIDTH // 9, HEIGHT // 9))
        self.black_king_img = pygame.transform.scale(pygame.image.load('resources/resources/black_king.png'),
                                                     (WIDTH // 9, HEIGHT // 9))
        self.white_king_img = pygame.transform.scale(pygame.image.load('resources/resources/white_king.png'),
                                                     (WIDTH // 9, HEIGHT // 9))
        self.black_pawn_img = pygame.transform.scale(pygame.image.load('resources/resources/black_pawn.png'),
                                                     (WIDTH // 12, HEIGHT // 10))
        self.white_pawn_img = pygame.transform.scale(pygame.image.load('resources/resources/white_pawn.png'),
                                                     (WIDTH // 12, HEIGHT // 10))
        self.light_square_img = pygame.transform.scale(pygame.image.load('resources/resources/light_square.png'),
                                                       (WIDTH // 8, HEIGHT // 8))
        self.dark_square_img = pygame.transform.scale(pygame.image.load('resources/resources/dark_square.png'),
                                                      (WIDTH // 8, HEIGHT // 8))
        self.board_coordinate = [
            [pygame.rect.Rect(j * (HEIGHT // 8), i * (WIDTH // 8), WIDTH // 8, HEIGHT // 8) for j in range(8)] for i in
            range(8)]
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
        self.map = {
            'R': self.black_rook_img,
            'r': self.white_rook_img,
            'Q': self.black_queen_img,
            'q': self.white_queen_img,
            'K': self.black_king_img,
            'k': self.white_king_img,
            'P': self.black_pawn_img,
            'p': self.white_pawn_img,
            'N': self.black_knight_img,
            'n': self.white_knight_img,
            'B': self.black_bishop_img,
            'b': self.white_bishop_img
        }

    def draw_board(self, SCREEN=SCREEN):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    SCREEN.blit(self.light_square_img, self.board_coordinate[i][j].topleft)
                    if j == 0:
                        create_text(SCREEN, str(8 - i), self.board_coordinate[i][j].topleft, fontSize=15)
                    if i == 7:
                        x, y = self.board_coordinate[i][j].bottomright
                        create_text(SCREEN, chr(97 + j), (x - 10, y - 15), fontSize=15)
                else:
                    SCREEN.blit(self.dark_square_img, self.board_coordinate[i][j].topleft)
                    if j == 0:
                        create_text(SCREEN, str(8 - i), self.board_coordinate[i][j].topleft, fontSize=15)
                    if i == 7:
                        x, y = self.board_coordinate[i][j].bottomright
                        create_text(SCREEN, chr(97 + j), (x - 10, y - 15), fontSize=15)

    def draw_pieces(self, SCREEN=SCREEN):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '':
                    img = self.map[self.board[i][j]]
                    rect = img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(img, rect)

    def check_diff_side(self, row_1, col_1, row_2, col_2):
        return (self.board[row_1][col_1].islower() and self.board[row_2][col_2].isupper()) or (
                self.board[row_1][col_1].isupper() and self.board[row_2][col_2].islower())

    @staticmethod
    def check_valid(row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def check_mouse_input(self):
        if self.is_playing_bot and not self.white_turn:
            pygame.display.update()
            is_mate, score, best_move = self.bot.find_moves_info_in_uci(self.move_made_in_uci)
            start_move = SQUARES_REVERSED[best_move[:2]]
            destination_move = SQUARES_REVERSED[best_move[2:4]]
            if len(best_move) == 5:
                promote = best_move[4]
                self.move(start_move, destination_move, promote)
            else:
                self.move(start_move, destination_move)
            return
        if pygame.mouse.get_pressed()[0] and self.delay == -1:
            x, y = pygame.mouse.get_pos()
            row, col = y // (HEIGHT // 8), x // (WIDTH // 8)
            if self.start_move == (None, None):
                if self.board[row][col] != '' and ((self.board[row][col].islower() and self.white_turn) or (
                        self.board[row][col].isupper() and not self.white_turn)):
                    self.start_move = (row, col)
            else:
                if (row, col) == self.start_move:
                    return
                elif not self.check_diff_side(self.start_move[0], self.start_move[1], row, col) and self.board[row][
                    col] != '':
                    self.start_move = (row, col)
                else:
                    self.move(self.start_move, (row, col))
        if pygame.key.get_pressed()[K_u] and self.delay == -1:
            self.undo_move()
            if self.is_playing_bot:
                self.undo_move()
        if self.delay >= 0:
            self.delay += 1
            if self.delay == 15:
                self.delay = -1

    # method to make a move from start_move=(row1,col1) to destination_move=(row2,col2),potentally have a promotion
    def move(self, start_move, destination_move, promote=None, is_analyzing=False, SCREEN=SCREEN):
        row, col = destination_move
        if (row, col) in self.get_legal_moves(start_move[0], start_move[1], self.white_turn):
            self.destination_move = (row, col)
            start_row, start_col = start_move
            end_row, end_col = destination_move
            # check if the move is castle or not,if it is,move the rook and king to a specific square
            if self.board[start_row][start_col] == 'k':
                check_long_castle, check_short_castle = self.check_castling_right()
                if check_long_castle and (end_row, end_col) == (7, 2):
                    self.board[7][0], self.board[7][3] = '', self.board[7][0]
                elif check_short_castle and (end_row, end_col) == (7, 6):
                    self.board[7][7], self.board[7][5] = '', self.board[7][7]
            elif self.board[start_row][start_col] == 'K':
                check_long_castle, check_short_castle = self.check_castling_right()
                if check_long_castle and (end_row, end_col) == (0, 2):
                    self.board[0][0], self.board[0][3] = '', self.board[0][0]
                elif check_short_castle and (end_row, end_col) == (0, 6):
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
            # animate move
            self.move_animation(start_move, destination_move, SCREEN)
            # 'move' by replace the start_move position with '' and the destination_move position with the piece/pawn
            # at the starting position
            self.board[start_row][start_col], self.board[end_row][end_col] = '', self.board[start_row][
                start_col]
            # initialized after making a move
            self.last_move = [start_move, destination_move]
            self.move_made.append(self.last_move)
            self.move_made_in_uci.append(SQUARES[start_move] + SQUARES[destination_move])
            # check for promotion
            if self.board[end_row][end_col].lower() == 'p' and (end_row == 7 or end_row == 0):
                self.board[end_row][end_col] = promote if promote is not None else self.pawn_promotion(end_row, end_col)
                self.move_made_in_uci[-1] += self.board[end_row][end_col]
            copy = deepcopy(self.board)
            self.board_history.append(copy)
            self.white_turn = not self.white_turn
            if self.is_checkmate() and not is_analyzing:
                pygame.quit()

            self.start_move = (None, None)
            self.destination_move = (None, None)
            self.delay = 0

    def undo_move(self, SCREEN=SCREEN):
        try:
            self.white_turn = not self.white_turn
            self.start_move = (None, None)
            self.destination_move = (None, None)
            self.last_move = [(None, None), (None, None)]
            last_move = self.move_made.pop()
            self.move_animation(last_move[1], last_move[0], SCREEN)
            self.move_made_in_uci.pop()
            self.board_history.pop()
            tmp = []
            for i in range(8):
                lst_tmp = []
                for j in range(8):
                    lst_tmp.append(self.board_history[-1][i][j])
                tmp.append(lst_tmp)
            self.board = tmp

            self.en_passant_history.pop()
            self.en_passant = self.en_passant_history[-1]
            self.delay = 0
        except IndexError:
            self.__init__()

    def print_board(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] != '':
                    print(board[i][j], end='')
                else:
                    print(' ', end='')
            print()

    def get_all_legal_moves(self, white_turn):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if white_turn and self.board[i][j].islower():
                    moves = self.get_legal_moves(i, j, white_turn)
                    for move in moves:
                        legal_moves.append([(i, j), move])
                if not white_turn and self.board[i][j].isupper():
                    moves = self.get_legal_moves(i, j, white_turn)
                    for move in moves:
                        legal_moves.append([(i, j), move])
        return legal_moves

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
        if self.board[row][col] == 'k':
            check_long_castle, check_short_castle = self.check_castling_right()
            if check_long_castle:
                final_legal_moves.append((7, 2))
            if check_short_castle:
                final_legal_moves.append((7, 6))
        elif self.board[row][col] == 'K':
            check_long_castle, check_short_castle = self.check_castling_right()
            if check_long_castle:
                final_legal_moves.append((0, 2))
            if check_short_castle:
                final_legal_moves.append((0, 6))
        return final_legal_moves

    def get_legal_moves_knight(self, row, col):
        legal_moves = []
        if self.check_valid(row + 2, col - 1) and (
                self.board[row + 2][col - 1] == '' or self.check_diff_side(row, col, row + 2, col - 1)):
            legal_moves.append((row + 2, col - 1))
        if self.check_valid(row + 2, col + 1) and (
                self.board[row + 2][col + 1] == '' or self.check_diff_side(row, col, row + 2, col + 1)):
            legal_moves.append((row + 2, col + 1))
        if self.check_valid(row - 2, col - 1) and (
                self.board[row - 2][col - 1] == '' or self.check_diff_side(row, col, row - 2, col - 1)):
            legal_moves.append((row - 2, col - 1))
        if self.check_valid(row - 2, col + 1) and (
                self.board[row - 2][col + 1] == '' or self.check_diff_side(row, col, row - 2, col + 1)):
            legal_moves.append((row - 2, col + 1))
        if self.check_valid(row + 1, col - 2) and (
                self.board[row + 1][col - 2] == '' or self.check_diff_side(row, col, row + 1, col - 2)):
            legal_moves.append((row + 1, col - 2))
        if self.check_valid(row + 1, col + 2) and (
                self.board[row + 1][col + 2] == '' or self.check_diff_side(row, col, row + 1, col + 2)):
            legal_moves.append((row + 1, col + 2))
        if self.check_valid(row - 1, col - 2) and (
                self.board[row - 1][col - 2] == '' or self.check_diff_side(row, col, row - 1, col - 2)):
            legal_moves.append((row - 1, col - 2))
        if self.check_valid(row - 1, col + 2) and (
                self.board[row - 1][col + 2] == '' or self.check_diff_side(row, col, row - 1, col + 2)):
            legal_moves.append((row - 1, col + 2))
        return legal_moves

    def get_legal_moves_rook(self, row, col):
        legal_moves = []
        for i in range(col + 1, 8):
            if self.board[row][i] != '':
                if self.check_diff_side(row, col, row, i):
                    legal_moves.append((row, i))
                break
            legal_moves.append((row, i))
        for i in range(col - 1, -1, -1):
            if self.board[row][i] != '':
                if self.check_diff_side(row, col, row, i):
                    legal_moves.append((row, i))
                break
            legal_moves.append((row, i))
        for i in range(row - 1, -1, -1):
            if self.board[i][col] != '':
                if self.check_diff_side(row, col, i, col):
                    legal_moves.append((i, col))
                break
            legal_moves.append((i, col))
        for i in range(row + 1, 8):
            if self.board[i][col] != '':
                if self.check_diff_side(row, col, i, col):
                    legal_moves.append((i, col))
                break
            legal_moves.append((i, col))
        return legal_moves

    def get_legal_moves_king(self, row, col):
        legal_moves = []
        if self.check_valid(row, col + 1) and (
                self.board[row][col + 1] == '' or self.check_diff_side(row, col, row, col + 1)):
            legal_moves.append((row, col + 1))
        if self.check_valid(row, col - 1) and (
                self.board[row][col - 1] == '' or self.check_diff_side(row, col, row, col - 1)):
            legal_moves.append((row, col - 1))
        if self.check_valid(row - 1, col - 1) and (
                self.board[row - 1][col - 1] == '' or self.check_diff_side(row, col, row - 1, col - 1)):
            legal_moves.append((row - 1, col - 1))
        if self.check_valid(row - 1, col + 1) and (
                self.board[row - 1][col + 1] == '' or self.check_diff_side(row, col, row - 1, col + 1)):
            legal_moves.append((row - 1, col + 1))
        if self.check_valid(row - 1, col) and (
                self.board[row - 1][col] == '' or self.check_diff_side(row, col, row - 1, col)):
            legal_moves.append((row - 1, col))
        if self.check_valid(row + 1, col + 1) and (
                self.board[row + 1][col + 1] == '' or self.check_diff_side(row, col, row + 1, col + 1)):
            legal_moves.append((row + 1, col + 1))
        if self.check_valid(row + 1, col) and (
                self.board[row + 1][col] == '' or self.check_diff_side(row, col, row + 1, col)):
            legal_moves.append((row + 1, col))
        if self.check_valid(row + 1, col - 1) and (
                self.board[row + 1][col - 1] == '' or self.check_diff_side(row, col, row + 1, col - 1)):
            legal_moves.append((row + 1, col - 1))
        return legal_moves

    def get_legal_moves_bishop(self, row, col):
        legal_moves = []
        i = 1

        while True:
            if not self.check_valid(row - i, col - i):
                break
            if self.board[row - i][col - i] != '':
                if self.check_diff_side(row, col, row - i, col - i):
                    legal_moves.append((row - i, col - i))
                break
            legal_moves.append((row - i, col - i))

            i += 1
        i = 1

        while True:
            if not self.check_valid(row + i, col - i):
                break
            if self.board[row + i][col - i] != '':
                if self.check_diff_side(row, col, row + i, col - i):
                    legal_moves.append((row + i, col - i))
                break
            legal_moves.append((row + i, col - i))

            i += 1
        i = 1

        while True:
            if not self.check_valid(row + i, col + i):
                break
            if self.board[row + i][col + i] != '':
                if self.check_diff_side(row, col, row + i, col + i):
                    legal_moves.append((row + i, col + i))
                break
            legal_moves.append((row + i, col + i))

            i += 1
        i = 1

        while True:
            if not self.check_valid(row - i, col + i):
                break
            if self.board[row - i][col + i] != '':
                if self.check_diff_side(row, col, row - i, col + i):
                    legal_moves.append((row - i, col + i))
                break
            legal_moves.append((row - i, col + i))

            i += 1

        return legal_moves

    def get_legal_moves_white_pawn(self, row, col):
        legal_moves = []
        if self.check_valid(row - 1, col - 1) and self.board[row - 1][col - 1] != '' and self.check_diff_side(row,
                                                                                                              col,
                                                                                                              row - 1,
                                                                                                              col - 1):
            legal_moves.append((row - 1, col - 1))
        if self.check_valid(row - 1, col + 1) and self.board[row - 1][col + 1] != '' and self.check_diff_side(row,
                                                                                                              col,
                                                                                                              row - 1,
                                                                                                              col + 1):
            legal_moves.append((row - 1, col + 1))
        # check if it can be en passant move or not
        if self.en_passant != (None, None):
            r, c = self.en_passant
            if abs(col - c) == 1 and r == row:
                self.board[r][c] = ''
                self.board[row][col], self.board[row - 1][col + (c - col)] = '', 'p'
                if self.get_king_position('WHITE') not in self.get_black_attack_square():
                    legal_moves.append((row - 1, col + (c - col)))
                self.board[r][c] = 'P'
                self.board[row][col], self.board[row - 1][col + (c - col)] = 'p', ''
        # if the pawn is in the starting position
        if row == 6:
            if self.check_valid(row - 1, col) and self.board[row - 1][col] == '':
                legal_moves.append((row - 1, col))
            if self.check_valid(row - 2, col) and self.board[row - 2][col] == '' and self.board[row - 1][col] == '':
                legal_moves.append((row - 2, col))

        else:
            if self.check_valid(row - 1, col) and self.board[row - 1][col] == '':
                legal_moves.append((row - 1, col))

        return legal_moves

    def get_legal_moves_black_pawn(self, row, col):
        legal_moves = []
        if self.check_valid(row + 1, col - 1) and self.board[row + 1][col - 1] != '' and self.check_diff_side(row,
                                                                                                              col,
                                                                                                              row + 1,
                                                                                                              col - 1):
            legal_moves.append((row + 1, col - 1))
        if self.check_valid(row + 1, col + 1) and self.board[row + 1][col + 1] != '' and self.check_diff_side(row,
                                                                                                              col,
                                                                                                              row + 1,
                                                                                                              col + 1):
            legal_moves.append((row + 1, col + 1))
        # check for en passant
        if self.en_passant != (None, None):
            r, c = self.en_passant
            if abs(col - c) == 1 and r == row:
                self.board[r][c] = ''
                self.board[row][col], self.board[row + 1][col + (c - col)] = '', 'P'
                if self.get_king_position('BLACK') not in self.get_white_attack_square():
                    legal_moves.append((row + 1, col + (c - col)))
                    # print(1)
                self.board[r][c] = 'p'
                self.board[row][col], self.board[row + 1][col + (c - col)] = 'P', ''
        # if the pawn is in the starting position
        if row == 1:
            if self.check_valid(row + 1, col) and self.board[row + 1][col] == '':
                legal_moves.append((row + 1, col))
            if self.check_valid(row + 2, col) and self.board[row + 2][col] == '' and self.board[row + 1][col] == '':
                legal_moves.append((row + 2, col))

        else:
            if self.check_valid(row + 1, col) and self.board[row + 1][col] == '':
                legal_moves.append((row + 1, col))

        return legal_moves

    def get_legal_moves_queen(self, row, col):
        legal_moves = self.get_legal_moves_rook(row, col) + self.get_legal_moves_bishop(row, col)
        return legal_moves

    def draw_legal_moves(self):
        curr_row, curr_col = self.start_move
        legal_moves = self.get_legal_moves(curr_row, curr_col, self.white_turn)
        for row, col in legal_moves:
            center = self.board_coordinate[row][col].center
            pygame.draw.circle(SCREEN, GREEN, center, 10)

    # method to get the attack squares of the piece ,including the squares of the blocking pieces of the same side
    def get_attack_square(self, row, col):
        attack_square = []
        if row is None or col is None:
            return []
        if self.board[row][col] == 'p':
            if self.check_valid(row - 1, col - 1):
                attack_square.append((row - 1, col - 1))
            if self.check_valid(row - 1, col + 1):
                attack_square.append((row - 1, col + 1))

        elif self.board[row][col] == 'P':
            if self.check_valid(row + 1, col - 1):
                attack_square.append((row + 1, col - 1))
            if self.check_valid(row + 1, col + 1):
                attack_square.append((row + 1, col + 1))
        # attack squares of white rook and black rook
        elif (self.board[row][col] == 'r') or (self.board[row][col] == 'R'):
            for i in range(col + 1, 8):
                if self.board[row][i] != '':
                    attack_square.append((row, i))
                    break
                attack_square.append((row, i))
            for i in range(col - 1, -1, -1):
                if self.board[row][i] != '':
                    attack_square.append((row, i))
                    break
                attack_square.append((row, i))
            for i in range(row - 1, -1, -1):
                if self.board[i][col] != '':
                    attack_square.append((i, col))
                    break
                attack_square.append((i, col))
            for i in range(row + 1, 8):
                if self.board[i][col] != '':
                    attack_square.append((i, col))
                    break
                attack_square.append((i, col))
        # attack squares of white bishop and black bishop
        elif (self.board[row][col] == 'b') or (self.board[row][col] == 'B'):
            i = 1

            while True:
                if not self.check_valid(row - i, col - i):
                    break
                if self.board[row - i][col - i] != '':
                    attack_square.append((row - i, col - i))
                    break
                attack_square.append((row - i, col - i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row + i, col - i):
                    break
                if self.board[row + i][col - i] != '':
                    attack_square.append((row + i, col - i))
                    break
                attack_square.append((row + i, col - i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row + i, col + i):
                    break
                if self.board[row + i][col + i] != '':
                    attack_square.append((row + i, col + i))
                    break
                attack_square.append((row + i, col + i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row - i, col + i):
                    break
                if self.board[row - i][col + i] != '':
                    attack_square.append((row - i, col + i))
                    break
                attack_square.append((row - i, col + i))

                i += 1
        # attack_squares of black and white knight
        elif (self.board[row][col] == 'n') or (self.board[row][col] == 'N'):
            if self.check_valid(row + 2, col - 1):
                attack_square.append((row + 2, col - 1))
            if self.check_valid(row + 2, col + 1):
                attack_square.append((row + 2, col + 1))
            if self.check_valid(row - 2, col - 1):
                attack_square.append((row - 2, col - 1))
            if self.check_valid(row - 2, col + 1):
                attack_square.append((row - 2, col + 1))
            if self.check_valid(row + 1, col - 2):
                attack_square.append((row + 1, col - 2))
            if self.check_valid(row + 1, col + 2):
                attack_square.append((row + 1, col + 2))
            if self.check_valid(row - 1, col - 2):
                attack_square.append((row - 1, col - 2))
            if self.check_valid(row - 1, col + 2):
                attack_square.append((row - 1, col + 2))
        # attack squares of white and black king
        elif (self.board[row][col] == 'k') or (self.board[row][col] == 'K'):
            if self.check_valid(row, col + 1):
                attack_square.append((row, col + 1))
            if self.check_valid(row, col - 1):
                attack_square.append((row, col - 1))
            if self.check_valid(row - 1, col - 1):
                attack_square.append((row - 1, col - 1))
            if self.check_valid(row - 1, col + 1):
                attack_square.append((row - 1, col + 1))
            if self.check_valid(row - 1, col):
                attack_square.append((row - 1, col))
            if self.check_valid(row + 1, col + 1):
                attack_square.append((row + 1, col + 1))
            if self.check_valid(row + 1, col):
                attack_square.append((row + 1, col))
            if self.check_valid(row + 1, col - 1):
                attack_square.append((row + 1, col - 1))
        # attack squares of white queen and black queen
        elif (self.board[row][col] == 'q') or (self.board[row][col] == 'Q'):
            for i in range(col + 1, 8):
                if self.board[row][i] != '':
                    attack_square.append((row, i))
                    break
                attack_square.append((row, i))
            for i in range(col - 1, -1, -1):
                if self.board[row][i] != '':
                    attack_square.append((row, i))
                    break
                attack_square.append((row, i))
            for i in range(row - 1, -1, -1):
                if self.board[i][col] != '':
                    attack_square.append((i, col))
                    break
                attack_square.append((i, col))
            for i in range(row + 1, 8):
                if self.board[i][col] != '':
                    attack_square.append((i, col))
                    break
                attack_square.append((i, col))
            i = 1

            while True:
                if not self.check_valid(row - i, col - i):
                    break
                if self.board[row - i][col - i] != '':
                    attack_square.append((row - i, col - i))
                    break
                attack_square.append((row - i, col - i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row + i, col - i):
                    break
                if self.board[row + i][col - i] != '':
                    attack_square.append((row + i, col - i))
                    break
                attack_square.append((row + i, col - i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row + i, col + i):
                    break
                if self.board[row + i][col + i] != '':
                    attack_square.append((row + i, col + i))
                    break
                attack_square.append((row + i, col + i))

                i += 1
            i = 1

            while True:
                if not self.check_valid(row - i, col + i):
                    break
                if self.board[row - i][col + i] != '':
                    attack_square.append((row - i, col + i))
                    break
                attack_square.append((row - i, col + i))

                i += 1
        return attack_square

    def get_white_attack_square(self):
        attack_square = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '' and self.board[i][j].islower():
                    attack_square += self.get_attack_square(i, j)
        return list(set(attack_square))

    def get_black_attack_square(self):
        attack_square = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '' and self.board[i][j].isupper():
                    attack_square += self.get_attack_square(i, j)
        return list(set(attack_square))

    def get_king_position(self, side):
        if side == 'BLACK':
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'K':
                        return i, j
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'k':
                        return i, j

    def is_in_check(self):
        if self.white_turn:
            unavailable_squares = self.get_black_attack_square()
            if self.get_king_position('WHITE') in unavailable_squares:
                return True
            return False
        else:
            unavailable_squares = self.get_white_attack_square()
            if self.get_king_position('BLACK') in unavailable_squares:
                return True
            return False

    def is_checkmate(self):
        if self.is_in_check():
            if self.white_turn:
                legal_moves = []
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j] != '' and self.board[i][j].islower():
                            legal_moves += self.get_legal_moves(i, j, self.white_turn)

                if len(legal_moves) == 0:
                    return True

                return False
            else:
                legal_moves = []
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j] != '' and self.board[i][j].isupper():
                            legal_moves += self.get_legal_moves(i, j, self.white_turn)
                if len(legal_moves) == 0:
                    return True
                return False

    def check_castling_right(self):
        if self.is_in_check():
            return [False, False]

        ans = [True, True]
        if self.white_turn:
            if self.get_king_position('WHITE') != (7, 4):
                return [False, False]
            # check short and long castle
            for start, end in self.move_made:
                if start == (7, 4):
                    return [False, False]
            for start, end in self.move_made:
                if start == (7, 7) or end == (7, 7):
                    ans[1] = False
                if start == (7, 0) or end == (7, 0):
                    ans[0] = False
            attack_squares = self.get_black_attack_square()
            if ans[1]:
                if (7, 5) in attack_squares or (7, 6) in attack_squares:
                    ans[1] = False
                if self.board[7][5] != '' or self.board[7][6] != '':
                    ans[1] = False
            if ans[0]:
                if (7, 2) in attack_squares or (7, 3) in attack_squares:
                    ans[0] = False
                if self.board[7][1] != '' or self.board[7][2] != '' or self.board[7][3] != '':
                    ans[0] = False
        else:
            if self.get_king_position('BLACK') != (0, 4):
                return [False, False]
            for start, end in self.move_made:
                if start == (0, 4):
                    return [False, False]
            for start, end in self.move_made:
                if start == (0, 7) or end == (0, 7):
                    ans[1] = False
                if start == (0, 0) or end == (0, 0):
                    ans[0] = False
            attack_squares = self.get_white_attack_square()
            if ans[1]:
                if (0, 5) in attack_squares or (0, 6) in attack_squares:
                    ans[1] = False
                if self.board[0][5] != '' or self.board[0][6] != '':
                    ans[1] = False
            if ans[0]:
                if (0, 2) in attack_squares or (0, 3) in attack_squares:
                    ans[0] = False
                if self.board[0][1] != '' or self.board[0][2] != '' or self.board[0][3] != '':
                    ans[0] = False
        return ans

    def pawn_promotion(self, row, col):
        # queen,rook,knight,bishop
        while True:
            if self.white_turn:
                if col >= 4:
                    rect_1 = self.white_queen_img.get_rect(center=self.board_coordinate[row][col - 1].center)
                    rect_2 = self.white_rook_img.get_rect(center=self.board_coordinate[row + 1][col - 1].center)
                    rect_3 = self.white_bishop_img.get_rect(center=self.board_coordinate[row + 2][col - 1].center)
                    rect_4 = self.white_knight_img.get_rect(center=self.board_coordinate[row + 3][col - 1].center)
                else:
                    rect_1 = self.white_queen_img.get_rect(center=self.board_coordinate[row][col + 1].center)
                    rect_2 = self.white_rook_img.get_rect(center=self.board_coordinate[row + 1][col + 1].center)
                    rect_3 = self.white_bishop_img.get_rect(center=self.board_coordinate[row + 2][col + 1].center)
                    rect_4 = self.white_knight_img.get_rect(center=self.board_coordinate[row + 3][col + 1].center)
                rect_5 = pygame.rect.Rect(0, 0, 75, 300)
                rect_5.midtop = rect_1.midtop
                pygame.draw.rect(SCREEN, WHITE, rect_5)
                SCREEN.blit(self.white_queen_img, rect_1)
                SCREEN.blit(self.white_rook_img, rect_2)
                SCREEN.blit(self.white_bishop_img, rect_3)
                SCREEN.blit(self.white_knight_img, rect_4)
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if rect_1.x <= x <= rect_1.x + 75 and rect_1.y <= y <= rect_1.y + 75:
                        return 'q'
                    elif rect_2.x <= x <= rect_2.x + 75 and rect_2.y <= y <= rect_2.y + 75:
                        return 'r'
                    elif rect_3.x <= x <= rect_3.x + 75 and rect_3.y <= y <= rect_3.y + 75:
                        return 'b'
                    elif rect_4.x <= x <= rect_4.x + 75 and rect_4.y <= y <= rect_4.y + 75:
                        return 'n'
            else:
                if col >= 4:
                    rect_1 = self.black_queen_img.get_rect(center=self.board_coordinate[row][col - 1].center)
                    rect_2 = self.black_rook_img.get_rect(center=self.board_coordinate[row - 1][col - 1].center)
                    rect_3 = self.black_bishop_img.get_rect(center=self.board_coordinate[row - 2][col - 1].center)
                    rect_4 = self.black_knight_img.get_rect(center=self.board_coordinate[row - 3][col - 1].center)
                else:
                    rect_1 = self.black_queen_img.get_rect(center=self.board_coordinate[row][col + 1].center)
                    rect_2 = self.black_rook_img.get_rect(center=self.board_coordinate[row - 1][col + 1].center)
                    rect_3 = self.black_bishop_img.get_rect(center=self.board_coordinate[row - 2][col + 1].center)
                    rect_4 = self.black_knight_img.get_rect(center=self.board_coordinate[row - 3][col + 1].center)
                rect_5 = pygame.rect.Rect(0, 0, 75, 300)
                rect_5.midbottom = rect_1.midbottom
                pygame.draw.rect(SCREEN, WHITE, rect_5)
                SCREEN.blit(self.black_queen_img, rect_1)
                SCREEN.blit(self.black_rook_img, rect_2)
                SCREEN.blit(self.black_bishop_img, rect_3)
                SCREEN.blit(self.black_knight_img, rect_4)
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if rect_1.x <= x <= rect_1.x + 75 and rect_1.y <= y <= rect_1.y + 75:
                        return 'Q'
                    elif rect_2.x <= x <= rect_2.x + 75 and rect_2.y <= y <= rect_2.y + 75:
                        return 'R'
                    elif rect_3.x <= x <= rect_3.x + 75 and rect_3.y <= y <= rect_3.y + 75:
                        return 'B'
                    elif rect_4.x <= x <= rect_4.x + 75 and rect_4.y <= y <= rect_4.y + 75:
                        return 'N'
            check_quit_game()
            pygame.display.update()
            CLOCK.tick(120)

    # draw the arrow to display surface depends ond the last move
    def draw_arrow(self, SCREEN=SCREEN):
        def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=2):
            rad = math.pi / 180
            pygame.draw.line(screen, lcolor, start, end, thickness)
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
            pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                                    end[1] + trirad * math.cos(rotation)),
                                                   (end[0] + trirad * math.sin(rotation - 120 * rad),
                                                    end[1] + trirad * math.cos(rotation - 120 * rad)),
                                                   (end[0] + trirad * math.sin(rotation + 120 * rad),
                                                    end[1] + trirad * math.cos(rotation + 120 * rad))))

        if self.last_move != [(None, None), (None, None)]:
            start_move, destination_move = self.last_move
            srow, scol = start_move
            drow, dcol = destination_move
            dcenter_x, dcenter_y = self.board_coordinate[drow][dcol].center
            if srow > drow:
                dcenter_y += 30
            if srow < drow:
                dcenter_y -= 30
            if scol > dcol:
                dcenter_x += 25
            if scol < dcol:
                dcenter_x -= 25
            if srow == drow:
                if scol > dcol:
                    dcenter_x += 12
                else:
                    dcenter_x -= 12
            arrow(SCREEN, YELLOW, YELLOW, self.board_coordinate[srow][scol].center, (dcenter_x, dcenter_y), 12, 8)

    # method to animate the move for UI purposes
    def move_animation(self, start_move, destination_move, SCREEN=SCREEN):
        start_row, start_col = start_move
        end_row, end_col = destination_move
        x_start, y_start = self.board_coordinate[start_row][start_col].center
        x_end, y_end = self.board_coordinate[end_row][end_col].center
        time = 15
        x_step = (x_end - x_start) / time
        y_step = (y_end - y_start) / time
        img = self.map[self.board[start_row][start_col]]
        LOCAL_CLOCK = pygame.time.Clock()
        for i in range(time):
            SCREEN.fill(WHITE)
            self.draw_board(SCREEN)
            if type(self)==Board:
                self.display_time(SCREEN)
            for j in range(8):
                for k in range(8):
                    if self.board[j][k] != '' and (j, k) != start_move:
                        img1 = self.map[self.board[j][k]]
                        rect = img1.get_rect(center=self.board_coordinate[j][k].center)
                        SCREEN.blit(img1, rect)
            rect = img.get_rect(center=(x_start + x_step * i, y_start + y_step * i))
            SCREEN.blit(img, rect)
            check_quit_game()
            pygame.display.update()
            LOCAL_CLOCK.tick(60)

    @staticmethod
    def convert_time(float_time):
        minute = int(float_time // 60)
        second = int(float_time) - minute * 60
        milisecond = int((float_time - int(float_time)) * 100)
        return f'{minute:02d}:{second:02d}:{milisecond:02d}'

    # display the time onto the display surface
    def display_time(self, SCREEN=SCREEN):
        if self.white_turn:
            self.white_time = self.white_time - (time.perf_counter() - self.time_start)
            self.time_start = time.perf_counter()
        else:
            self.black_time = self.black_time - (time.perf_counter() - self.time_start)
            self.time_start = time.perf_counter()
        white_time_rect = create_rect(SCREEN, 750, 450, 150, 50, BLACK, 3)
        black_time_rect = create_rect(SCREEN, 750, 150, 150, 50, BLACK, 3)
        create_text_center(SCREEN, self.convert_time(self.white_time), white_time_rect.center, BLACK, 30)
        create_text_center(SCREEN, self.convert_time(self.black_time), black_time_rect.center, BLACK, 30)

    def check_timeout(self):
        if self.black_time <= 0 or self.white_time <= 0:
            pygame.quit()
