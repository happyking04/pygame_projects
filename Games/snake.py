import pygame
import random

pygame.init()

width = 800
height = 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong Game')


paddle_width = 10
paddle_height = 100
paddle_speed = 10

paddle1_x = 50
paddle1_y = height / 2 - paddle_height / 2

paddle2_x = width - 50 - paddle_width
paddle2_y = height / 2 - paddle_height / 2

ball_size = 10
ball_speed_x = 5
ball_speed_y = 5

ball_x = width / 2
ball_y = height / 2


game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_y -= paddle_speed
    elif keys[pygame.K_s]:
        paddle1_y += paddle_speed

    if keys[pygame.K_UP]:
        paddle2_y -= paddle_speed
    elif keys[pygame.K_DOWN]:
        paddle2_y += paddle_speed

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check if the ball hit the wall
    if ball_y <= 0 or ball_y >= height - ball_size:
        ball_speed_y = -ball_speed_y

    # Check if the ball hit the paddle
    if ball_x <= paddle1_x + paddle_width and paddle1_y <= ball_y <= paddle1_y + paddle_height:
        ball_speed_x = -ball_speed_x
    elif ball_x >= paddle2_x - ball_size and paddle2_y <= ball_y <= paddle2_y + paddle_height:
        ball_speed_x = -ball_speed_x

    # Check if the ball went out of bounds
    if ball_x <= 0 or ball_x >= width - ball_size:
        ball_x = width / 2
        ball_y = height / 2
        ball_speed_x = -ball_speed_x
        ball_speed_y = random.choice([-5, 5])

    # Draw the game screen
    game_display.fill((255, 255, 255))
    pygame.draw.rect(game_display, (0, 0, 0), [paddle1_x, paddle1_y, paddle_width, paddle_height])
    pygame.draw.rect(game_display, (0, 0, 0), [paddle2_x, paddle2_y, paddle_width, paddle_height])
    pygame.draw.circle(game_display, (255, 0, 0), (int(ball_x), int(ball_y)), ball_size)
    pygame.display.update()

    # Set the game speed
    clock = pygame.time.Clock()
    clock.tick(60)

# Quit Pygame
pygame.quit()
quit()