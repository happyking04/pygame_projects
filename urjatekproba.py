import pygame
from win32api import GetSystemMetrics
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bestest game ever!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
BULLET_VEL = 10
MAX_BULLETS = 0
VEL = 15
ALIEN_VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

space_jazz = pygame.mixer.Sound('Assets\lol.mp3')
space_jazz.set_volume(0.2)
LASER_SHOT = pygame.mixer.Sound('Assets\laser_shot.mp3.mp3')
YELLOW_SPACESHIP_IMAGE = pygame.image.load('Assets\spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load('Assets\spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE_IMAGE = pygame.image.load('Assets\space.png')
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))
ALIEN_IMAGE = pygame.image.load('Assets\Alien.png')
ALIEN = pygame.transform.scale(ALIEN_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
def event_ESC_pressed(get_pressed):
    if get_pressed[pygame.K_ESCAPE]:
        exit()

def alien_controller(yellow, alien):
    if yellow.x > alien.x:
        alien.x += ALIEN_VEL
    if yellow.x < alien.x:
        alien.x -= ALIEN_VEL
    if yellow.y > alien.y:
        alien.y += ALIEN_VEL
    if yellow.y < alien.y:
        alien.y -= ALIEN_VEL



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, alien):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(ALIEN, (alien.x, alien.y))
    if red_health <= 0:
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    elif red_health > 0:
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    if yellow_health <= 0:
     yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, RED)
     WIN.blit(yellow_health_text, (10, 10))
    elif yellow_health > 0:
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_spaceship_movement(yellow):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + SPACESHIP_WIDTH < BORDER.x + 15:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + SPACESHIP_HEIGHT + 15 < HEIGHT:
        yellow.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <= 0:
            red_bullets.remove(bullet)


def red_spaceship_movement(red):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 5:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + SPACESHIP_WIDTH < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + SPACESHIP_HEIGHT + 15 < HEIGHT:
        red.y += VEL



def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    alien = pygame.Rect(400, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        space_jazz.play()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLETS:
                    LASER_SHOT.play()
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) <= MAX_BULLETS:
                    LASER_SHOT.play()
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, alien)
        alien_controller(yellow, alien)
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        get_pressed = pygame.key.get_pressed()
        event_ESC_pressed(get_pressed)
        yellow_spaceship_movement(yellow)
        red_spaceship_movement(red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)


    main()



if __name__ == "__main__":
    main()