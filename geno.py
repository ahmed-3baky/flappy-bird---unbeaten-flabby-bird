import random 
import sys 
import pygame
from pygame.locals import * 

import pygad
import threading

class PygadThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        ga_instance = pygad.GA(num_generations=20,
                       sol_per_pop=10,
                       num_parents_mating=5,
                       num_genes=1,
                       fitness_func=fitness_func,
                       init_range_low=100.0,
                       init_range_high=200.0,
                       random_mutation_min_val=50.0,
                       random_mutation_max_val=350.0,
                       mutation_by_replacement=True,
                       on_generation=on_generation,
                       crossover_type= "single_point",
                       suppress_warnings=True)

        ga_instance.run()

last_gen_best_solution = 0
def on_generation(ga_inst): 
    global last_gen_best_solution, playery

    best_sol, best_sol_fit, _ = ga_inst.best_solution()

    if playery > best_sol:playery = playery - 15
    elif playery < best_sol:playery = playery + 15

    last_gen_best_solution = best_sol

def closest_pipe(playerx, pipes):
    pipe0X = abs(playerx - pipes[0]['x'])
    pipe1X = abs(playerx - pipes[1]['x'])

    if pipe0X < pipe1X:
        return 0
    else:
        return 1

def fitness_func(ga_instance, solution, solution_idx):
    global playery, pipe_height, playerx, top_pipes, bottom_pipes, shapes, ground

    if type(solution) is int:pass
    else:solution = solution[0]
    if solution < 0:return -8888
    if solution > ground - 25:return -9999
    fitness_ground = abs(solution - ground)
    if fitness_ground < 50:fitness_ground = (-1.0/fitness_ground) * 999999
    
    near_top_pipe = top_pipes[closest_pipe(playerx, top_pipes)]
    pipe_height = shapes['pipe'][0].get_height()
    fitness_upper = abs(solution - (pipe_height + near_top_pipe['y']))
    if(solution < pipe_height + near_top_pipe['y'] + 50 and abs(playerx - near_top_pipe['x']) < shapes['pipe'][0].get_width() + 50):
        fitness_upper = (-1.0/fitness_upper) * 999999
    else:
        fitness_upper = fitness_upper

    near_bottob_pipe = bottom_pipes[closest_pipe(playerx, bottom_pipes)]
    fitness_lower = abs(solution + shapes['player'].get_height() - near_bottob_pipe['y']) 
    if (solution + shapes['player'].get_height() > near_bottob_pipe['y'] - 50) and abs(playerx - near_bottob_pipe['x']) < shapes['pipe'][0].get_width() + 50:
        fitness_lower = (-1.0/fitness_lower) * 999999
    else:
        fitness_lower = fitness_lower

    fitness = (fitness_ground + fitness_upper + fitness_lower)/3
    return fitness

shapes = {}
sounds = {}
s_width = 500 ; s_height = 500
s = pygame.display.set_mode((s_width, s_height))
ground = s_height * 0.84 ; frames = 20

bird = 'data/shapes/bird.png'
BG = 'data/shapes/background.png'
pipe = 'data/shapes/pipe.png'

def Start():


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                s.blit(shapes['background'], (0, 0))    

                pygame.display.update()
                frames_clock.tick(frames)

