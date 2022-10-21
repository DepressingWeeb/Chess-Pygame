import sys
from constants import *

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def create_text(SCREEN, text, coordinate, color=BLACK, fontSize=20):
    mytext = pygame.font.Font("freesansbold.ttf", fontSize)
    text_surface = mytext.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = coordinate
    SCREEN.blit(text_surface, text_rect)


def create_text_center(SCREEN, text, coordinate, color=BLACK, fontSize=20):
    mytext = pygame.font.Font("freesansbold.ttf", fontSize)
    text_surface = mytext.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = coordinate
    SCREEN.blit(text_surface, text_rect)


def create_rect(SCREEN, x, y, w, h, color, width=0):
    rect = pygame.rect.Rect(x, y, w, h)
    rect.center = (x, y)
    pygame.draw.rect(SCREEN, color, rect, width)
    return rect


def create_button(SCREEN, x, y, w, h, color, color_on_hover, text, text_color=BLACK, text_size=20):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x - w // 2 < mouse_x < x + w // 2 and y - h // 2 < mouse_y < y + h // 2:
        rect = create_rect(SCREEN, x, y, w, h, color_on_hover)
        create_text_center(SCREEN, text, rect.center, text_color, text_size)
        if pygame.mouse.get_pressed()[0]:
            if text == 'Play Bot' or text == 'Single Play':
                return True
            else:
                quit_game()

    else:
        rect = create_rect(SCREEN, x, y, w, h, color)
        create_text_center(SCREEN, text, rect.center, text_color, text_size)
    return None


def quit_game():
    pygame.quit()
    sys.exit()


def check_quit_game():
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
