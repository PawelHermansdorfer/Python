# TODO(Pawel Hermansdorfer): Wieghts * <0.95, 1.05> if wieght is 0 then it won't change
# TODO(Pawel Hermansdorfer): Fitness boost for passing pipe
# TODO(Pawel Hermansdorfer): Draw score(passed pipes)

# TODO(Pawel Hermansdorfer): mutacje gauss + semgo gaussa (metaeolucja)
import time
import os

import numpy as np 

import pygame
pygame.init()

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.pygame import PygameRenderer

GAME_STARTED = False

########################################
# Setup params
all_possible_inputs = [
        'None',

        'Bird\'s position on Y axis',
        'Bird\'s position on X axis',
        'Bird\'s velocity on Y axis',

        'Next pipe\'s position on X axis',
        'Next gaps\'s position on Y axis',

        'Bird\'s distance to next pipe',
        'Difference between bird and next gap on Y axis',
]
selected_inputs = [['', 0] for _ in all_possible_inputs]
selected_inputs[0] = [all_possible_inputs[1], 1]
selected_inputs[1] = [all_possible_inputs[4], 4]

nn_inputs_order = []
nn_inputs_order_text = []

input_count = 2
hidden_neuron_count = 3

normalize_inputs = False

BIRD_COUNT = 50

mutation_propability = 0.5
mutation_magnitude = 0.5
crossover_propability = 0.5

elitism = True

use_reward_point_for_time_survived = True
reward_points_for_time_survived    = 1

use_reward_points_for_passing_pipe = True
reward_points_for_passing_pipe    = 1000

use_punish_points_hitting_ground = True
punish_points_hitting_ground      = -1000

use_punish_points_flying_above_screen = True
punish_points_flying_above_screen = -1

# Settings
game_speed_factor = 1
draw_hitboxes = False
hitboxes_width = 2
display_fps = False
max_fps = 30
max_fps_options = [30, 60, 120, 144, 164]
max_fps_option_idx = 0

# UI error messages 
failed_no_inputs = False
failed_zero_probabilities = False

######################################## Load data
window = pygame.display.set_mode((0,0), pygame.DOUBLEBUF | pygame.OPENGL)
window_dim = window.get_size()
window_surface = pygame.Surface(window_dim) 

game_scale_factor = window_dim[1]/512
game_scale = (game_scale_factor, game_scale_factor)
game_dim = (288*game_scale[0], 512*game_scale[1])
game_surface = pygame.Surface(game_dim)

# Imgui init
imgui.create_context()
impl = PygameRenderer()
io = imgui.get_io()
io.display_size = window_dim
imgui.set_next_window_size(500, 300)

# Font
debug_font = pygame.font.Font(None, 32) 
nn_inputs_font = pygame.font.Font(None, 18) 
nn_nodes_font = pygame.font.Font(None, 18) 

# Assets from https://github.com/samuelcust/flappy-bird-assets
texture_to_world_scale = 1/120

dir_path = os.path.dirname(os.path.realpath(__file__))
pipe_texture   = pygame.image.load(dir_path + "/res/pipe-green.png")
bg_texture     = pygame.image.load(dir_path + "/res/background-day.png")
ground_texture = pygame.image.load(dir_path + "/res/base.png")

yellow_bird_textures  = [
         pygame.image.load(dir_path + "/res/yellowbird-upflap.png"),
         pygame.image.load(dir_path + "/res/yellowbird-midflap.png"),
         pygame.image.load(dir_path + "/res/yellowbird-downflap.png"),
         pygame.image.load(dir_path + "/res/yellowbird-midflap.png"),
]
blue_bird_textures = [
         pygame.image.load(dir_path + "/res/bluebird-upflap.png"),
         pygame.image.load(dir_path + "/res/bluebird-midflap.png"),
         pygame.image.load(dir_path + "/res/bluebird-downflap.png"),
         pygame.image.load(dir_path + "/res/bluebird-midflap.png"),
]
red_bird_textures = [
         pygame.image.load(dir_path + "/res/redbird-upflap.png"),
         pygame.image.load(dir_path + "/res/redbird-midflap.png"),
         pygame.image.load(dir_path + "/res/redbird-downflap.png"),
         pygame.image.load(dir_path + "/res/redbird-midflap.png"),
]
bird_textures = [yellow_bird_textures, blue_bird_textures, red_bird_textures]
bird_color_yellow = 0
bird_color_blue = 1
bird_color_red = 2
# NOTE(Pawel Hermansdorfer): 1st gen random, later -> RED - elitism | BLUE - crossover | yellow - mutation

