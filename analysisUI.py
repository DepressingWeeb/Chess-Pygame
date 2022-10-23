import pygame.time

from utils import *
from analysis_board import AnalysisBoard


def analysis_waiting(moves_count, q):
    val = 0
    pygame.init()
    while True:
        SCREEN.fill(WHITE)
        if not q.empty():
            val = q.get()
            if val == moves_count - 1:
                pygame.quit()
                break
        create_text(SCREEN, f'{val}/{moves_count - 1}', (WIDTH // 2, HEIGHT // 2), BLACK, 50)
        check_quit_game()
        pygame.display.update()
        CLOCK.tick(20)


def analysis_ui(acc_white, acc_black, count_type_white, count_type_black):
    SCREEN_ANALYSIS = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK_ANALYSIS = pygame.time.Clock()
    pygame.init()
    while True:
        SCREEN_ANALYSIS.fill(LYNCH)
        rect = create_rect(SCREEN_ANALYSIS, 150, 100, 150, 50, YELLOW, 5)
        create_rect(SCREEN_ANALYSIS, 150, 100, 140, 40, WHITE)
        create_text_center(SCREEN_ANALYSIS, '{:.2f}'.format(acc_white), rect.center, BLACK, 30)
        rect_1 = create_rect(SCREEN_ANALYSIS, 450, 100, 150, 50, GREEN, 5)
        create_rect(SCREEN_ANALYSIS, 450, 100, 140, 40, BLACK)
        create_text_center(SCREEN_ANALYSIS, '{:.2f}'.format(acc_black), rect_1.center, WHITE, 30)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[0]}               Best Moves               {count_type_black[0]}',
                           (300, 200), LIME)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[1]}                Excellent                {count_type_black[1]}',
                           (300, 250), GREEN)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[2]}                  Good                  {count_type_black[2]}',
                           (300, 300), LIGHT_GREEN)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[3]}               Inaccuracy               {count_type_black[3]}',
                           (300, 350), LIGHT_YELLOW)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[4]}                 Mistake                 {count_type_black[4]}',
                           (300, 400), ORANGE)
        create_text_center(SCREEN_ANALYSIS,
                           f'{count_type_white[5]}                 Blunder                 {count_type_black[5]}',
                           (300, 450), RED)

        check_quit_game()
        if pygame.key.get_pressed()[K_a]:
            return
        pygame.display.update()
        CLOCK_ANALYSIS.tick(30)

    pass


def analysis_detail(SCREEN, move_made, move_made_in_uci, types):
    a_board = AnalysisBoard(move_made, move_made_in_uci, types)
    CLOCK_ANALYSIS = pygame.time.Clock()
    while True:
        SCREEN.fill(WHITE)
        a_board.draw_board(SCREEN)
        a_board.draw_arrow(SCREEN)
        a_board.draw_pieces(SCREEN)
        a_board.draw_label(SCREEN)
        a_board.check_key(SCREEN)
        check_quit_game()
        pygame.display.update()
        CLOCK_ANALYSIS.tick(60)
