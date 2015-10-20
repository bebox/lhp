#!/usr/bin/env python3

#import argparse
#import subprocess
#parser = argparse.ArgumentParser()
#parser.add_argument("-m", "--midiout", help="enable midi output", action="store_true")
#parser.add_argument("-c", "--midiport", type=int,  help="connect to midi port")
#parser.add_argument("-l", "--listmidiports",  help="list midi ports and exit", action="store_true")
#parser.add_argument("-p", "--projectname",  help="project name, use *.lhp extension", type=str)
#parser.add_argument('--version', action='version', version=subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8"))
#args = parser.parse_args()

import pygame_sdl2 as pygame
from pygame_sdl2.locals import *
from lhpFunctions import *

#import operator
#import pickle #used for saving and loading projects
#import math #used for scrolling screen
#import re
#
#if args.listmidiports or args.midiport:
#    args.midiout = True
#
#if args.midiout:
#    import time
#    import rtmidi
#    midiout = rtmidi.MidiOut()
#    available_ports = midiout.get_ports()
#    print("MIDIout enabled")
#
#if args.listmidiports:
#    for i,y in enumerate(available_ports):
#        print(i+1, ":", y)
#    quit()
#
#if args.midiport:
#    midiout.open_port(args.midiport-1)
#    print("lhp connected to", available_ports[args.midiport-1])
#elif not args.midiport and args.midiout:
#    midiout.open_virtual_port("lhp")
#    print("Created virtual MIDIport: lhp")
#
#if args.projectname:
#    print("Project name:", args.projectname)
#    #lista_nota = pickle.load(open( args.projectname, "rb" ))
#
#else:
#    args.projectname = "save.lhp"

#Start of the program ###########################################

pygame.init()

#scale and display resolution
display_scale_factor_x = 1 #display scale factor becouse original resolution is 160x90
display_scale_factor_y = 1 #display scale factor becouse original resolution is 160x90
display_width = 1200*display_scale_factor_x #this is graphics resolution, hardcoded
display_height = 600*display_scale_factor_y #this is graphics resolution, hardcoded

#screen is a pygame default window

screen = pygame.display.set_mode((display_width,display_height))

#program caption title
pygame.display.set_caption('lilypond hybride pianoroll 0.1')

#RGB colors definitions
#color_black = (0,0,0)
color_white = (255,255,255)
color_git = (77,78,80)
#
#boja_note_vani = (113, 50, 255)
#boja_note_nutra = (203, 139, 57)
#
#boja_note_povisilica_vani = (0, 255, 255)
#boja_note_povisilica_nutra = (0, 255, 255)
#
#boja_note_snizilica_vani = (255, 0, 255)
#boja_note_snizilica_nutra = (255, 0, 255)
#
#boja_pauze_vani = (0, 148, 0)
#boja_pauze_nutra = (48, 212, 0)
#
#lista_boja = [boja_note_vani, boja_note_nutra, boja_note_vani, boja_note_nutra, boja_note_vani, boja_note_nutra, boja_pauze_vani, boja_pauze_nutra]
#
##pygame clock
clock = pygame.time.Clock()
##variable which exits the program
crashed = False
#
#pic_prvi_takt = pygame.image.load('../image/prvi_takt.png')
#pic_drugi_takt = pygame.image.load('../image/drugi_takt.png')
#pic_zadnji_takt = pygame.image.load('../image/zadnji_takt.png')
#pic_plavi_okvir = pygame.image.load('../image/rub_plavi.png')
#pic_kljucevi = pygame.image.load('../image/kljucevi.png')
#pic_cursor = pygame.image.load('../image/cursor.png')
picSpriteFont = pygame.image.load('../image/tom-thumb-new.png')
picBarLine = pygame.image.load('../image/barLine.png')
picBarLines = pygame.image.load('../image/barLines.png')
picGridLine = pygame.image.load('../image/gridLine.png')
picGridDot = pygame.image.load('../image/gridDot.png')
picCursor = pygame.image.load('../image/cursor.png')
#
##loading cursor sprites into list
##cursor_color = 0
#list_sprite_cursor = []
#for i in range(0,6):
#    pic_cursor.set_clip(pygame.Rect(pozicijaSprite(i,3),0,3,7))
#    list_sprite_cursor.append(pic_cursor.subsurface(pic_cursor.get_clip()))
#
##loading letter sprites into list
listSpriteFont = []
##defining field
for column in range(0,4):
    for row in range(0, 32):
        picSpriteFont.set_clip(pygame.Rect(row*4,column*6,4,6))
        listSpriteFont.append(picSpriteFont.subsurface(picSpriteFont.get_clip()))
