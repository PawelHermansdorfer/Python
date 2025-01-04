# TODO(Pawel Hermansdorfer): draw birds reversed
# TODO(Pawel Hermansdorfer): 0 index - best - with elitis whill be drawn last
# TODO(Pawel Hermansdorfer): 0 index with elitism will have red skin POG

# https://www.pygame.org/wiki/MatplotlibPygame

import pygame
import time
import os
import random
import numpy as np 

pygame.init()
random.seed(69)


######################################## Load data
fps = 60
s_per_frame = 1/fps

# window = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
window = pygame.display.set_mode((0,0))
window_dim = window.get_size()

game_scale_factor = window_dim[1]/512
game_scale = (game_scale_factor, game_scale_factor)
game_dim = (288*game_scale[0], 512*game_scale[1])
game_surface = pygame.Surface(game_dim)

debug_font = pygame.font.Font(None, 32) 

# Assets from https://github.com/samuelcust/flappy-bird-assets
dir_path = os.path.dirname(os.path.realpath(__file__))
pipe_texture   = pygame.image.load(dir_path + "\\res\\pipe-green.png")
bg_texture     = pygame.image.load(dir_path + "\\res\\background-day.png")
ground_texture = pygame.image.load(dir_path + "\\res\\base.png")
bird_textures  = [
         pygame.image.load(dir_path + "\\res\\yellowbird-upflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-downflap.png"),
         pygame.image.load(dir_path + "\\res\\yellowbird-midflap.png"),
]

texture_to_world_scale = 1/120


######################################## Init variables
frame_start = time.perf_counter()
frame_end   = 0
frame_time  = 0

def world_to_screen(pos):
    world_to_screen_scale  = (1/texture_to_world_scale * game_scale[0],
                              -1/texture_to_world_scale * game_scale[1])
    world_to_screen_offset = (game_dim[0]/2, game_dim[1]/2)
    result =  [round(pos[0] * world_to_screen_scale[0] + world_to_screen_offset[0]),
               round(pos[1] * world_to_screen_scale[1] + world_to_screen_offset[1])]
    return result

# Background
background_width  = bg_texture.get_size()[0] * texture_to_world_scale
background_height = bg_texture.get_size()[1] * texture_to_world_scale
background_half_width  = background_width/2
background_half_height = background_height/2
left_side_of_background  = -background_half_width
right_side_of_background = background_half_width
bottom_of_background = -background_half_height

# Ground
ground_width  = ground_texture.get_size()[0] * texture_to_world_scale
ground_height = ground_texture.get_size()[1] * texture_to_world_scale
ground_half_width  = ground_width/2
ground_half_height = ground_height/2
ground_x = 0
ground_y = bottom_of_background + ground_half_height - 0.5

# Bird
bird_width  = bird_textures[0].get_size()[0] * texture_to_world_scale # all bird pngs have the same size  
bird_height = bird_textures[0].get_size()[1] * texture_to_world_scale
bird_half_width  = bird_width/2
bird_half_height = bird_height/2

bird_hitbox_r = bird_half_width # circle

BIRD_COUNT = 50
birds_y = [0 for _ in range(BIRD_COUNT)]
birds_x = -0.7
bird_vel = [0 for _ in range(BIRD_COUNT)]
bird_jump_vel = 2.4
g = -9.1

alive = [True for _ in range(BIRD_COUNT)]
alive_count = BIRD_COUNT
def die(idx):
    global alive_count
    alive[idx] = False
    alive_count -= 1

fitness = np.array([0 for _ in range(BIRD_COUNT)])
mutation_propability = 0.5
crossover_propability = 0.5

input_count = 4
hidden_neuron_count = 5
input_values  = [np.array([0, 0, 0, 0]) for _ in range(BIRD_COUNT)]
hidden_weights = [np.random.normal(size=(input_count, hidden_neuron_count)) for _ in range(BIRD_COUNT)]
hidden_biases  = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
hidden_values = [np.array([0 for _ in range(hidden_neuron_count)]) for __ in range(BIRD_COUNT)]
output_weights = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
output_value = [0 for _ in range(BIRD_COUNT)]

# Genetic algorithm params
elitism = True

# Pipes
pipe_width  = pipe_texture.get_size()[0] * texture_to_world_scale
pipe_height = pipe_texture.get_size()[1] * texture_to_world_scale
pipe_half_width  = pipe_width/2
pipe_half_height = pipe_height/2
gap_between_pipes = 3.5

