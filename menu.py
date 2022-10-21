from utils import *


def menu():
    while True:
        SCREEN.fill(WHITE)
        check_quit_game()
        ans1 = create_button(SCREEN, 300, 150, 200, 50, LIGHT_GREEN, LIGHT_YELLOW, 'Play Bot', BLACK, 20)
        ans2 = create_button(SCREEN, 300, 300, 200, 50, LIGHT_GREEN, LIGHT_YELLOW, 'Single Play', BLACK, 20)
        create_button(SCREEN, 300, 450, 200, 50, LIGHT_GREEN, LIGHT_YELLOW, 'Quit', BLACK, 20)
        if any([ans1, ans2]):
            return True if ans1 else False
        pygame.display.update()
        CLOCK.tick(30)