#
##bliting functions
##bliting of a letter
def blitFont(x, y, letter):
        screen.blit(pygame.transform.scale(listSpriteFont[letter], (4*display_scale_factor_x, 6*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a barLine
def blitBarLine(x, y):
        screen.blit(pygame.transform.scale(picBarLine, (6*display_scale_factor_x, 290*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a barLines
def blitBarLines(x, y):
        screen.blit(pygame.transform.scale(picBarLines, (208*display_scale_factor_x, 7*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a gridLine
def blitGridLine(x, y):
        screen.blit(pygame.transform.scale(picGridLine, (7*display_scale_factor_x, 290*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))

##bliting of a gridDot
def blitGridDot(x, y):
        screen.blit(pygame.transform.scale(picGridDot, (8*display_scale_factor_x, 8*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))


listCursor = []
picCursor.set_clip(pygame.Rect(0,0,5,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))
picCursor.set_clip(pygame.Rect(47,0,5,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))
picCursor.set_clip(pygame.Rect(26,0,1,52))
listCursor.append(picCursor.subsurface(picCursor.get_clip()))
#pic_cursor.set_clip(pygame.Rect(0,0,3,7))
#list_sprite_cursor.append(pic_cursor.subsurface(pic_cursor.get_clip()))

##bliting of a cursor
def blitCursor(x, y, velicina):
        #wide 5 pix
        screen.blit(pygame.transform.scale(listCursor[0], (5*display_scale_factor_x, 52*display_scale_factor_y)), (x*display_scale_factor_x, y*display_scale_factor_y))
        #should be 43 when it is big 1/4
        for i in range(int(velicina*52*4)):
            screen.blit(pygame.transform.scale(listCursor[2], (1*display_scale_factor_x, 52*display_scale_factor_y)), (i+x*display_scale_factor_x, y*display_scale_factor_y))
        #wide 5 pix
        screen.blit(pygame.transform.scale(listCursor[1], (5*display_scale_factor_x, 52*display_scale_factor_y)), ((velicina*52*4-5)+x*display_scale_factor_x, y*display_scale_factor_y))
#
base_x = 50
base_y = display_height/2
cursor_x = 0
cursor_y = 0
cursor_size = 1
timeSignature = (4, 4)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

##Keyboard buttons without MODS
        if event.type == pygame.KEYDOWN:
#            if pygame.key.get_mods() == 0:
#
#                #modes defined
#
#                #= enter chord mode
            if event.key == pygame.K_RIGHT:
                cursor_x += 52*cursor_size*timeSignature[1]
            if event.key == pygame.K_LEFT:
                cursor_x -= 52*cursor_size*timeSignature[1]
            if event.key == pygame.K_UP:
                cursor_y -= 31
            if event.key == pygame.K_DOWN:
                cursor_y += 31
#                    swap_cursor_ton = obj_cursor.ton
#                    #swap_cursor_pozicija = obj_cursor.pozicija
#                    chord_mode = 1
#                    #obj_cursor.bg_scroll_x = 0
#                    #obj_cursor.bg_scroll_y = 0
#                    #obj_cursor.pozicija = 0
#                    obj_cursor.ton = 32
#                    obj_cursor.trajanje = 15
#
#    #flipanje
    screen.fill(color_git)
    for y in range(0,4):
        for i in range(0,20):
            blitGridDot(base_x+(i*52)+(52/2),base_y-4-31+(y*62)-(62))
    for y in range(0,5):
        for i in range(0,5):
            blitBarLines(base_x+(i*208),base_y-(6/2)+(y*62)-(62*2))
    for i in range(0,5):
        if i%4 != 4:
            blitGridLine(base_x+(i*208), base_y-(290/2))
    for i in range(0,5):
        blitBarLine(base_x+(i*208*4),base_y-(290/2))

    blitCursor(base_x+cursor_x+4,base_y-(54/2)+cursor_y+2, cursor_size)

#    blit_prvi_takt(18-bg_scroll_x,bg_scroll_y-15+30)
#
#    #if drugi_takt_lijevi-bg_scroll_x < 67:
#    for i in range(0, broj_taktova):
#      blit_drugi_takt(drugi_takt_desni+i*96-bg_scroll_x,bg_scroll_y-15+30)
#
#    blit_zadnji_takt(drugi_takt_desni+broj_taktova*96-bg_scroll_x,bg_scroll_y-15+30)
#
#
#    for i in lista_nota:
#        pygame.draw.rect(screen, lista_boja[i.predikat*2], [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x)*display_scale_factor_x,(ton2Pixel(i.ton)+2+bg_scroll_y)*display_scale_factor_y,(trajanje2Pixel(i.trajanje)-1)*display_scale_factor_x,3*display_scale_factor_y] )
#        pygame.draw.rect(screen, lista_boja[i.predikat*2+1], [(pozicija2Pixel(i.pozicija)+3-bg_scroll_x)*display_scale_factor_x,(ton2Pixel(i.ton)+3+bg_scroll_y+predikati[i.predikat])*display_scale_factor_y,(trajanje2Pixel(i.trajanje)-3)*display_scale_factor_x,(3-2)*display_scale_factor_y] )
#        #show ligatures
#        if i.ligatura == True:
#            if [x for x in lista_nota if ((x.pozicija == (i.pozicija + i.trajanje + 1)) and (x.ton == i.ton) and (x.predikat == i.predikat))]:
#                pygame.draw.rect(screen, boja_note_vani, [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x+trajanje2Pixel(i.trajanje)-1)*display_scale_factor_x,(ton2Pixel(i.ton)+2+bg_scroll_y+1)*display_scale_factor_y,3*display_scale_factor_x,1*display_scale_factor_y] )
#            else:
#                pygame.draw.rect(screen, boja_note_vani, [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x+trajanje2Pixel(i.trajanje)-1)*display_scale_factor_x,(ton2Pixel(i.ton)+2+bg_scroll_y+1)*display_scale_factor_y,1*display_scale_factor_x,1*display_scale_factor_y] )
#
#    #print chordnames on the screen
#    for chord in list_chords:
#        #pygame.draw.rect(screen, lista_boja[i.predikat*2], [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y)*display_scale_factor,(trajanje2Pixel(i.trajanje)-1)*display_scale_factor,3*display_scale_factor] )
#        for i,j in enumerate(chord.ton):
#            blit_slovo((i*4)+(pozicija2Pixel(chord.pozicija)+2-bg_scroll_x),8,slovoPozicija(j))
#
#    #print markup on the screen
#    for markup in list_markup:
#        #pygame.draw.rect(screen, lista_boja[i.predikat*2], [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y)*display_scale_factor,(trajanje2Pixel(i.trajanje)-1)*display_scale_factor,3*display_scale_factor] )
#        for i,j in enumerate(markup.ton):
#            blit_slovo((i*4)+(pozicija2Pixel(markup.pozicija)+2-bg_scroll_x),79,slovoPozicija(j))
#
#    blit_cursor(pozicija2Pixel(obj_cursor.pozicija)-bg_scroll_x,ton2Pixel(obj_cursor.ton)+bg_scroll_y,pozicija2Pixel(obj_cursor.pozicija)+trajanje2Pixel(obj_cursor.trajanje)-bg_scroll_x,ton2Pixel(obj_cursor.ton)+bg_scroll_y,obj_cursor.sprite)
#
#    #show lilypond note value
#    for i,j in enumerate(kljucevi[obj_cursor.ton][0] + kljucevi[obj_cursor.ton][1] + rijecnikNotnihVrijednosti[obj_cursor.trajanje]):
#        blit_slovo((i*4)+20,90-5,slovoPozicija(j))
#
#    #show measure number
#    for i,j in enumerate("B" + str(int(obj_cursor.pozicija/16)+1+7)):
#    #for i,j in enumerate("B" + str(int(obj_cursor.pozicija/16)+1)):
#        blit_slovo((i*4)+20,0,slovoPozicija(j))
#
#    #show insert mod
#    if insert_mode:
#        for i,j in enumerate("-- INSERT --"):
#            blit_slovo((i*4)+112,90-5,slovoPozicija(j))
#
#    #show old mod
#    if old_mode:
#        for i,j in enumerate("-- OLD --"):
#            blit_slovo((i*4)+112,90-5,slovoPozicija(j))
#
#    #show old mod
#    if chord_mode:
#        for i,j in enumerate("-- CHORD --"):
#            blit_slovo((i*4)+112,90-5,slovoPozicija(j))
#
#    #show old mod
#    if markup_mode:
#    for i,letter in enumerate("Daniel debeli Kreko"): #tu denes loremIpsum varijablu
#        blitFont((i%40)*4,int(i/40)*6, spriteFont.index(letter))
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