def main():
    global playerx, playery, top_pipes, bottom_pipes
    score = 0
    playerx = int(s_width/5)
    playery = int(s_width/5)
    intial_val = 0

    new_pipe = random_pipe()
    new_pipe2 = random_pipe()

    # my List of upper pipes
    top_pipes = [
        {'x': s_width + 200, 'y': new_pipe[0]['y']},
        {'x': s_width + 200 + (s_width/2), 'y': new_pipe2[0]['y']},
    ]
    # my List of lower pipes
    bottom_pipes = [
        {'x': s_width + 200, 'y': new_pipe[1]['y']},
        {'x': s_width + 200+ (s_width/2), 'y': new_pipe2[1]['y']},
    ]

    pipe_x_spead = -20

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        crashTest = Crushed(playerx, playery, top_pipes, bottom_pipes) 
        if crashTest:
            return   

        # score
        Mid_Pos = playerx + shapes['player'].get_width()/2
        for pipe in top_pipes:
            pipeMidPos = pipe['x'] + shapes['pipe'][0].get_width()/2
            if pipeMidPos <= Mid_Pos < pipeMidPos + abs(pipe_x_spead):
                score += 1
                print(f"Your score is {score}") 
                sounds['POINT_'].play()

        for upperPipe , lowerPipe in zip(top_pipes, bottom_pipes):
            upperPipe['x'] += pipe_x_spead
            lowerPipe['x'] += pipe_x_spead

        if 0 < top_pipes[0]['x'] < abs(pipe_x_spead) + 1:
            newpipe = random_pipe()
            top_pipes.append(newpipe[0])
            bottom_pipes.append(newpipe[1])

        if top_pipes[0]['x'] < -shapes['pipe'][0].get_width():
            top_pipes.pop(0)
            bottom_pipes.pop(0)

        s.blit(shapes['background'], (0, 0))
        for upperPipe, lowerPipe in zip(top_pipes, bottom_pipes):
            s.blit(shapes['pipe'][0], (upperPipe['x'], upperPipe['y']))
            s.blit(shapes['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        s.blit(shapes['base'], (intial_val, ground))
        s.blit(shapes['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += shapes['numbers'][digit].get_width()
        Xoffset = (s_width - width)/2

        for digit in myDigits:
            s.blit(shapes['numbers'][digit], (Xoffset, s_height*0.12))
            Xoffset += shapes['numbers'][digit].get_width()
        pygame.display.update()
        frames_clock.tick(frames)

def Crushed(playerx, playery, top_pipes, bottom_pipes):
    pygad_thread = PygadThread()
    pygad_thread.run()

    if playery > ground - 25  or playery < 0:
        print("Ground", playery, fitness_func(None, playery, 0))
        sounds['hit'].play()
        return True

    for pipe in top_pipes:
        pipe_height = shapes['pipe'][0].get_height()
        if(playery < pipe_height + pipe['y'] and abs(playerx - pipe['x']) < shapes['pipe'][0].get_width()):
            print("Upper", playery, fitness_func(None, playery, 0))
            sounds['hit'].play()
            return True

    for pipe in bottom_pipes:
        if (playery + shapes['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < shapes['pipe'][0].get_width():
            print("Lower", playery, fitness_func(None, playery, 0))
            sounds['hit'].play()
            return True

    return False

def random_pipe():
    global pipe_height

    pipe_height = shapes['pipe'][0].get_height()
    new_of = s_height/3
    y2 = new_of + random.randrange(0, int(s_height - shapes['base'].get_height()  - 1.2 *new_of))
    pipeX = s_width + 10
    y1 = pipe_height - y2 + new_of
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2}  ] 
    return pipe


pygame.init() 
frames_clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird ')

shapes['base'] =pygame.image.load('data/shapes/base.png').convert_alpha()
shapes['pipe'] =(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(), 180), 
pygame.image.load(pipe).convert_alpha()
)



shapes['background'] = pygame.image.load(BG).convert()
shapes['player'] = pygame.image.load(bird).convert_alpha()

# Game sounds
sounds['hit'] = pygame.mixer.Sound('data/audio/hit.wav')
sounds['POINT_'] = pygame.mixer.Sound('data/audio/POINT_.wav')
sounds['FLY'] = pygame.mixer.Sound('data/audio/FLY.wav')

shapes['numbers'] = ( 
    pygame.image.load('data/shapes/0.png').convert_alpha(),
    pygame.image.load('data/shapes/1.png').convert_alpha(),
    pygame.image.load('data/shapes/2.png').convert_alpha(),
    pygame.image.load('data/shapes/3.png').convert_alpha(),
    pygame.image.load('data/shapes/4.png').convert_alpha(),
    pygame.image.load('data/shapes/5.png').convert_alpha(),
    pygame.image.load('data/shapes/6.png').convert_alpha(),
    pygame.image.load('data/shapes/7.png').convert_alpha(),
    pygame.image.load('data/shapes/8.png').convert_alpha(),
    pygame.image.load('data/shapes/9.png').convert_alpha(),
)



while True:
    Start()
    main() 