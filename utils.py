import sys
from constants import *


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

def create_rect(SCREEN,x,y,w,h,color,width=0):
    rect=pygame.rect.Rect(x,y,w,h)
    rect.center=(x,y)
    pygame.draw.rect(SCREEN,color,rect,width)
    return rect



def check_quit_game():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
