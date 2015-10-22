#!/usr/bin/env python3

import pygame_sdl2 as pygame
import math
from pygame_sdl2.locals import *
from lhpFunctions import *

pygame.init()

#scale and display resolution
display_scale_factor_x = 1 #display scale factor becouse original resolution is 160x90
display_scale_factor_y = 1 #display scale factor becouse original resolution is 160x90
display_width = 1200*display_scale_factor_x #this is graphics resolution, hardcoded
display_height = 600*display_scale_factor_y #this is graphics resolution, hardcoded
zoom_factor = 1
zoom_x = int(208/zoom_factor)
zoom_y = int(31)
bar = 10

listZoomFactor = [32, 16, 8, 4, 2, 1, 1/2, 1/4, 1/8, 1/16]
#listZoomFactor = [math.log(i*0.1+0.1) for i in range(1, 100)]
#listZoomFactor = [i*i*0.1 for i in range(1, 100)]

#screen is a pygame default window

screen = pygame.display.set_mode((display_width,display_height))

#program caption title
pygame.display.set_caption('lilypond hybride pianoroll' + get_git_revision_short_hash())

#RGB colors definitions
#color_black = (0,0,0)

##pygame clock
clock = pygame.time.Clock()
##variable which exits the program
crashed = False

#pictures loaded
picSpriteFont = pygame.image.load('../image/tom-thumb-new.png')
picBarLine = pygame.image.load('../image/barLine.png')
picBarLines = pygame.image.load('../image/barLines.png')
picGridLine = pygame.image.load('../image/gridLine.png')
picGridDot = pygame.image.load('../image/gridDot.png')
picCursor = pygame.image.load('../image/cursor.png')
picNote = pygame.image.load('../image/note.png')

##loading letter sprites into list
listSpriteFont = []
##defining field
for column in range(0,4):
    for row in range(0, 32):
        picSpriteFont.set_clip(pygame.Rect(row*4,column*6,4,6))
        listSpriteFont.append(picSpriteFont.subsurface(picSpriteFont.get_clip()))

##bliting functions
##bliting of a letter
def blitFont(x, y, letter):
        screen.blit(pygame.transform.scale(listSpriteFont[letter], (4*display_scale_factor_x*3, 6*display_scale_factor_y*3)), (x*display_scale_factor_x*3, y*display_scale_factor_y*3))

