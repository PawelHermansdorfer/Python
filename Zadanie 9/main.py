import pygame
import time
import random
import numpy as np

pygame.init()
pygame.font.init()

fps = 60
s_per_frame = 1/fps
frame_start = time.perf_counter()
frame_end   = 0
frame_time  = 0

window = pygame.display.set_mode((720, 480), pygame.RESIZABLE)
pygame.display.set_caption('Ping pong')
window_dim = window.get_size()

game_surface = pygame.Surface(window_dim)
score_font = pygame.font.Font(None, 128) 

player_width  = enemy_width  = window_dim[0]/150
player_height = enemy_height = window_dim[1]/6
player_y = window_dim[1]/2 - player_height/2
enemy_y  = window_dim[1]/2 - enemy_height/2

player_dir = enemy_dir = 0
player_vel = 500
enemy_vel = 400

ball_pos = [window_dim[0]/2, window_dim[1]/2]
ball_r = player_height / 10

def get_new_ball_dir():
    return [random.choice([-0.70710678118, 0.70710678118]), # 0.70710678118 == 1/sqrt(2)
            random.choice([-0.70710678118, 0.70710678118])]
ball_dir = get_new_ball_dir()
            
bell_default_vel = 500
ball_vel = bell_default_vel

player_score = 0
enemy_score = 0
winner = 0 # 1-player, 2-computer

stoped = False
while not stoped:
    window_dim = window.get_size()
    window_center = (window_dim[0]/2, window_dim[1]/2)

    ######################################## Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True
        elif event.type == pygame.VIDEORESIZE:
            window_dim = window.get_size()
            game_surface = pygame.Surface(window_dim)

        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q | pygame.K_ESCAPE:
                    stoped = True

                case pygame.K_w | pygame.K_UP:
                    player_dir = -1
                case pygame.K_s | pygame.K_DOWN:
                    player_dir = 1

        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    player_dir = 0
                case pygame.K_s | pygame.K_DOWN:
                    player_dir = 0

    ######################################## Update
    player_x = window_dim[0] * 0.05 - player_width/2
    enemy_x  = window_dim[0] * 0.95 - enemy_width/2

    if frame_time != 0:
        dt = min(frame_time, s_per_frame)

        # Ball
        ball_pos[0] += ball_vel * ball_dir[0] * dt
        ball_pos[1] += ball_vel * ball_dir[1] * dt

        if ball_pos[0] - ball_r <= 0: # left
            enemy_score += 1
            if enemy_score == 11 and winner == 0: winner = 2
            ball_pos = [window_dim[0]/2, window_dim[1]/2]
            ball_dir = get_new_ball_dir()
            ball_vel = bell_default_vel

        if ball_pos[0] + ball_r >= window_dim[0]: # right
            player_score += 1
            if player_score == 11 and winner == 0: winner = 1
            ball_pos = [window_dim[0]/2, window_dim[1]/2]
            ball_dir = get_new_ball_dir()
            ball_vel = bell_default_vel

        if ball_pos[1] <= 0: #
            ball_pos[1] = ball_r
            ball_dir[1] = -ball_dir[1]

        if ball_pos[1] >= window_dim[1]:
            ball_pos[1] = window_dim[1] - ball_r
            ball_dir[1] = -ball_dir[1]

        def collide(x, y, w, h, ball_pos, ball_r):
            x_collide = x - ball_r <= ball_pos[0] <= x + w + ball_r
            y_collide = y - ball_r <= ball_pos[1] <= y + h + ball_r
            return x_collide and y_collide

        ball_vel += 0.5 # increase ball velocity

        # player
        player_y += player_vel * player_dir * dt
        player_y = min(max(player_y, 0), window_dim[1] - player_height) # limit y to screen
        if collide(player_x, player_y, player_width, player_height, ball_pos, ball_r):
            ball_dir[0] = 1
            x = random.uniform(-np.pi/4, np.pi/4)
            ball_dir = [np.cos(x), np.sin(x)]
            ball_pos[0] = player_x + player_width + ball_r

        # enemy
        enemy_center_y = enemy_y + enemy_height/2
        enemy_ball_dist = ball_pos[1] - enemy_center_y
        enemy_dir = 0
        if ball_dir[0] > 0:
            enemy_dir = 1 if enemy_ball_dist > 0 else -1 

        enemy_dy = enemy_vel * dt
        if enemy_dy > abs(enemy_ball_dist):
            enemy_dy = abs(enemy_ball_dist)
        enemy_y += enemy_dir * enemy_dy
        enemy_y = min(max(enemy_y, 0), window_dim[1] - enemy_height) # limit y to screen

        if collide(enemy_x, enemy_y, enemy_width, enemy_height, ball_pos, ball_r):
            x = np.pi + random.uniform(-np.pi/4, np.pi/4)
            ball_dir = [np.cos(x), np.sin(x)]
            ball_pos[0] = enemy_x - ball_r

    ######################################## Draw
    game_surface.fill((33,33,33))

    score_text = f'{player_score}:{enemy_score}'
    if winner == 1: score_text = 'Player Won'
    if winner == 2: score_text = 'Computer Won'
    score = score_font.render(score_text, True, (150, 150, 150))
    score_rect = score.get_rect(center=window_center)
    game_surface.blit(score, score_rect)

    pygame.draw.rect(game_surface, (255, 255, 255), pygame.Rect(player_x, player_y, player_width, player_height))
    pygame.draw.rect(game_surface, (255, 255, 255), pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
    pygame.draw.circle(game_surface, (255, 255, 255), ball_pos, ball_r)

    window.blit(game_surface, (0, 0))
    pygame.display.flip()

    ######################################## Frame rate
    elapsed = time.perf_counter() - frame_start
    if elapsed < s_per_frame:
        time.sleep(s_per_frame - elapsed)

    frame_end = time.perf_counter() 
    frame_time = frame_end - frame_start
    frame_start = frame_end