score_numbers_textures = [pygame.image.load(dir_path + f"/res/{i}.png") for i in range(10)]
score_numbers_widths = score_numbers_textures[0].get_size()[0] * texture_to_world_scale
score_numbers_heights = 36


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

passed_pipe = False
score = 0

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
bird_width  = bird_textures[0][0].get_size()[0] * texture_to_world_scale # all bird pngs have the same size  
bird_height = bird_textures[0][0].get_size()[1] * texture_to_world_scale
bird_half_width  = bird_width/2
bird_half_height = bird_height/2

bird_hitbox_r = bird_half_width # circle

birds_y = []
birds_x = -0.7
bird_vel = []
bird_jump_vel = 2.4
g = -9.1

birds_colors = []

alive = []
alive_count = []
def die(idx):
    global alive_count
    if alive[bird_idx]:
        alive[idx] = False
        alive_count -= 1

fitness = []

current_generation_idx = 0
best_fitness_this_generation = 0
best_fitness_overall = 0

input_values   = []
hidden_weights = []
hidden_biases  = []
hidden_values  = []
output_weights = []
output_value   = []

# Pipes
pipe_width  = pipe_texture.get_size()[0] * texture_to_world_scale
pipe_height = pipe_texture.get_size()[1] * texture_to_world_scale
pipe_half_width  = pipe_width/2
pipe_half_height = pipe_height/2
gap_between_pipes = 3.5

def get_new_pipe_y():
    return gap_between_pipes/2 + (np.random.random() - 0.3) * 1.5 

pipe_count = 2
pipes_vel = -0.5
pipes_dx = background_half_width + pipe_half_width
pipes_spawn_x = right_side_of_background + pipe_half_width
first_pipe_x = pipes_spawn_x
pipes_y = [get_new_pipe_y(), get_new_pipe_y()]

def blit(texture, pos, angle=0):
    texture_dim = texture.get_size()
    texture = pygame.transform.scale(texture, (texture_dim[0]*game_scale[0],
                                               texture_dim[1]*game_scale[1]))
    if angle != 0:
        texture = pygame.transform.rotate(texture, angle)
    rect = texture.get_rect(center=world_to_screen(pos))
    game_surface.blit(texture, rect)