def get_new_pipe_y():
    return gap_between_pipes/2 + (random.random() - 0.3) * 1.5 

pipe_count = 2
pipes_vel = -0.5
pipes_dx = background_half_width + pipe_half_width
pipes_spawn_x = right_side_of_background + pipe_half_width
first_pipe_x = pipes_spawn_x
pipes_y = [get_new_pipe_y(), get_new_pipe_y()]

######################################## Game loop
stoped = False
while not stoped:
    window_dim = window.get_size()

    ######################################## input_values
    space_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True
        elif event.type == pygame.VIDEORESIZE:
            window_dim = window.get_size()
            world_to_screen_offset = [window_dim[0]/2, window_dim[1]/2]

            game_scale_factor = window_dim[1]/512
            game_scale = (game_scale_factor, game_scale_factor)
            game_dim = (288*game_scale[0], 512*game_scale[1])
            game_surface = pygame.Surface(game_dim)
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q:
                    stoped = True
                case pygame.K_SPACE:
                    space_pressed = True


    ######################################## Update
    if frame_time != 0:
        dt = frame_time

        for bird_idx in range(BIRD_COUNT):
            if alive[bird_idx]:
                fitness[bird_idx] += 1

                left_side_of_first_pipe   = first_pipe_x - pipe_half_width
                right_side_of_first_pipe  = first_pipe_x + pipe_half_width
                bottom_of_top_first_pipe  = pipes_y[0] - pipe_half_height
                top_of_bottom_first_pipe  = pipes_y[0] - gap_between_pipes + pipe_half_height
                left_side_of_second_pipe   = first_pipe_x + pipes_dx - pipe_half_width
                right_side_of_second_pipe  = first_pipe_x + pipes_dx + pipe_half_width
                bottom_of_top_second_pipe  = pipes_y[1] - pipe_half_height
                top_of_bottom_second_pipe  = pipes_y[1] - gap_between_pipes + pipe_half_height

                left_side_of_next_pipe   = 0
                right_side_of_next_pipe  = 0
                bottom_of_top_next_pipe  = 0
                top_of_bottom_next_pipe  = 0
                if right_side_of_first_pipe >= birds_x - bird_hitbox_r:
                    left_side_of_next_pipe   = left_side_of_first_pipe
                    right_side_of_next_pipe  = right_side_of_first_pipe
                    bottom_of_top_next_pipe  = bottom_of_top_first_pipe
                    top_of_bottom_next_pipe  = top_of_bottom_first_pipe
                else:
                    left_side_of_next_pipe   = left_side_of_second_pipe
                    right_side_of_next_pipe  = right_side_of_second_pipe
                    bottom_of_top_next_pipe  = bottom_of_top_second_pipe
                    top_of_bottom_next_pipe  = top_of_bottom_second_pipe


                dist_to_next_pipe = 0 # left_side_of_next_pipe - birds_x
                y_difference_to_next_pipe = top_of_bottom_next_pipe - birds_y[bird_idx]

                input_values[bird_idx]  = np.array([birds_y[bird_idx], bird_vel[bird_idx],
                                                    dist_to_next_pipe, y_difference_to_next_pipe])
                hidden_values[bird_idx] = np.tanh(input_values[bird_idx] @  hidden_weights[bird_idx] + hidden_biases[bird_idx])
                output_value[bird_idx]  = np.tanh(hidden_values[bird_idx] @ output_weights[bird_idx])
                output_activated = output_value[bird_idx] >= 0


                if (left_side_of_next_pipe <= birds_x + bird_hitbox_r 
                    and right_side_of_next_pipe >= birds_x - bird_hitbox_r):
                        if (birds_y[bird_idx] + bird_hitbox_r >= bottom_of_top_next_pipe
                            or birds_y[bird_idx] - bird_hitbox_r <= top_of_bottom_next_pipe):
                            die(bird_idx) # make death

                # Handle bird-ground collision
                if birds_y[bird_idx] - bird_hitbox_r <= ground_y + ground_half_height:
                    die(bird_idx) # make death

                # Bird
                bird_vel[bird_idx] += g * dt
                if output_activated:
                    bird_vel[bird_idx] = bird_jump_vel

                birds_y[bird_idx] += bird_vel[bird_idx] * dt

        # Pipes
        if first_pipe_x + pipe_half_width < left_side_of_background:
            first_pipe_x = first_pipe_x + pipes_dx
            pipes_y[0] = pipes_y[1]
            pipes_y[1] = get_new_pipe_y()

        first_pipe_x += pipes_vel * dt

        # Ground
        if ground_x + ground_half_width < left_side_of_background:
            ground_x += ground_width

        ground_x += pipes_vel * dt # ground has same speed as pipes

    # Check for new generation
    if alive_count == 0:
        ground_x = 0

        first_pipe_x = pipes_spawn_x
        pipes_y = [get_new_pipe_y(), get_new_pipe_y()]

        birds_y = [0 for _ in range(BIRD_COUNT)]
        bird_vel = [0 for _ in range(BIRD_COUNT)]
        alive = [True for _ in range(BIRD_COUNT)]
        alive_count = BIRD_COUNT

        # Tournament selection
        probabilities = fitness / fitness.sum()
        indexes = np.arange(0, BIRD_COUNT)

        insert_to_next_gen_idx = 0
        if elitism:
            best_one = np.argmax(fitness)
            input_values[insert_to_next_gen_idx]   = input_values[best_one]
            hidden_weights[insert_to_next_gen_idx] = hidden_weights[best_one]
            hidden_biases[insert_to_next_gen_idx]  = hidden_biases[best_one]
            hidden_values[insert_to_next_gen_idx]  = hidden_values[best_one]
            output_weights[insert_to_next_gen_idx] = output_weights[best_one]
            output_value[insert_to_next_gen_idx]   = output_value[best_one]
            insert_to_next_gen_idx += 1

        while insert_to_next_gen_idx < BIRD_COUNT:
            rnd = np.random.rand()
            do_mutation  = rnd <= mutation_propability 
            do_crossover = rnd <= crossover_propability

            if do_mutation:
                parent_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                child_idx = insert_to_next_gen_idx
                insert_to_next_gen_idx += 1

                input_valuespchild_idx    = np.array([0, 0, 0, 0])
                hidden_weights[child_idx] = hidden_weights[parent_idx] * np.random.normal(1.0, 0.1, hidden_neuron_count)
                hidden_biases[child_idx]  = hidden_biases[parent_idx] * np.random.normal(1.0, 0.1, hidden_neuron_count)
                hidden_values[child_idx]  = np.array([0 for _ in range(hidden_neuron_count)])
                output_weights[child_idx] = output_weights[parent_idx] * np.random.normal(1.0, 0.1, hidden_neuron_count)
                output_value[child_idx]   = 0

                fitness[child_idx] = 0

            # Crossovers
            if do_crossover and insert_to_next_gen_idx < BIRD_COUNT:
                parent_a_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                parent_b_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                child_idx = insert_to_next_gen_idx
                insert_to_next_gen_idx += 1

                input_valuespchild_idx    = np.array([0, 0, 0, 0])
                hidden_weights[child_idx] = (hidden_weights[parent_a_idx] + hidden_weights[parent_b_idx]) / 2
                hidden_biases[child_idx]  = (hidden_biases[parent_a_idx] + hidden_biases[parent_b_idx]) / 2
                hidden_values[child_idx]  = np.array([0 for _ in range(hidden_neuron_count)])
                output_weights[child_idx] = (output_weights[parent_a_idx] + output_weights[parent_b_idx]) / 2
                output_value[child_idx]   = 0

                fitness[child_idx] = 0


        # fitness = np.array([0 for _ in range(BIRD_COUNT)])

        # input_values  = [np.array([0, 0, 0, 0]) for _ in range(BIRD_COUNT)]
        # hidden_weights = [np.random.normal(size=(input_count, hidden_neuron_count)) for _ in range(BIRD_COUNT)]
        # hidden_biases  = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
        # hidden_values = [np.array([0 for _ in range(hidden_neuron_count)]) for __ in range(BIRD_COUNT)]
        # output_weights = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
        # output_value = [0 for _ in range(BIRD_COUNT)]


    ######################################## Draw
    window.fill((33,33,33))
    game_surface.fill((33,33,33))

    def blit(texture, pos, angle=0):
        texture_dim = texture.get_size()
        texture = pygame.transform.scale(texture, (texture_dim[0]*game_scale[0],
                                                   texture_dim[1]*game_scale[1]))
        texture = pygame.transform.rotate(texture, angle)
        rect = texture.get_rect(center=world_to_screen(pos))
        game_surface.blit(texture, rect)

    # background
    blit(bg_texture, (0, 0), 0)

    # Pipes
    blit(pipe_texture, (first_pipe_x, pipes_y[0]), 180)
    blit(pipe_texture, (first_pipe_x, pipes_y[0] - gap_between_pipes), 0)

    blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1]), 180)
    blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1] - gap_between_pipes), 0)

    # Ground
    blit(ground_texture, (ground_x, ground_y))
    blit(ground_texture, (ground_x + 2*ground_half_width - 0.005, ground_y)) # hacky -0.005 to be sure there's no pixel gap between ground tiles

    # Bird
    for bird_idx in range(BIRD_COUNT):
        if alive[bird_idx]:
            bird_texture_idx = int(frame_start*7 % len(bird_textures))
            bird_texture = bird_textures[bird_texture_idx]
            bird_angle = max(min(bird_vel[bird_idx]*3.4 + 8, 4), -4) * 8
            blit(bird_texture, [birds_x, birds_y[bird_idx]], bird_angle)

    # Game surface
    window.blit(game_surface, (0, 0))

    # Neural network
    input_nodes_positions  = []
    hidden_nodes_positions = []
    output_nodes_positions = []

    best_bird_idx = np.argmax(fitness)
    input_node_count = input_values[best_bird_idx].shape[0]
    input_nodes_x = ((window_dim[0] - game_dim[0]) / 4) + game_dim[0]
    input_node_r = 20
    space_between_input_nodes = 60
    y = game_dim[1]/2 - (input_node_count - 1)*(2*input_node_r + space_between_input_nodes)*0.5
    for i in range(input_node_count):
        input_nodes_positions.append((input_nodes_x, y))
        y += 2*input_node_r + space_between_input_nodes

    hidden_noe_x = ((window_dim[0] - game_dim[0]) / 2) + game_dim[0]
    space_between_hidden_nodes = 60
    hidden_node_r = 20
    y = game_dim[1]/2 - (hidden_neuron_count - 1)*(2*hidden_node_r + space_between_hidden_nodes)*0.5
    for i in range(hidden_neuron_count):
        hidden_nodes_positions.append((hidden_noe_x, y))
        y += 2*hidden_node_r + space_between_hidden_nodes

    output_x = (3*(window_dim[0] - game_dim[0])/4) + game_dim[0]
    output_y = game_dim[1]/2
    output_node_pos = (output_x, output_y)
    output_r = 20

    def get_node_or_weight_color(v):
        r = min(max(v, -1), 0) * -255
        g = min(max(v, 0), 1) * 255
        return (r, g, 0)

    for i, input_node_pos in enumerate(input_nodes_positions):
        for j, hidden_node_pos in enumerate(hidden_nodes_positions):
            weight_color = get_node_or_weight_color(hidden_weights[best_bird_idx][i, j])
            weight_width = int(np.ceil(np.abs(hidden_weights[best_bird_idx][i, j]) * 1.5 + 1))
            pygame.draw.line(window, weight_color, input_node_pos, hidden_node_pos, width=weight_width)
        input_color = get_node_or_weight_color(input_values[best_bird_idx][i])
        pygame.draw.circle(window, input_color, input_node_pos, radius=hidden_node_r)
        # input_value_text = debug_font.render(f'{}', True, (255,255,255)
        # window.blit(), (0, y))

    for i, hidden_node_pos in enumerate(hidden_nodes_positions):
        weight_color = get_node_or_weight_color(output_weights[best_bird_idx][i])
        weight_width = int(np.ceil(np.abs(output_weights[best_bird_idx][i]) * 1.5 + 1))
        pygame.draw.line(window, weight_color, hidden_node_pos, output_node_pos, width=weight_width)
        hidden_color = get_node_or_weight_color(hidden_values[best_bird_idx][i])
        pygame.draw.circle(window, hidden_color, hidden_node_pos, radius=hidden_node_r)

    output_color = get_node_or_weight_color(output_value[best_bird_idx])
    pygame.draw.circle(window, output_color, output_node_pos, radius=hidden_node_r)

    # Telemetry 
    telemetry = [
            f'Frame time:  {frame_time*1000:.1f}ms',
            f'FPS: {(1/frame_time) if frame_time != 0 else 0:.0f}',
            f'Alive: {alive_count}',
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
