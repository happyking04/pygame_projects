import pygame
from sys import exit
from win32api import GetSystemMetrics
from random import randint

collide_with_bottom = randint(0, 1)
collide_p2 = randint(0, 1)

ball_vel_x = randint(7, 10)
ball_vel_y = 1
ball_speed_dif = 5
winner_text = ""
PLAYER_VEL = 15
p1_score = 0
p2_score = 0
FPS = 60
game_active = False

pygame.init()
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

font = pygame.font.SysFont('comicsans', 50)
text_surface = font.render('Pong', True, 'Black')

font2 = pygame.font.SysFont('comicsans', 20)
text2_surface = font2.render('Press SPACE to start', True, 'Black')

font3 = pygame.font.SysFont('comicsans', 70)


commercial_ball = pygame.Surface((50, 50))

p1_surface = pygame.Surface((20, 75))
p1_rect = p1_surface.get_rect(center=(25, HEIGHT // 2))

p2_rect = p1_surface.get_rect(center=(WIDTH - 25, HEIGHT // 2))

ball_surface = pygame.Surface((15, 15))
ball_rect = ball_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))


def scores(ball_rect):
    global p1_score, p2_score, collide_with_bottom, collide_p2, ball_vel_x, ball_vel_y
    if ball_rect.right >= WIDTH + 150:
        ball_rect.center = [WIDTH // 2, randint(5, HEIGHT - 5)]
        p1_score += 1
        collide_with_bottom = randint(0, 1)
        collide_p2 = randint(0, 1)
        ball_vel_y = randint(2, 5)
        #p1_rect.center = [25, HEIGHT // 2]
        #p2_rect.center = [WIDTH - 25, HEIGHT // 2]
        ball_vel_x = randint(5, 7)
        #pygame.time.delay(50)
    elif ball_rect.left <= -150:
        ball_rect.center = [WIDTH // 2, randint(5, HEIGHT - 5)]
        p2_score += 1
        collide_with_bottom = randint(0, 1)
        collide_p2 = randint(0, 1)
        #p1_rect.center = [25, HEIGHT // 2]
        #p2_rect.center = [WIDTH - 25, HEIGHT // 2]
        ball_vel_x = randint(5, 7)
        ball_vel_y = randint(2, 5)
        #pygame.time.delay(50)
    p1_score_surface = font3.render(f'{p1_score}', True, 'White')
    p2_score_surface = font3.render(f'{p2_score}', True, 'White')
    WIN.blit(p1_score_surface, (WIDTH // 4, HEIGHT // 2 - 45))
    WIN.blit(p2_score_surface, (WIDTH // 4 * 3, HEIGHT // 2 - 45))
    if p1_score >= 10:
        winner_text = "P1 Wins!"
        return winner_text
    if p2_score >= 10:
        winner_text = "P2 Wins!"
        return winner_text
    return None

def p1_movement(p1_rect):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and p1_rect.y >= 0:
        p1_rect.y -= PLAYER_VEL
    if keys[pygame.K_s] and p1_rect.bottom <= HEIGHT:
        p1_rect.y += PLAYER_VEL
    if keys[pygame.K_a] and p1_rect.left >= 0:
        p1_rect.x -= PLAYER_VEL
    if keys[pygame.K_d] and p1_rect.right <= WIDTH:
        p1_rect.x += PLAYER_VEL

def p2_movement(p2_rect):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and p2_rect.y >= 0:
        p2_rect.y -= PLAYER_VEL
    if keys[pygame.K_DOWN] and p2_rect.bottom <= HEIGHT:
        p2_rect.y += PLAYER_VEL
    if keys[pygame.K_LEFT] and p2_rect.left >= 0:
        p2_rect.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and p2_rect.right <= WIDTH:
        p2_rect.x += PLAYER_VEL

def ball_movement(ball_rect, ball_vel_x, ball_vel_y, p1_rect, p2_rect, ball_speed_dif):
    global collide_with_bottom, collide_p2
    keys = pygame.key.get_pressed()
    if ball_vel_x <= 4:
        ball_vel_x = 5


    if collide_p2:
        ball_rect.x -= ball_vel_x
    else:
        ball_rect.x += ball_vel_x

    if p2_rect.colliderect(ball_rect) and keys[pygame.K_UP]:
        collide_p2 = 1
        ball_vel_x -= ball_speed_dif
        ball_vel_y += 2
    elif p2_rect.colliderect(ball_rect) and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        collide_p2 = 1
        ball_vel_x += 50
    elif p2_rect.colliderect(ball_rect) and keys[pygame.K_DOWN]:
        collide_p2 = 1
        ball_vel_x += ball_speed_dif
        ball_vel_y -= 2
    elif p2_rect.colliderect(ball_rect):
        collide_p2 = 1


    if p1_rect.colliderect(ball_rect) and keys[pygame.K_w]:
        collide_p2 = 0
        ball_vel_x -= ball_speed_dif
        ball_vel_y += 2
    elif p1_rect.colliderect(ball_rect) and keys[pygame.K_s] and keys[pygame.K_d]:
        collide_p2 = 0
        ball_vel_x += 50
    elif p1_rect.colliderect(ball_rect) and keys[pygame.K_s]:
        collide_p2 = 0
        ball_vel_y -= 2
        ball_vel_x += ball_speed_dif
    elif p1_rect.colliderect(ball_rect):
        collide_p2 = 0


    if ball_vel_y <= 0:
        ball_vel_y = 1
    elif ball_vel_y >= 7:
        ball_vel_y = 6

    if ball_rect.bottom <= HEIGHT and not collide_with_bottom:
        ball_rect.y += ball_vel_y
    else:
        collide_with_bottom = 1
    if collide_with_bottom:
        ball_rect.y -= ball_vel_y
    if ball_rect.top <= 0:
        collide_with_bottom = 0
    return ball_vel_x, ball_vel_y




clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    if game_active:
        WIN.fill('Black')
        pygame.draw.rect(WIN, 'White', ball_rect)
        pygame.draw.rect(WIN, 'White', p1_rect, 6)
        pygame.draw.rect(WIN, 'White', p2_rect, 6)

        p1_movement(p1_rect)
        p2_movement(p2_rect)
        winner_text = scores(ball_rect)
        ball_vel_x, ball_vel_y = ball_movement(ball_rect,ball_vel_x, ball_vel_y, p1_rect, p2_rect, ball_speed_dif)
        pygame.display.update()

        if winner_text:
            game_active = False
    else:
        WIN.fill('Green')
        if winner_text != "":
            winner_surface = font.render(winner_text, True, 'Black')
            WIN.blit(winner_surface, (WIDTH // 2 - 95, 25))
        else:
            WIN.blit(text_surface, (WIDTH // 2 - 50, 25))
        WIN.blit(commercial_ball, (WIDTH // 2 - 25, HEIGHT // 2 - 25))
        WIN.blit(text2_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_active = True
            p1_score = 0
            p2_score = 0
            winner_text = ""
            ball_vel_x = randint(7, 10)
            ball_vel_y = 3
            p1_rect.center = [25, HEIGHT // 2]
            p2_rect.center = [WIDTH - 25, HEIGHT // 2]
        pygame.display.update()

    clock.tick(FPS)

