import pygame
from win32api import GetSystemMetrics


def event_ESC_pressed(get_pressed):
    if get_pressed[pygame.K_ESCAPE]:
        exit()


WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    get_pressed =  pygame.key.get_pressed()
    event_ESC_pressed(get_pressed)