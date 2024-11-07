# Assets from https://github.com/samuelcust/flappy-bird-assets

import pygame
import time
import os

pygame.init()

fps = 60
s_per_frame = 1/fps
game_scale = [1.5, 1.5]
window_dim = [288*game_scale[0], 512*game_scale[1]]
window = pygame.display.set_mode(window_dim, pygame.RESIZABLE)

debug_font = pygame.font.Font(None, 32) 

dir_path = os.path.dirname(os.path.realpath(__file__))
pipe_texture  = pygame.image.load(dir_path + "\\res\\pipe.png")
bg_texture    = pygame.image.load(dir_path + "\\res\\bg.png")
bird_textures = [
         pygame.image.load(dir_path + "\\res\\yellowbird-upflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-downflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
]

pipe_texture_dim = pipe_texture.get_size()
pipe_texture = pygame.transform.scale(pipe_texture, (pipe_texture_dim[0] * game_scale[0],
                                                     pipe_texture_dim[1] * game_scale[1]))

bg_texture_dim = bg_texture.get_size()
bg_texture = pygame.transform.scale(bg_texture, (bg_texture_dim[0] * game_scale[0],
                                                 bg_texture_dim[1] * game_scale[1]))

for i in range(len(bird_textures)):
    bird_texture_dim = bird_textures[i].get_size()
    bird_textures[i] = pygame.transform.scale(bird_textures[i], (bird_texture_dim[0] * game_scale[0],
                                                                 bird_texture_dim[1] * game_scale[1]))

def animate_bird(frame_start) -> int: # idx in texture arrays
    return int(frame_start*3 % len(bird_textures))


########################################
frame_start = time.perf_counter()
frame_end   = 0
frame_time  = 1

bird_pos = [-0.7, 0]
bird_vel = 0
g = 15

world_to_screen_scale  = (120 * game_scale[0], -120 * game_scale[1])
def world_to_screen(pos):
    result =  [round(pos[0] * world_to_screen_scale[0] + window_dim[0]/2),
               round(pos[1] * world_to_screen_scale[1] + window_dim[1]/2)]
    return result

########################################
started = False
stoped = False
while not stoped:
    # Inputs
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

    ########################################
    # Update
    dt = frame_time

    if started:
        bird_vel += -g * dt
        if space_pressed:
            bird_vel = 4
        bird_pos[1] += bird_vel * dt


    ########################################
    # Draw
    window.fill((39, 43, 48))

    def blit(texture, pos, angle=0):
        texture = pygame.transform.rotate(texture, angle)
        rect = texture.get_rect(center=world_to_screen(pos))
        window.blit(texture, rect)

    blit(bg_texture, (0, 0), 0)

    bird_texture = bird_textures[animate_bird(frame_start)]
    bird_angle = max(min(bird_vel, 4), -4) * 8
    blit(bird_texture, bird_pos, bird_angle)

    window.blit(debug_font.render(f'Frame time:  {frame_time*1000:.1f}ms | {1/frame_time:.0f}FPS', True, (255,255,255)), (0, 0))
    window.blit(debug_font.render(f'pos: ({bird_pos[0]:.1f}, {bird_pos[1]:.1f})', True, (255,255,255)), (0, 30))
    window.blit(debug_font.render(f'vel: {bird_vel:.1f}',                         True, (255,255,255)), (0, 60))

    pygame.display.flip()

    ########################################
    # Frame rate
    elapsed = time.perf_counter() - frame_start
    if elapsed < s_per_frame:
        time.sleep(s_per_frame - elapsed)

    frame_end = time.perf_counter() 
    frame_time = frame_end - frame_start
    frame_start = frame_end
