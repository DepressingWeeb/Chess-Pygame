# TODO: Analysis (optional)
import pygame.display


def main_loop():
    while game:
        try:
            SCREEN.fill(WHITE)
            board.draw_board()
            board.draw_arrow()
            board.draw_pieces()
            board.display_time()
            board.check_mouse_input()
            board.draw_legal_moves()
            board.check_timeout()
            check_quit_game()
            if pygame.key.get_pressed()[K_a]:
                pygame.quit()
                break
            pygame.display.update()
            CLOCK.tick(120)
        except pygame.error:
            break


# board.test()
if __name__ == '__main__':
    import multiprocessing
    from constants import *
    from board import Board
    from utils import *
    from analysis import *
    from analysisUI import *
    from menu import menu

    game = True
    pygame.init()
    is_play_bot = menu()
    board = Board(is_play_bot)
    SCREEN = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    main_loop()
    q = multiprocessing.Queue()
    acc_white = multiprocessing.Value('f')
    acc_black = multiprocessing.Value('f')
    is_terminate=multiprocessing.Value('i')
    count_type_white = multiprocessing.Array('i', 6)
    count_type_black = multiprocessing.Array('i', 6)
    types = multiprocessing.Array('i', len(board.move_made))
    p1 = multiprocessing.Process(target=analysis_waiting, args=(len(board.move_made_in_uci), q,is_terminate))
    p2 = multiprocessing.Process(target=analysis, args=(
        board.move_made_in_uci, q, acc_white, acc_black, count_type_white, count_type_black, types,is_terminate))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(is_terminate)
    if is_terminate == 1:
        quit_game()
    analysis_ui(acc_white.value, acc_black.value, count_type_white, count_type_black)
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    analysis_detail(SCREEN, board.move_made, board.move_made_in_uci, types)
