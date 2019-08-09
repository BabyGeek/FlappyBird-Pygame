#!/usr/bin/env python
"""
    Flappy bird copy by Paul Oggero
    Images source : https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites
"""

import pygame, sys, time, random
clock = pygame.time.Clock()
from pygame.locals import *

pygame.init()

# Loading images
base_image = pygame.image.load("images/base.png")
player_image = pygame.image.load("images/bird.png")
top_pipe_image = pygame.image.load("images/top_pipe.png")
bottom_pipe_image = pygame.image.load("images/bottom_pipe.png")
icon_image = pygame.image.load("images/icon.png")


# Window settings
pygame.display.set_caption("Flappy Copy")
resolution = display_width, display_height = (350, 650)
screen = pygame.display.set_mode(resolution, 0, 32)
display = pygame.Surface((288, 624)) # used as the surface for rendering, which is scaled
pygame.display.set_icon(icon_image)

global animation_frames
animation_frames = {}

def score(count):
    font = pygame.font.Font('fonts/3Dventure.ttf', 40)
    score = font.render(str(count), True, (255, 255, 255))
    display.blit(score, [144, 0])
    
    

def start():
    """
        Begining of the game with starting screen
    """
    global background_image
    
    start_background = pygame.image.load("images/start.png")
    base_location = [0, 512]
    base_movement = -2    
    
    # Random background
    backgrounds = ["images/background.png", "images/background-night.png"]
    background = random.randint(0, len(backgrounds) - 1)
    background_image = pygame.image.load(backgrounds[background])
    
    # Displaying background
    display.blit(background_image, (0, 0))
    display.blit(start_background, (52, 150))
    
    # Displaying base
    display.blit(base_image, base_location)
    
    # Scaling display on screen and refresh
    screen.blit(pygame.transform.scale(display, resolution), (0, 0))        
    pygame.display.flip()
    
    waiting = True
    
    while waiting:                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                waiting = True
                game_loop()
    
    
def pipes(x, y, space):
    display.blit(top_pipe_image, (x, y))
    display.blit(bottom_pipe_image, (x, y + space + bottom_pipe_image.get_height()))

def load_animation(path, frame_durations):
    """
        Load animations images
        Return a list of names
    """
    global animation_frames    
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

# Load bird animations for IDLE
animation_database = {}
animation_database['idle'] = load_animation('images/bird_animations/idle', [7, 7, 40])

# Setting player frame and action at begining
player_frame = 0
player_action = 'idle'


def create_text_object(message, font, color):
    text_surface = font.render(message, True, color)
    
    return text_surface, text_surface.get_rect()

def message(big_message, small_message, color_1 = (255, 0, 0), color_2 = (255, 0, 0)):
    """
        Define a message from a string    
    """
    text = pygame.font.Font('fonts/04B_30__.ttf', 40)
    small_text = pygame.font.Font('fonts/04B_30__.ttf', 15)
    
    text_surface, text_rect = create_text_object(big_message, text, color_1)
    text_rect.center = 144, 312 - 50
    display.blit(text_surface, text_rect)
    
    small_text_surface, small_text_rect = create_text_object(small_message, small_text, color_2)
    small_text_rect.center = 144, 312 - 10
    display.blit(small_text_surface, small_text_rect)
    
    screen.blit(pygame.transform.scale(display, resolution), (0, 0))        
    pygame.display.flip()
    

def game_over():
    """
        Printing message when the game is over
    """
    global player_location
    
    message('You died', 'Press a key to restart')
    
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                waiting = False
    start()

def game_loop():
    global player_frame, player_action, background_image, player_rect, player_location
    # Bird mouvement and start location
    up = False
    down = False
    
    player_location = [50, 312]
    y_movement = 0
    
    # Base movement
    base_location = [0, 512]
    base_movement = -4
    
    # Pipes location
    x = 288
    y = random.randint(-600, -400)
    space = pygame.image.load("images/bird_animations/idle/idle_0.png").get_width() * 3
    pipe_speed = 5
    
    # Score
    score_actuel = 0
    
    while True:
        
        # Displaying background
        display.blit(background_image, (0, 0))
        
        # Displaying bird
        player_frame += 2
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
            
        player_img_id = animation_database[player_action][player_frame]
        player_image = animation_frames[player_img_id]
        
        # Rotation de l'image selon le déplacement du joueur
        if up == False and down == False:
            display.blit(player_image, player_location)
        if up == True:
            display.blit(pygame.transform.rotate(player_image, 25), player_location)        
        if down == True:
            display.blit(pygame.transform.rotate(player_image, -25), player_location)                
           
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_SPACE:
                    y_movement = -6
                    up = True
                    down = False
            elif event.type == KEYUP:
                y_movement = 4
                up = False
                down = True
                
        player_location[1] += y_movement
        
        # Displaying pipes
        pipes(x, y, space)
        x -= pipe_speed
        
        # Displaying score
        score(score_actuel)
        
        # Checking collisions
        player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
        top_pipe_rect = pygame.Rect(x, y, top_pipe_image.get_width(), top_pipe_image.get_height())
        bottom_pipe_rect = pygame.Rect(x, y + space + bottom_pipe_image.get_height(), bottom_pipe_image.get_width(), bottom_pipe_image.get_height())
                
        if player_rect.colliderect(top_pipe_rect) or player_rect.colliderect(bottom_pipe_rect):
            game_over()
        
        # If the pipe is out, another appear
        if x <= -top_pipe_image.get_width():
            x = 288
            y = random.randint(-700, -400)
            top_pipe_rect = pygame.Rect(x, y, top_pipe_image.get_width(), top_pipe_image.get_height())
            bottom_pipe_rect = pygame.Rect(x, y + space + bottom_pipe_image.get_height(), bottom_pipe_image.get_width(), bottom_pipe_image.get_height())
            score_actuel += 1
            
        # Displaying base and moving it 
        base_location[0] += base_movement
        
        if base_location[0] < -24:
            base_location[0] = 0
        
        display.blit(base_image, base_location)
        
        # Boundaries
        if player_location[1] >= 512 - player_image.get_height() or player_location[1] < 0:
            game_over()
             
        # Scaling and refreshing
        screen.blit(pygame.transform.scale(display, resolution), (0, 0))    
        pygame.display.update()
        clock.tick(60)
start()