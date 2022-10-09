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
            pygame.display.update()
            CLOCK.tick(120)
        except pygame.error:
            break



# board.test()
if __name__=='__main__':
    import multiprocessing
    from constants import *
    from board import Board
    from utils import *
    from analysis import *
    from analysisUI import *
    #SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    #CLOCK = pygame.time.Clock()
    board=Board()
    game = True
    pygame.init()
    main_loop()
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=analysis_waiting, args=(q,))
    p2 = multiprocessing.Process(target=analysis, args=(board.move_made_in_uci, q))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

