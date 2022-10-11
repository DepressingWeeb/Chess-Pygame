# TODO: Analysis (optional)


def main_loop():
    while game:
        try:
            SCREEN.fill(WHITE)
            board.draw_board()
            board.draw_arrow()
            board.draw_pieces()
            board.check_mouse_input()
            board.draw_legal_moves()
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

    board = Board()
    game = True
    pygame.init()
    main_loop()
    q = multiprocessing.Queue()
    acc_white=multiprocessing.Value('f')
    acc_black=multiprocessing.Value('f')
    count_type_white=multiprocessing.Array('i',6)
    count_type_black = multiprocessing.Array('i', 6)
    types=multiprocessing.Array('i',len(board.move_made))
    p1 = multiprocessing.Process(target=analysis_waiting, args=(len(board.move_made_in_uci),q))
    p2 = multiprocessing.Process(target=analysis, args=(board.move_made_in_uci, q,acc_white,acc_black,count_type_white,count_type_black,types))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    SCREEN=analysis_ui(acc_white.value,acc_black.value,count_type_white,count_type_black)
    analysis_detail(SCREEN,board.move_made,board.move_made_in_uci,types)
