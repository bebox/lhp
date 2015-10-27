import pygame_sdl2 as pygame
from pygame_sdl2.locals import *

pygame.init()

spriteFont = [
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
    " ", "!", "\"", "#", "$", "%", "", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
    "", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
    "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", ""
    ]

loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque posuere, est eu finibus posuere, velit nunc faucibus orci, eget congue ligula erat eu nisi. Mauris sed accumsan risus. Nulla pretium urna eu ante consequat lobortis. Suspendisse non arcu porta, aliquam ante eu, ornare tellus. Ut vestibulum vel ex quis consequat. Phasellus auctor fringilla orci, ac viverra metus pulvinar at. Suspendisse non lectus eget justo dapibus scelerisque. Nullam nec venenatis lorem, in elementum sem. Cras sollicitudin ligula vitae nibh dignissim sagittis. Duis vitae finibus nibh. Maecenas ut orci a elit tristique porta quis in massa. Suspendisse id mattis mi, eu dapibus enim. Praesent sodales ante eget ligula euismod, vel pulvinar nibh tempor."

display_scale_factor_x = 8 #display scale factor becouse original resolution is 160x90
display_scale_factor_y = 8 #display scale factor becouse original resolution is 160x90
display_width = 160*display_scale_factor_x #this is graphics resolution, hardcoded
display_height = 90*display_scale_factor_y #this is graphics resolution, hardcoded

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('lilypond hybride pianoroll 0.1')
color_white = (255,255,255)
clock = pygame.time.Clock()
crashed = False

picSpriteFont = pygame.image.load('tom-thumb-new.png')
listSpriteFont = []
for column in range(0,4):
    for row in range(0, 32):
        picSpriteFont.set_clip(pygame.Rect(row*4,column*6,4,6))
        print(pygame.Rect(row*4,column*6,4,6))
        listSpriteFont.append(picSpriteFont.subsurface(picSpriteFont.get_clip()))

def blitFont(x, y, letter):
        screen.blit(pygame.transform.scale(listSpriteFont[letter], (4*display_scale_factor_x, 6*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    for i,letter in enumerate(loremIpsum): #tu denes loremIpsum varijablu
    #for i,letter in enumerate("Daniel debeli Kreko"): #tu denes loremIpsum varijablu
        blitFont((i%40)*4,int(i/40)*6, spriteFont.index(letter))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