##bliting of a barLine
def blitBarLine(x, y):
        screen.blit(pygame.transform.scale(picBarLine, (6*display_scale_factor_x, 290*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a barLines
def blitBarLines(x, y, zoom):
        #for i in range(zoom_x):
        #    screen.blit(pygame.transform.scale(picBarLines, (1*display_scale_factor_x, 7*display_scale_factor_y)), (i+x*display_scale_factor_x, y*display_scale_factor_y))
        pixel = int(208/zoom_factor)
        for i in range(int(zoom_x/pixel)):
            screen.blit(pygame.transform.scale(picBarLines, (pixel*display_scale_factor_x, 7*display_scale_factor_y)), (i*pixel+x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a gridLine
def blitGridLine(x, y):
        screen.blit(pygame.transform.scale(picGridLine, (7*display_scale_factor_x, 290*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a gridDot
def blitGridDot(x, y):
        screen.blit(pygame.transform.scale(picGridDot, (8*display_scale_factor_x, 8*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))


##bliting of a cursor
listCursor = []
picCursor.set_clip(pygame.Rect(0,0,5,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))
picCursor.set_clip(pygame.Rect(47,0,5,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))
picCursor.set_clip(pygame.Rect(26,0,1,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))

def blitCursor(x, y, velicina):
        #should be 43 when it is big 1/4
        for i in range(int(velicina*52*4)):
            screen.blit(pygame.transform.scale(listCursor[2], (1*display_scale_factor_x, 52*display_scale_factor_y)), (i+x*display_scale_factor_x, y*display_scale_factor_y))
        #wide 5 pix
        screen.blit(pygame.transform.scale(listCursor[0], (5*display_scale_factor_x, 52*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))
        #wide 5 pix
        screen.blit(pygame.transform.scale(listCursor[1], (5*display_scale_factor_x, 52*display_scale_factor_y)), ((velicina*52*4-5)+x*display_scale_factor_x, y*display_scale_factor_y))

#bliting note
listNote = []
picNote.set_clip(pygame.Rect(0,0,14,24))
listNote.append(picNote.subsurface(picNote.get_clip()))
picNote.set_clip(pygame.Rect(15,0,1,24))
listNote.append(picNote.subsurface(picNote.get_clip()))
picNote.set_clip(pygame.Rect(16,0,14,24))
listNote.append(picNote.subsurface(picNote.get_clip()))

def blitNote(x, y, velicina):
        #wide 5 pix
        screen.blit(pygame.transform.scale(listNote[0], (14*display_scale_factor_x, 24*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))
        #should be 43 when it is big 1/4
        for i in range(int(velicina*zoom_x)):
            screen.blit(pygame.transform.scale(listNote[2], (1*display_scale_factor_x, 24*display_scale_factor_y)), (14+i+x*display_scale_factor_x, y*display_scale_factor_y))
        #wide 5 pix
        screen.blit(pygame.transform.scale(listNote[2], (14*display_scale_factor_x, 24*display_scale_factor_y)), (14+velicina*52*4+x*display_scale_factor_x, y*display_scale_factor_y))

base_x = 50
base_y = display_height/2
bar_grid = 8
timeSignature = (4,4)
pozicija_x = 0
pozicija_x_staro = 0
pozicija_y = 0
pozicija_y_staro = 0

obj_cursor = cursor(1, 0, timeSignature[1], timeSignature[1])

#convert pixel into x:position
def pixel2Pos(pixel):
    pozicija_x = int((pixel-base_x+zoom_x)/zoom_x) #-1
    return(pozicija_x)
#convert pixel into y:tone
def pixel2Tone(pixel):
    pozicija_y = int(-(pixel-base_y+zoom_y*10)/zoom_y)+10
    return(pozicija_y)
def pos2Pixel(pos):
    pixel = (pos*zoom_x)+base_x-zoom_x
    return(pixel)
def tone2Pixel(pos):
    pixel = (-pos*zoom_y+base_y-zoom_y*10)+10*zoom_y
    return(pixel)


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

##Keyboard buttons without MODS
        if event.type == pygame.MOUSEMOTION:
            #print ("mouse at (%d, %d)" % event.pos)
            snap = roundSnap[hashMusic2Float[obj_cursor.snap]]
            pozicija_y = round((-(event.pos[1]-base_y+zoom_y*10)/zoom_y)+10)
            pozicija_x = int( ((event.pos[0]-base_x+zoom_x)/zoom_x) * snap)/snap
            #pozicija_x = pixel2Pos(event.pos[0])
            obj_cursor.pozicija = pozicija_x
            #pozicija_y = pixel2Tone(event.pos[1])
            obj_cursor.ton = pozicija_y
            #print(pos2Pixel(pozicija_x))
            #print(tone2Pixel(pozicija_y))
            if pozicija_x != pozicija_x_staro or pozicija_y != pozicija_y_staro:
                pozicija_x_staro = pozicija_x
                pozicija_y_staro = pozicija_y
                print("X:" + str(pozicija_x) + ", Y:" + str(pozicija_y))
                #print ("mouse at (%d, %d)" % event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            print("oj")
            if event.button == 4:
                zoom_factor = listIndexStep(zoom_factor, listZoomFactor, +1)
            if event.button == 5:
                zoom_factor = listIndexStep(zoom_factor, listZoomFactor, -1)

        if event.type == pygame.KEYDOWN:

            if pygame.key.get_mods() == 0:
                if event.key == pygame.K_RIGHT:
                    obj_cursor.pozicija += hashMusic2Float[obj_cursor.snap]
                if event.key == pygame.K_LEFT:
                    obj_cursor.pozicija -= hashMusic2Float[obj_cursor.snap]
                if event.key == pygame.K_UP:
                    obj_cursor.ton += 1
                if event.key == pygame.K_DOWN:
                    obj_cursor.ton -= 1

                if event.key == pygame.K_p:
                    print(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje)

            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                if event.key == pygame.K_RIGHT:
                    obj_cursor.trajanje = listIndexStep(obj_cursor.trajanje, listMusic2Float, +1)
                if event.key == pygame.K_LEFT:
                    obj_cursor.trajanje = listIndexStep(obj_cursor.trajanje, listMusic2Float, -1)
                if event.key == pygame.K_UP:
                    obj_cursor.snap = listIndexStep(obj_cursor.snap, listMusic2Float, +1)
                if event.key == pygame.K_DOWN:
                    obj_cursor.snap = listIndexStep(obj_cursor.snap, listMusic2Float, -1)
#
#    #flipanje
    zoom_x = int(208/zoom_factor)
    screen.fill(color_git)

    #bliting grid dots
    for y in range(0,4):
        for i in range(0, int(timeSignature[0]*int(obj_cursor.snap)/timeSignature[1])*bar):
            #if hashGrid[listGrid[cursor_grid]] < timeSignature[1]:
                #zoom_x is beat lenght
                #blitGridDot(base_x+((i*zoom_x/timeSignature[1])+(zoom_x/timeSignature[1]/2)),base_y-4-31+(y*62)-(62))
                #           base    distance    offset
                blitGridDot(base_x+((zoom_x*hashMusic2Float[obj_cursor.snap])*i+(zoom_x*hashMusic2Float[listIndexStep(obj_cursor.snap, listMusic2Float, -1)])),base_y-4-31+(y*62)-(62))
                #blitGridDot(base_x+((zoom_x)*i),base_y-4-31+(y*62)-(62))

    #bliting horizontal barlines
    for y in range(0,5):
        for i in range(0,int(timeSignature[0]*bar*hashMusic2Float[timeSignature[1]])):
            blitBarLines(base_x+(i*zoom_x),base_y-(6/2)+(y*62)-(62*2), zoom_x)

    #bliting grid lines
    for i in range(0,timeSignature[0]*(bar)):
        if i%timeSignature[0] != 0:
            blitGridLine(base_x+(int(i*zoom_x*hashMusic2Float[timeSignature[1]])), base_y-(290/2))

    #bliting bar lines
    for i in range(0,bar):
        blitBarLine(base_x+(int(i*zoom_x*timeSignature[0]*hashMusic2Float[timeSignature[1]])),base_y-(290/2))

    blitCursor(pos2Pixel(obj_cursor.pozicija), tone2Pixel(obj_cursor.ton)-(52/2), hashMusic2Float[obj_cursor.trajanje]/zoom_factor)
    #blitNote(base_x+cursor_x+4,base_y-cursor_y, hashSnap[listSnap[cursor_size]])

    ##blit snap text
    for i,letter in enumerate("Time:" + str(timeSignature) + " Snap:" + str(obj_cursor.snap) + " Duration:" + str(obj_cursor.trajanje) + " Bar:" + str(obj_cursor.pozicija) + "/" + str(bar) + " Pos:" + str(obj_cursor.pozicija) + " Note:" + str(obj_cursor.ton) + " Zoom:" + str(zoom_factor)): #tu denes loremIpsum varijablu
        blitFont((i%100)*4,int(i/100)*6, spriteFont.index(letter))

    #blit grid text
    #for i,letter in enumerate("Grid: " + str(bar_grid)): #tu denes loremIpsum varijablu
    #    blitFont((i%40)*4,int(i/40)*6+7, spriteFont.index(letter))
#
#
#    #plavi okvir
#    blit_kljucevi(0,-15+bg_scroll_y)
#    blit_rub(0,0)
    pygame.display.flip()
    clock.tick(60)
#
pygame.quit()
#quit()