def draw_rect_hitbox(center, w, h):
    w = w * (1/texture_to_world_scale * game_scale[0])
    h = h * (1/texture_to_world_scale * game_scale[0])
    center = world_to_screen(center)
    rect = pygame.Rect(center[0] - w//2, center[1]-h//2, w, h)
    pygame.draw.rect(game_surface, (255, 0, 0), rect, hitboxes_width)

def get_node_or_weight_color(v):
    r = min(max(v, -1), 0) * -255
    g = min(max(v, 0), 1) * 255
    return (r, g, 0)

def limit(x, a, b):
    return min(max(x, a), b)

######################################## Game loop
stoped = False
while not stoped:
    window_dim = window.get_size()

    ######################################## input_values
    space_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stoped = True
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q:
                    stoped = True
                case pygame.K_SPACE:
                    if GAME_STARTED:
                        if game_speed_factor == 0:
                            game_speed_factor = 1
                        else:
                            game_speed_factor = 0

        impl.process_event(event)

    ######################################## Update
    if frame_time != 0 and GAME_STARTED:
        dt = frame_time

        for _ in range(game_speed_factor):
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
                left_side_of_next_pipe  = left_side_of_first_pipe
                right_side_of_next_pipe = right_side_of_first_pipe
                bottom_of_top_next_pipe = bottom_of_top_first_pipe
                top_of_bottom_next_pipe = top_of_bottom_first_pipe
            else:
                left_side_of_next_pipe  = left_side_of_second_pipe
                right_side_of_next_pipe = right_side_of_second_pipe
                bottom_of_top_next_pipe = bottom_of_top_second_pipe
                top_of_bottom_next_pipe = top_of_bottom_second_pipe

            # pipe_score_point =(left_side_of_next_pipe + right_side_of_next_pipe) / 2
            pipe_score_point = right_side_of_next_pipe
            if not passed_pipe and pipe_score_point < birds_x:
                passed_pipe = True
                score += 1
                if use_reward_points_for_passing_pipe:
                    for bird_idx in range(BIRD_COUNT):
                        fitness[bird_idx] += reward_points_for_passing_pipe
            if passed_pipe and pipe_score_point > birds_x:
                passed_pipe = False

            for bird_idx in range(BIRD_COUNT):
                if alive[bird_idx]:

                    if use_punish_points_flying_above_screen:
                        if birds_y[bird_idx] >= background_half_height:
                            fitness[bird_idx] += punish_points_flying_above_screen

                    if use_reward_point_for_time_survived:
                        fitness[bird_idx] += reward_points_for_time_survived

                    if best_fitness_this_generation < fitness[bird_idx]:
                        best_fitness_this_generation = fitness[bird_idx]

                    inputs = [0 for _ in range(input_count)]
                    for input_idx in range(len(inputs)):
                        value = 0
                        match nn_inputs_order[input_idx]:
                            case 'Bird\'s position on Y axis':
                                value = birds_y[bird_idx]
                                if normalize_inputs: value = limit(value + background_half_height, 0, background_height) / background_height

                            case 'Bird\'s position on X axis':
                                value = birds_x
                                if normalize_inputs: value = limit(value + background_half_width, 0, background_width) / background_width

                            case 'Bird\'s velocity on Y axis':
                                value = bird_vel[bird_idx]
                                if normalize_inputs: value = limit(value + background_half_height, 0, background_height) / background_height

                            case 'Next pipe\'s position on X axis':
                                value = left_side_of_next_pipe
                                if normalize_inputs: value = limit(value + background_half_width, 0, background_width) / background_width

                            case 'Next gaps\'s position on Y axis':
                                value = top_of_bottom_next_pipe
                                if normalize_inputs: value = limit(value + background_half_height, 0, background_height) / background_height

                            case 'Bird\'s distance to next pipe':
                                value = birds_x -left_side_of_next_pipe
                                if normalize_inputs: value = limit(value + background_half_width, 0, background_width) / background_width

                            case 'Difference between bird and next gap on Y axis':
                                value = birds_y[bird_idx] - top_of_bottom_next_pipe
                                if normalize_inputs: value = limit(value + background_half_height, 0, background_height) / background_height

                        inputs[input_idx] = value

                    input_values[bird_idx]  = np.array(inputs)
                    hidden_values[bird_idx] = np.tanh(input_values[bird_idx] @  hidden_weights[bird_idx] + hidden_biases[bird_idx])
                    output_value[bird_idx]  = np.tanh(hidden_values[bird_idx] @ output_weights[bird_idx])
                    output_activated = output_value[bird_idx] >= 0

                    # Pipe collision
                    if (left_side_of_next_pipe <= birds_x + bird_hitbox_r 
                        and right_side_of_next_pipe >= birds_x - bird_hitbox_r):
                            if (birds_y[bird_idx] + bird_hitbox_r >= bottom_of_top_next_pipe
                                or birds_y[bird_idx] - bird_hitbox_r <= top_of_bottom_next_pipe):
                                die(bird_idx)

                    # Handle bird-ground collision
                    if birds_y[bird_idx] - bird_hitbox_r <= ground_y + ground_half_height:
                        die(bird_idx) # make death
                        if use_punish_points_hitting_ground:
                            fitness[bird_idx] += punish_points_hitting_ground

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
            # Tournament selection???
            fitness_sum = 0
            for i in range(len(fitness)):
                fitness[i] = max(fitness[i], 0)
                fitness_sum += fitness[i]
            if fitness_sum == 0: 
                for i in range(len(fitness)):
                    fitness[i] = 1

            probabilities = fitness / fitness.sum()
            probabilities = np.nan_to_num(probabilities, nan=0)
            indexes = np.arange(0, BIRD_COUNT)

            insert_to_next_gen_idx = 0
            if elitism:
                best_one = np.argmax(fitness)
                hidden_weights[insert_to_next_gen_idx] = hidden_weights[best_one]
                hidden_biases[insert_to_next_gen_idx]  = hidden_biases[best_one]
                output_weights[insert_to_next_gen_idx] = output_weights[best_one]
                birds_colors[insert_to_next_gen_idx] = bird_color_red
                insert_to_next_gen_idx += 1

            while insert_to_next_gen_idx < BIRD_COUNT:
                rnd = np.random.rand()
                do_mutation  = rnd <= mutation_propability 
                do_crossover = rnd <= crossover_propability

                # mutation
                if do_mutation:
                    parent_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                    child_idx = insert_to_next_gen_idx
                    insert_to_next_gen_idx += 1

                    hidden_weights[child_idx] = hidden_weights[parent_idx] * np.random.normal(1.0, mutation_magnitude, hidden_neuron_count)
                    hidden_biases[child_idx]  = hidden_biases[parent_idx] * np.random.normal(1.0, mutation_magnitude, hidden_neuron_count)
                    output_weights[child_idx] = output_weights[parent_idx] * np.random.normal(1.0, mutation_magnitude, hidden_neuron_count)

                    birds_colors[child_idx] = bird_color_blue

                # Crossovers
                if do_crossover and insert_to_next_gen_idx < BIRD_COUNT:
                    parent_a_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                    parent_b_idx = np.random.choice(indexes, 1, p=probabilities)[0]
                    child_idx = insert_to_next_gen_idx
                    insert_to_next_gen_idx += 1

                    hidden_weights[child_idx] = (hidden_weights[parent_a_idx] + hidden_weights[parent_b_idx]) / 2
                    hidden_biases[child_idx]  = (hidden_biases[parent_a_idx] + hidden_biases[parent_b_idx]) / 2
                    output_weights[child_idx] = (output_weights[parent_a_idx] + output_weights[parent_b_idx]) / 2

                    birds_colors[child_idx] = bird_color_yellow

            current_generation_idx += 1
            if best_fitness_overall < best_fitness_this_generation:
                best_fitness_overall = best_fitness_this_generation
            best_fitness_this_generation = 0

            # Setup scene for next gen
            ground_x = 0

            first_pipe_x = pipes_spawn_x
            pipes_y = [get_new_pipe_y(), get_new_pipe_y()]

            for bird_idx in range(BIRD_COUNT):
                birds_y[bird_idx]  = 0
                bird_vel[bird_idx] = 0
                alive[bird_idx]    = True
                fitness[bird_idx]  = 0

            alive_count = BIRD_COUNT
            score = 0

    ######################################## Draw
    window_surface.fill((33,33,33))

    if GAME_STARTED:
        game_surface.fill((33,33,33))

        # background
        blit(bg_texture, (0, 0), 0)

        # Pipes
        blit(pipe_texture, (first_pipe_x, pipes_y[0]), 180)
        blit(pipe_texture, (first_pipe_x, pipes_y[0] - gap_between_pipes), 0)
        if draw_hitboxes:
            draw_rect_hitbox((first_pipe_x, pipes_y[0]), pipe_width, pipe_height)
            draw_rect_hitbox((first_pipe_x, pipes_y[0] - gap_between_pipes), pipe_width, pipe_height)

        blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1]), 180)
        blit(pipe_texture, (first_pipe_x + pipes_dx, pipes_y[1] - gap_between_pipes), 0)

        if draw_hitboxes:
            draw_rect_hitbox((first_pipe_x + pipes_dx, pipes_y[1]), pipe_width, pipe_height)
            draw_rect_hitbox((first_pipe_x + pipes_dx, pipes_y[1] - gap_between_pipes), pipe_width, pipe_height)

        # Ground
        blit(ground_texture, (ground_x, ground_y))
        blit(ground_texture, (ground_x + 2*ground_half_width - 0.005, ground_y)) # cheesy -0.005 to be sure there's no pixel gap between ground tiles

        if draw_hitboxes:
            draw_rect_hitbox((ground_x, ground_y), ground_width, ground_height)
            draw_rect_hitbox((ground_x + 2*ground_half_width - 0.005, ground_y), ground_width, ground_height)

        # Bird
        # NOTE(Pawel Hermansdorfer): Draw reversed so that idx 0 - best from prev gen with elitism (red bird) is drawn at the top
        for bird_idx in range(BIRD_COUNT-1, 0-1, -1):
            if alive[bird_idx]:
                bird_color = birds_colors[bird_idx]
                bird_texture_idx = int(frame_start*7 % len(bird_textures))
                bird_texture = bird_textures[bird_color][bird_texture_idx]
                bird_angle = max(min(bird_vel[bird_idx]*3.4 + 8, 4), -4) * 8
                blit(bird_texture, [birds_x, birds_y[bird_idx]], bird_angle)

                if draw_hitboxes:
                    pygame.draw.circle(game_surface, (255, 0, 0), world_to_screen([birds_x, birds_y[bird_idx]]),
                                       bird_half_width * (1/texture_to_world_scale * game_scale[0]),
                                       hitboxes_width)

        # Score
        score_str = str(score)
        total_score_width = score_numbers_widths * len(score_str)
        score_x = -1 * total_score_width / 2
        score_y = background_half_height * 0.6
        for number in score_str:
            blit(score_numbers_textures[int(number)], [score_x, score_y], 0)
            score_x += score_numbers_widths


        # Game surface
        window_surface.blit(game_surface, (0, 0))

        # Neural network
        input_nodes_positions  = []
        hidden_nodes_positions = []
        output_nodes_positions = []

        best_bird_idx = np.argmax(fitness) # if couple has the same, best one with elitism is best from prev gen pog!
        input_node_count = input_values[best_bird_idx].shape[0]
        input_nodes_x = ((window_dim[0] - game_dim[0]) / 4) + game_dim[0]
        input_node_r = 20
        space_between_input_nodes = 60
        y = game_dim[1]/2 - (input_node_count - 1)*(2*input_node_r + space_between_input_nodes)*0.5
        for i in range(input_node_count):
            input_nodes_positions.append((input_nodes_x, y))
            y += 2*input_node_r + space_between_input_nodes

        hidden_node_x = ((window_dim[0] - game_dim[0]) / 2) + game_dim[0]
        space_between_hidden_nodes = 60
        hidden_node_r = 20
        y = game_dim[1]/2 - (hidden_neuron_count - 1)*(2*hidden_node_r + space_between_hidden_nodes)*0.5
        for i in range(hidden_neuron_count):
            hidden_nodes_positions.append((hidden_node_x, y))
            y += 2*hidden_node_r + space_between_hidden_nodes

        output_x = (3*(window_dim[0] - game_dim[0])/4) + game_dim[0]
        output_y = game_dim[1]/2
        output_node_pos = (output_x, output_y)
        output_r = 20

        for i, input_node_pos in enumerate(input_nodes_positions):
            for j, hidden_node_pos in enumerate(hidden_nodes_positions):
                weight_color = get_node_or_weight_color(hidden_weights[best_bird_idx][i, j])
                weight_width = int(np.ceil(np.abs(hidden_weights[best_bird_idx][i, j]) * 1.5 + 1))
                pygame.draw.line(window_surface, weight_color, input_node_pos, hidden_node_pos, width=weight_width)
            input_color = get_node_or_weight_color(input_values[best_bird_idx][i])
            pygame.draw.circle(window_surface, input_color, input_node_pos, radius=hidden_node_r)

            label_dim = nn_inputs_order_text[i].get_size()
            label_pos = (input_node_pos[0] - label_dim[0] - hidden_node_r*2, input_node_pos[1] - label_dim[1]//2)
            window_surface.blit(nn_inputs_order_text[i], label_pos)

            value_text = nn_nodes_font.render(f'{input_values[best_bird_idx][i]:.2f}', True, (255, 255, 255))
            value_text_dim = value_text.get_size()
            value_text_pos = (input_node_pos[0] - value_text_dim[0]//2, input_node_pos[1] - value_text_dim[1]//2)
            window_surface.blit(value_text, value_text_pos)
            

        for i, hidden_node_pos in enumerate(hidden_nodes_positions):
            weight_color = get_node_or_weight_color(output_weights[best_bird_idx][i])
            weight_width = int(np.ceil(np.abs(output_weights[best_bird_idx][i]) * 1.5 + 1))
            pygame.draw.line(window_surface, weight_color, hidden_node_pos, output_node_pos, width=weight_width)
            hidden_color = get_node_or_weight_color(hidden_values[best_bird_idx][i])
            pygame.draw.circle(window_surface, hidden_color, hidden_node_pos, radius=hidden_node_r)

            value_text = nn_nodes_font.render(f'{hidden_values[best_bird_idx][i]:.2f}', True, (255, 255, 255))
            value_text_dim = value_text.get_size()
            value_text_pos = (hidden_node_pos[0] - value_text_dim[0]//2, hidden_node_pos[1] - value_text_dim[1]//2)
            window_surface.blit(value_text, value_text_pos)

        output_color = get_node_or_weight_color(output_value[best_bird_idx])
        pygame.draw.circle(window_surface, output_color, output_node_pos, radius=hidden_node_r)

        value_text = nn_nodes_font.render(f'{output_value[best_bird_idx]:.2f}', True, (255, 255, 255))
        value_text_dim = value_text.get_size()
        value_text_pos = (output_node_pos[0] - value_text_dim[0]//2, output_node_pos[1] - value_text_dim[1]//2)
        window_surface.blit(value_text, value_text_pos)

        # Telemetry 
        if display_fps:
            telemetry = [
                    f'Frame time:  {frame_time*1000:.1f}ms',
                    f'FPS: {(1/frame_time) if frame_time != 0 else 0:.0f}',
            ]
            y = 0
            for line in telemetry:
                window_surface.blit(debug_font.render(line, True, (255,255,255)), (0, y))
                y += 30

    # Draw to window
    texture_data = pygame.image.tostring(window_surface, "RGBA", 1)
    width, height = window_surface.get_width(), window_surface.get_height()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)  # Bottom-left
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)   # Bottom-right
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)    # Top-right
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)   # Top-left
    glEnd()

    glDeleteTextures([texture_id])

    # UI
    imgui.new_frame()
    if GAME_STARTED:
        imgui.begin("Settings & Stats")

        imgui.text(f'Generation: {current_generation_idx}')
        imgui.text(f'Birds alive: {alive_count}')
        imgui.text(f'Best fitness this generation: {best_fitness_this_generation}')
        imgui.text(f'Best fitness overall: {best_fitness_overall}')

        imgui.spacing()

        if imgui.button('Skip generation'):
            for bird_idx in range(BIRD_COUNT):
                die(bird_idx)

        imgui.separator()

        _, game_speed_factor = imgui.slider_int("Game speed", game_speed_factor, 0, 20)

        imgui.spacing()

        _, display_fps = imgui.checkbox('Show FPS', display_fps)
        max_fps_change, max_fps_option_idx = imgui.combo("Max FPS", max_fps_option_idx, ['30', '60', '120', '144', '165'])
        if max_fps_change:
            max_fps = max_fps_options[max_fps_option_idx]

        imgui.spacing()

        _, draw_hitboxes = imgui.checkbox('Show Hitboxes', draw_hitboxes)
        _, hitboxes_width = imgui.slider_int("Hitboxes width", hitboxes_width, 0, 5)

        imgui.spacing()

        if imgui.button('QUIT'):
            stoped = True
        imgui.end()
    else:
        imgui.begin("Setup")


        possible_inputs = all_possible_inputs.copy()
        for i in range(len(all_possible_inputs) - 1):
            _, selected_input_idx = imgui.combo(f"Select input {i+1}", selected_inputs[i][1], possible_inputs)
            if selected_input_idx == 0:
                for j in range(i, len(selected_inputs)):
                    selected_inputs[j] = ['', 0]
                break
            else:
                selected_inputs[i][0] = possible_inputs[selected_input_idx]
                selected_inputs[i][1] = selected_input_idx
                possible_inputs.remove(selected_inputs[i][0])

        imgui.spacing()

        _, normalize_inputs = imgui.checkbox('Normalize inputs', normalize_inputs)

        imgui.spacing()

        _, hidden_neuron_count = imgui.input_int('Hidden layer size', hidden_neuron_count)

        imgui.separator()

        _, BIRD_COUNT = imgui.input_int('Population size', BIRD_COUNT)

        _, elitism = imgui.checkbox('Elitism', elitism)

        _, mutation_propability = imgui.slider_float("Mutation propablility", mutation_propability, 0, 1)
        _, mutation_magnitude = imgui.slider_float("Mutation magnitude", mutation_magnitude, 0, 2)
        _, crossover_propability = imgui.slider_float("Crossover propablility", crossover_propability, 0, 1)

        imgui.text('Fitness calculation')

        _, use_reward_point_for_time_survived = imgui.checkbox('Give points for time survived', use_reward_point_for_time_survived)
        if use_reward_point_for_time_survived:
            imgui.indent()
            _, reward_points_for_time_survived = imgui.input_int('Points for time survived', reward_points_for_time_survived)
            imgui.spacing()
            imgui.unindent()

        _, use_reward_points_for_passing_pipe = imgui.checkbox('Give points for passing pipes', use_reward_points_for_passing_pipe)
        if use_reward_points_for_passing_pipe:
            imgui.indent()
            _, reward_points_for_passing_pipe = imgui.input_int('Points for passing pipes', reward_points_for_passing_pipe)
            imgui.spacing()
            imgui.unindent()

        _, use_punish_points_hitting_ground = imgui.checkbox('Punish for hitting ground', use_punish_points_hitting_ground)
        if use_punish_points_hitting_ground:
            imgui.indent()
            _, punish_points_hitting_ground = imgui.input_int('Points for hittin ground', punish_points_hitting_ground)
            imgui.spacing()
            imgui.unindent()

        _, use_punish_points_flying_above_screen = imgui.checkbox('Punish for flying above screen', use_punish_points_flying_above_screen)
        if use_punish_points_flying_above_screen:
            imgui.indent()
            _, punish_points_flying_above_screen = imgui.input_int('Points for flying above screen', punish_points_flying_above_screen)
            imgui.spacing()
            imgui.unindent()

        if imgui.button('START SIMULATION'):
            failed = False
            if input_count == 0:
                failed = True
                failed_no_inputs = True
            if mutation_propability == 0 and crossover_propability == 0:
                failed = True
                failed_zero_probabilities = True

            if not failed:
                GAME_STARTED = True

                input_count = 0
                for selected_input in selected_inputs:
                    if selected_input[1] == 0: break
                    else:
                        input_count += 1
                        nn_inputs_order.append(selected_input[0])
                        nn_inputs_order_text.append(nn_inputs_font.render(selected_input[0], True, (255, 255, 255)))

                # Init population
                birds_y = [0 for _ in range(BIRD_COUNT)]
                bird_vel = [0 for _ in range(BIRD_COUNT)]
                birds_colors = [np.random.choice([bird_color_yellow, bird_color_blue, bird_color_red]) for _ in range(BIRD_COUNT)]
                alive = [True for _ in range(BIRD_COUNT)]
                alive_count = BIRD_COUNT
                
                fitness = np.array([0 for _ in range(BIRD_COUNT)])
                
                input_values  = [np.array([0, 0, 0, 0]) for _ in range(BIRD_COUNT)]
                hidden_weights = [np.random.normal(size=(input_count, hidden_neuron_count)) for _ in range(BIRD_COUNT)]
                hidden_biases  = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
                hidden_values = [np.array([0 for _ in range(hidden_neuron_count)]) for __ in range(BIRD_COUNT)]
                output_weights = [np.random.normal(size=hidden_neuron_count) for _ in range(BIRD_COUNT)]
                output_value = [0 for _ in range(BIRD_COUNT)]


        imgui.indent()
        if failed_no_inputs:
            imgui.text('You must select at least one input')

        if failed_zero_probabilities:
            imgui.text('At least one of probabilities must be non-zero')

        imgui.end()

    imgui.render()
    impl.render(imgui.get_draw_data())


    pygame.display.flip()

    ######################################## Frame rate
    fps = max_fps
    s_per_frame = 1/fps

    elapsed = time.perf_counter() - frame_start
    if elapsed < s_per_frame:
        time.sleep(s_per_frame - elapsed)

    frame_end = time.perf_counter() 
    frame_time = frame_end - frame_start
    frame_start = frame_end
