import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MineSweeper")


running = True
while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False


pygame.quit()
