
import pygame
import time
import os
import random

pygame.init()
random.seed(69)


######################################## Load data
fps = 60
s_per_frame = 1/fps
game_scale = [1.5, 1.5]
window_dim = [288*game_scale[0], 512*game_scale[1]]
window = pygame.display.set_mode(window_dim, pygame.RESIZABLE)

debug_font = pygame.font.Font(None, 32) 

# Assets from https://github.com/samuelcust/flappy-bird-assets
dir_path = os.path.dirname(os.path.realpath(__file__))
pipe_texture  = pygame.image.load(dir_path + "\\res\\pipe-green.png")
bg_texture    = pygame.image.load(dir_path + "\\res\\background-day.png")
bird_textures = [
         pygame.image.load(dir_path + "\\res\\yellowbird-upflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-downflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
]

texture_to_world_scale = 120


######################################## Init variables
frame_start = time.perf_counter()
frame_end   = 0
frame_time  = 0

def world_to_screen(pos):
    world_to_screen_scale  = (texture_to_world_scale * game_scale[0],
                              -texture_to_world_scale * game_scale[1])
    result =  [round(pos[0] * world_to_screen_scale[0] + window_dim[0]/2),
               round(pos[1] * world_to_screen_scale[1] + window_dim[1]/2)]
    return result

# Background
background_width  = bg_texture.get_size()[0] / texture_to_world_scale
background_height = bg_texture.get_size()[1] / texture_to_world_scale
left_side_of_background  = -background_width/2
right_side_of_background = background_width/2

# Bird
bird_pos = [-0.7, 0]
bird_vel = 0
bird_jump_vel = 2.4
g = -9.1

# Pipes
pipe_width  = pipe_texture.get_size()[0] / texture_to_world_scale
pipe_height = pipe_texture.get_size()[1] / texture_to_world_scale
gap_between_pipes = 3.5

def get_pipes_y():
    return gap_between_pipes/2 + (random.random() - 0.5) * 2 

pipe_count = 2
pipes_vel = -0.5
pipes_dx = background_width/2 + pipe_width/2
pipes_spawn_x = right_side_of_background + pipe_width/2
first_pipe_x = pipes_spawn_x
pipes_y = [get_pipes_y(), get_pipes_y()]

# bottom_of_top_pipe  = pipes_y - pipe_height/2
# top_of_bottom_pipe  = pipes_y - gap_between_pipes + pipe_height/2
# left_side_of_pipes  = pipes_x + pipe_width/2
# right_side_of_pipes = pipes_x - pipe_width/2


######################################## Game loop
started = False
stoped = False
while not stoped:
    ######################################## Inputs
    space_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True
        elif event.type == pygame.VIDEORESIZE:
            window_dim = window.get_size()
            world_to_screen_offset = [window_dim[0]/2, window_dim[1]/2]
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q:
                    stoped = True
                case pygame.K_SPACE:
                    space_pressed = True
                    if not started: started = True


    ######################################## Update
    if frame_time != 0:
        dt = frame_time

        # Bird
        bird_vel += g * dt
        if space_pressed:
            bird_vel = bird_jump_vel

        if not started and bird_pos[1] < -0:
            bird_vel = bird_jump_vel
            bird_pos[1] = 0

        bird_pos[1] += bird_vel * dt

        # Pipe
        if first_pipe_x + pipe_width/2 < left_side_of_background:
            first_pipe_x = first_pipe_x + pipes_dx
            pipes_y[0] = pipes_y[1]
            pipes_y[1] = get_pipes_y()

        first_pipe_x += pipes_vel * dt


    ######################################## Draw
    window.fill((39, 43, 48))

    def blit(texture, pos, angle=0):
        texture_dim = texture.get_size()
        texture = pygame.transform.scale(texture, (texture_dim[0]*game_scale[0],
                                                   texture_dim[1]*game_scale[1]))
        texture = pygame.transform.rotate(texture, angle)
        rect = texture.get_rect(center=world_to_screen(pos))
        window.blit(texture, rect)

    # background
    blit(bg_texture, (0, 0), 0)

    # Pipes
    blit(pipe_texture, (first_pipe_x, pipes_y[0]), 180)
    blit(pipe_texture, (first_pipe_x, pipes_y[0] - gap_between_pipes), 0)

    blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1]), 180)
    blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1] - gap_between_pipes), 0)


    # bird
    bird_texture_idx = int(frame_start*7 % len(bird_textures))
    bird_texture = bird_textures[bird_texture_idx]
    bird_angle = max(min(bird_vel*3 + 8, 4), -4) * 8
    blit(bird_texture, bird_pos, bird_angle)

    # Telemetry 
    telemetry = [
            f'Frame time:  {frame_time*1000:.1f}ms | {(1/frame_time) if frame_time != 0 else 0:.0f}FPS',
            f'pos: ({bird_pos[0]:.1f}, {bird_pos[1]:.1f})',
            f'vel: {bird_vel:.1f}',
    ]
    y = 0
    for line in telemetry:
        window.blit(debug_font.render(line, True, (255,255,255)), (0, y))
        y += 30

    pygame.display.flip()


    ######################################## Frame rate
    elapsed = time.perf_counter() - frame_start
    if elapsed < s_per_frame:
        time.sleep(s_per_frame - elapsed)

    frame_end = time.perf_counter() 
    frame_time = frame_end - frame_start
    frame_start = frame_end
