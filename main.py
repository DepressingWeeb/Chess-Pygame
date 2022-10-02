# TODO: Analysis (optional)

import pygame
import sys
from pygame.locals import *

WIDTH = 600
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 238, 170, 0.5)
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARES = {
    (0, 0): "a8", (0, 1): "b8", (0, 2): "c8", (0, 3): "d8", (0, 4): "e8", (0, 5): "f8", (0, 6): "g8",
    (0, 7): "h8",
    (1, 0): "a7", (1, 1): "b7", (1, 2): "c7", (1, 3): "d7", (1, 4): "e7", (1, 5): "f7", (1, 6): "g7",
    (1, 7): "h7",
    (2, 0): "a6", (2, 1): "b6", (2, 2): "c6", (2, 3): "d6", (2, 4): "e6", (2, 5): "f6", (2, 6): "g6",
    (2, 7): "h6",
    (3, 0): "a5", (3, 1): "b5", (3, 2): "c5", (3, 3): "d5", (3, 4): "e5", (3, 5): "f5", (3, 6): "g5",
    (3, 7): "h5",
    (4, 0): "a4", (4, 1): "b4", (4, 2): "c4", (4, 3): "d4", (4, 4): "e4", (4, 5): "f4", (4, 6): "g4",
    (4, 7): "h4",
    (5, 0): "a3", (5, 1): "b3", (5, 2): "c3", (5, 3): "d3", (5, 4): "e3", (5, 5): "f3", (5, 6): "g3",
    (5, 7): "h3",
    (6, 0): "a2", (6, 1): "b2", (6, 2): "c2", (6, 3): "d2", (6, 4): "e2", (6, 5): "f2", (6, 6): "g2",
    (6, 7): "h2",
    (7, 0): "a1", (7, 1): "b1", (7, 2): "c1", (7, 3): "d1", (7, 4): "e1", (7, 5): "f1", (7, 6): "g1",
    (7, 7): "h1",
}
pygame.init()


