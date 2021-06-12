import pygame
import sys

# Icon made by Freepik from www.flaticon.com

#starts up pygame
pygame.init()

#width and height of the window
WIDTH = 800
HEIGHT = 600
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)

# black-colored quit button (default look) (32x32)
quit_img = pygame.image.load('exit.png')
# when hovered quit button lights up (32x32)
quit_light_img = pygame.image.load('exit_light.png')

play_button = pygame.image.load('play.png')
play_light = pygame.image.load('playlight.png')

# background 800 x 600 img
gamebg = pygame.image.load('gamebg.png')

# load music, set volume, -1 = plays song infinitely, change it to 0 to play once only
pygame.mixer.music.load('8bitmusic.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

while True:
    #draws the background using the image
    screen.blit(gamebg, (0, 0))
    #gets the mouse position as a tuple (x, y) mouse[0] for x and mouse[1] for y
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        #if X button of window is clicked the game is exited
        if event.type == pygame.QUIT:
            sys.exit()

        # if quit button location is clicked the game is exited
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 800 >= mouse[0] >= 800 - 32 and 600 >= mouse[1] >= 600 - 32:
                sys.exit()

    #the default quit button will be drawn and if hovered over the quit light up button is drawn instead
    if 800 >= mouse[0] >= 800 - 32 and 600 >= mouse[1] >= 600 - 32:
        screen.blit(quit_light_img, (800 - 32, 600 - 32))
    else:
        screen.blit(quit_img, (800 - 32, 600 - 32))

    # play button
    if WIDTH/2 + 32 >= mouse[0] >= WIDTH/2 - 32 and HEIGHT/2 + 64 >= mouse[1] >= HEIGHT/2:
        screen.blit(play_light, (WIDTH/2 - 32, HEIGHT/2))
    else:
        screen.blit(play_button, (WIDTH/2 - 32, HEIGHT/2))

    # this is to update the game loop
    pygame.display.update()
