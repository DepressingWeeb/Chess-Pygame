from utils import *


def analysis_waiting(q):
    val=0
    pygame.init()
    while True:
        SCREEN.fill(WHITE)
        if not q.empty():
            val=q.get()
        create_text(SCREEN,f'{val}',(WIDTH//2,HEIGHT//2),BLACK,50)
        check_quit_game()
        pygame.display.update()
        CLOCK.tick(20)