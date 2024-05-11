import random 
import sys 
import pygame
from pygame.locals import * 

shapes = {}
sounds = {}
s_width = 500 ; s_height = 500
s = pygame.display.set_mode((s_width, s_height))
ground = s_height *0.84 ; frames = 40

bird = 'data/shapes/bird.png'
BG = 'data/shapes/background.png'
pipe = 'data/shapes/pipe.png'

def Start():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                s.blit(shapes['background'], (0, 0))    
  
                pygame.display.update()
                frames_clock.tick(frames)

def main():
    score = 0
    playerx = int(s_width/5)
    playery = int(s_width/5)
    intial_val = 0

    new_pipe = random_pipe()
    new_pipe2 = random_pipe()

    top_pipes = [
        {'x': s_width+200, 'y':new_pipe[0]['y']},
        {'x': s_width+200+(s_width/2), 'y':new_pipe2[0]['y']},
    ]
    bottom_pipes = [
        {'x': s_width+200, 'y':new_pipe[1]['y']},
        {'x': s_width+200+(s_width/2), 'y':new_pipe2[1]['y']},
    ]

    bird_speed = -8 
    status = False 
    bird_current_val = -9 ; bird_y_max = 10
    bird_balance = 1 ; pipe_x_spead = -7
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    bird_current_val = bird_speed
                    status = True
                    sounds['FLY'].play()
        
        crashTest = Crushed(playerx, playery, top_pipes, bottom_pipes) 
        if crashTest:
            return     

        #score
        Mid_Pos = playerx + shapes['player'].get_width()/2
        for pipe in top_pipes:
            pipeMidPos = pipe['x'] + shapes['pipe'][0].get_width()/2
            if pipeMidPos<= Mid_Pos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                sounds['POINT_'].play()

        if bird_current_val <bird_y_max and not status: bird_current_val += bird_balance

        if status: status = False            
        bird_height = shapes['player'].get_height()
        playery = playery + min(bird_current_val, ground - playery - bird_height)

        for i , j in zip(top_pipes, bottom_pipes):
            i['x'] += pipe_x_spead
            j['x'] += pipe_x_spead

        # Add a new pipe 
        if 0<top_pipes[0]['x']<8:
            newpipe = random_pipe()
            top_pipes.append(newpipe[0])
            bottom_pipes.append(newpipe[1])

        if top_pipes[0]['x'] < -shapes['pipe'][0].get_width():
            top_pipes.pop(0)
            bottom_pipes.pop(0)
        
        # blit shapes
        s.blit(shapes['background'], (0, 0))
        for i, j in zip(top_pipes, bottom_pipes):
            s.blit(shapes['pipe'][0], (i['x'], i['y']))
            s.blit(shapes['pipe'][1], (j['x'], j['y']))

        s.blit(shapes['base'], (intial_val, ground))
        s.blit(shapes['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += shapes['numbers'][digit].get_width()
        xoff = (s_width - width)/2

        for digit in myDigits:
            s.blit(shapes['numbers'][digit], (xoff, s_height*0.12))
            xoff += shapes['numbers'][digit].get_width()
        pygame.display.update()
        frames_clock.tick(frames)

def Crushed(playerx, playery, top_pipes, bottom_pipes):
    if playery> ground - 25  or playery<0:
        sounds['hit'].play()
        return True
    
    for pipe in bottom_pipes:
        if (playery + shapes['player'].get_height() > pipe['y']) and abs(playerx-pipe['x']) < shapes['pipe'][0].get_width():
            sounds['hit'].play()
            return True
        
    for pipe in top_pipes:
        pipe_height = shapes['pipe'][0].get_height()
        if(playery < pipe_height + pipe['y'] and abs(playerx - pipe['x']) < shapes['pipe'][0].get_width()):
            sounds['hit'].play()
            return True


    return False

def random_pipe():
    pipe_height = shapes['pipe'][0].get_height()
    new_of = s_height/3
    y2 = new_of + random.randrange(0, int(s_height - shapes['base'].get_height()  - 1.5 *new_of))
    pipeX = s_width + 10
    y1 = pipe_height - y2 + new_of
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2}   
    ]
    return pipe





if __name__ == "__main__":

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