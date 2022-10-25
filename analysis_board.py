from utils import *
from board import Board


class AnalysisBoard(Board):
    def __init__(self, move_made, move_made_in_uci, types):
        super().__init__()
        self.move_made_analysis = move_made
        self.move_made_in_uci_analysis = move_made_in_uci
        self.index = -1
        self.types = types
        self.best_img = pygame.image.load(r"resources\chesscom-labels\32x\best_32x.png")
        self.excellent_img = pygame.image.load(r"resources\chesscom-labels\32x\excellent_32x.png")
        self.good_img = pygame.image.load(r"resources\chesscom-labels\32x\good_32x.png")
        self.inaccuracy_img = pygame.image.load(r"resources\chesscom-labels\32x\inaccuracy_32x.png")
        self.mistake_img = pygame.image.load(r"resources\chesscom-labels\32x\mistake_32x.png")
        self.blunder_img = pygame.image.load(r"resources\chesscom-labels\32x\blunder_32x.png")

    def check_key(self,SCREEN=SCREEN):
        if self.delay >= 0:
            self.delay += 1
            if self.delay == 15:
                self.delay = -1
            return
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.index = max(self.index - 1, -1)
            self.delay = 0
            if self.index == -1:
                self.__init__(self.move_made_analysis, self.move_made_in_uci_analysis, self.types)
            else:
                self.undo_move(SCREEN)
        elif keys[K_RIGHT]:
            self.index = min(self.index + 1, len(self.move_made_analysis) - 1)
            if self.move_made_in_uci_analysis[self.index][-1].isdigit():
                self.move(self.move_made_analysis[self.index][0], self.move_made_analysis[self.index][1], None, True,SCREEN)
                self.delay = 0
            else:
                self.move(self.move_made_analysis[self.index][0], self.move_made_analysis[self.index][1],
                          self.move_made_in_uci_analysis[self.index][-1], True,SCREEN)
                self.delay = 0

    def draw_label(self, SCREEN=SCREEN):
        if self.index == -1:
            return
        type_dict = {
            0: self.best_img,
            1: self.excellent_img,
            2: self.good_img,
            3: self.inaccuracy_img,
            4: self.mistake_img,
            5: self.blunder_img
        }
        row, col = self.move_made_analysis[self.index][1]
        rect = type_dict[self.types[self.index]].get_rect(center=self.board_coordinate[row][col].topright)
        SCREEN.blit(type_dict[self.types[self.index]], rect)