class Board:
    def __init__(self):
        self.start_move = (None, None)
        self.destination_move = (None, None)
        self.delay = -1
        self.white_turn = True
        self.last_move = [(None, None), (None, None)]
        self.move_made = []
        self.en_passant = (None, None)
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

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    SCREEN.blit(self.light_square_img, self.board_coordinate[i][j].topleft)
                    if j == 0:
                        create_text(str(8 - i), self.board_coordinate[i][j].topleft, fontSize=15)
                    if i == 7:
                        x, y = self.board_coordinate[i][j].bottomright
                        create_text(chr(97 + j), (x - 10, y - 15), fontSize=15)
                else:
                    SCREEN.blit(self.dark_square_img, self.board_coordinate[i][j].topleft)
                    if j == 0:
                        create_text(str(8 - i), self.board_coordinate[i][j].topleft, fontSize=15)
                    if i == 7:
                        x, y = self.board_coordinate[i][j].bottomright
                        create_text(chr(97 + j), (x - 10, y - 15), fontSize=15)

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'R':
                    rect = self.black_rook_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_rook_img, rect)
                if self.board[i][j] == 'r':
                    rect = self.white_rook_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_rook_img, rect)
                if self.board[i][j] == 'N':
                    rect = self.black_knight_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_knight_img, rect)
                if self.board[i][j] == 'n':
                    rect = self.white_knight_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_knight_img, rect)
                if self.board[i][j] == 'B':
                    rect = self.black_bishop_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_bishop_img, rect)
                if self.board[i][j] == 'b':
                    rect = self.white_bishop_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_bishop_img, rect)
                if self.board[i][j] == 'Q':
                    rect = self.black_queen_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_queen_img, rect)
                if self.board[i][j] == 'q':
                    rect = self.white_queen_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_queen_img, rect)
                if self.board[i][j] == 'K':
                    rect = self.black_king_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_king_img, rect)
                if self.board[i][j] == 'k':
                    rect = self.white_king_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_king_img, rect)
                if self.board[i][j] == 'P':
                    rect = self.black_pawn_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.black_pawn_img, rect)
                if self.board[i][j] == 'p':
                    rect = self.white_pawn_img.get_rect(center=self.board_coordinate[i][j].center)
                    SCREEN.blit(self.white_pawn_img, rect)

    def check_diff_side(self, row_1, col_1, row_2, col_2):
        return (self.board[row_1][col_1].islower() and self.board[row_2][col_2].isupper()) or (
                self.board[row_1][col_1].isupper() and self.board[row_2][col_2].islower())

    @staticmethod
    def check_valid(row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def move(self):
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
                else:
                    if (row, col) in self.get_legal_moves(self.start_move[0], self.start_move[1]):
                        self.destination_move = (row, col)
                        start_row, start_col = self.start_move
                        end_row, end_col = self.destination_move
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
                        else:
                            self.en_passant = (None, None)

                        self.board[start_row][start_col], self.board[end_row][end_col] = '', self.board[start_row][
                            start_col]
                        if self.board[end_row][end_col].lower() == 'p' and (end_row == 7 or end_row == 0):
                            self.board[end_row][end_col] = self.pawn_promotion(end_row, end_col)

                        self.last_move = [self.start_move, self.destination_move]
                        self.move_made.append(self.last_move)
                        self.white_turn = not self.white_turn
                        if self.is_checkmate():
                            pygame.quit()
                            sys.exit()
                        self.start_move = (None, None)
                        self.destination_move = (None, None)
                        self.delay = 0

                    elif not self.check_diff_side(self.start_move[0], self.start_move[1], row, col):
                        self.start_move = (row, col)

        if self.delay >= 0:
            self.delay += 1
            if self.delay == 15:
                self.delay = -1

    def get_legal_moves(self, row, col):
        legal_moves = []
        if row is None or col is None:
            return []
        if self.board[row][col] == 'p' and self.white_turn:
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
                    legal_moves.append((row - 1, col + (c - col)))
            # if the pawn is in the starting position
            if row == 6:
                if self.check_valid(row - 1, col) and self.board[row - 1][col] == '':
                    legal_moves.append((row - 1, col))
                if self.check_valid(row - 2, col) and self.board[row - 2][col] == '' and self.board[row - 1][col] == '':
                    legal_moves.append((row - 2, col))

            else:
                if self.check_valid(row - 1, col) and self.board[row - 1][col] == '':
                    legal_moves.append((row - 1, col))

        elif self.board[row][col] == 'P' and not self.white_turn:
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
                    legal_moves.append((row + 1, col + (c - col)))
            # if the pawn is in the starting position
            if row == 1:
                if self.check_valid(row + 1, col) and self.board[row + 1][col] == '':
                    legal_moves.append((row + 1, col))
                if self.check_valid(row + 2, col) and self.board[row + 2][col] == '' and self.board[row + 1][col] == '':
                    legal_moves.append((row + 2, col))

            else:
                if self.check_valid(row + 1, col) and self.board[row + 1][col] == '':
                    legal_moves.append((row + 1, col))
        # legal moves of white rook and black rook
        elif (self.board[row][col] == 'r' and self.white_turn) or (self.board[row][col] == 'R' and not self.white_turn):
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
        # legal moves of white bishop and black bishop
        elif (self.board[row][col] == 'b' and self.white_turn) or (self.board[row][col] == 'B' and not self.white_turn):
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
        # legal moves of black and white knight
        elif (self.board[row][col] == 'n' and self.white_turn) or (self.board[row][col] == 'N' and not self.white_turn):
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
        # legal moves of white and black king
        elif (self.board[row][col] == 'k' and self.white_turn) or (self.board[row][col] == 'K' and not self.white_turn):
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
        # legal moves of white queen and black queen
        elif (self.board[row][col] == 'q' and self.white_turn) or (self.board[row][col] == 'Q' and not self.white_turn):
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

        final_legal_moves = []
        for move in legal_moves:
            r, c = row, col
            r1, c1 = move
            temp_1, temp_2 = self.board[r][c], self.board[r1][c1]
            self.board[r][c], self.board[r1][c1] = '', self.board[r][c]
            self.white_turn = not self.white_turn
            if self.white_turn:
                if self.get_king_position('BLACK') not in self.get_white_attack_square():
                    final_legal_moves.append(move)
            else:
                if self.get_king_position('WHITE') not in self.get_black_attack_square():
                    final_legal_moves.append(move)
            self.board[r][c], self.board[r1][c1] = temp_1, temp_2
            self.white_turn = not self.white_turn
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

    def draw_legal_moves(self):
        curr_row, curr_col = self.start_move
        legal_moves = self.get_legal_moves(curr_row, curr_col)
        for row, col in legal_moves:
            center = self.board_coordinate[row][col].center
            pygame.draw.circle(SCREEN, GREEN, center, 10)

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
        # return False
        if self.is_in_check():
            if self.white_turn:
                legal_moves = []
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j] != '' and self.board[i][j].islower():
                            legal_moves += self.get_legal_moves(i, j)

                if len(legal_moves) == 0:
                    return True

                return False
            else:
                legal_moves = []
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j] != '' and self.board[i][j].isupper():
                            legal_moves += self.get_legal_moves(i, j)
                if len(legal_moves) == 0:
                    return True
                return False

    def check_castling_right(self):
        if self.is_in_check():
            return [False, False]
        ans = [True, True]
        if self.white_turn:
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
                if (7, 1) in attack_squares or (7, 2) in attack_squares or (7, 3) in attack_squares:
                    ans[0] = False
                if self.board[7][1] != '' or self.board[7][2] != '' or self.board[7][3] != '':
                    ans[0] = False
        else:
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
                if (0, 1) in attack_squares or (0, 2) in attack_squares or (0, 3) in attack_squares:
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


board = Board()


def create_text(text, coordinate, color=BLACK, fontSize=20):
    mytext = pygame.font.Font("freesansbold.ttf", fontSize)
    text_surface = mytext.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = coordinate
    SCREEN.blit(text_surface, text_rect)


def main_loop():
    while True:
        SCREEN.fill(WHITE)
        board.draw_board()
        board.draw_pieces()
        board.move()
        board.draw_legal_moves()
        check_quit_game()
        pygame.display.update()
        CLOCK.tick(120)


def check_quit_game():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


main_loop()
