#!/usr/bin/env python3

import argparse
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--midiout", help="enable midi output", action="store_true")
parser.add_argument("-c", "--midiport", type=int,  help="connect to midi port")
parser.add_argument("-l", "--listmidiports",  help="list midi ports and exit", action="store_true")
parser.add_argument("-p", "--projectname",  help="project name, use *.lhp extension", type=str)
parser.add_argument('--version', action='version', version=subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8"))
args = parser.parse_args()

import pygame_sdl2 as pygame
from pygame_sdl2.locals import *
from lhpFunctions import *
import operator
import pickle #used for saving and loading projects
import math #used for scrolling screen

if args.listmidiports or args.midiport:
    args.midiout = True

if args.midiout:
    import time
    import rtmidi
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print("MIDIout enabled")

if args.listmidiports:
    for i,y in enumerate(available_ports):
        print(i+1, ":", y)
    quit()

if args.midiport:
    midiout.open_port(args.midiport-1)
    print("lhp connected to", available_ports[args.midiport-1])
elif not args.midiport and args.midiout:
    midiout.open_virtual_port("lhp")
    print("Created virtual MIDIport: lhp")

if args.projectname:
    print("Project name:", args.projectname)
    #lista_nota = pickle.load(open( args.projectname, "rb" ))

else:
    args.projectname = "save.lhp"

#Start of the program ###########################################

pygame.init()

#scale and display resolution
display_scale_factor = 8 #display scale factor becouse original resolution is 160x90
display_width = 160*display_scale_factor #this is graphics resolution, hardcoded
display_height = 90*display_scale_factor #this is graphics resolution, hardcoded

#screen is a pygame default window
screen = pygame.display.set_mode((display_width,display_height))
#program caption title
pygame.display.set_caption('lilypond 18.9.3')

#RGB colors definitions
color_black = (0,0,0)
color_white = (255,255,255)

boja_note_vani = (113, 50, 255)
boja_note_nutra = (203, 139, 57)

boja_note_povisilica_vani = (0, 255, 255)
boja_note_povisilica_nutra = (0, 255, 255)

boja_note_snizilica_vani = (255, 0, 255)
boja_note_snizilica_nutra = (255, 0, 255)

boja_pauze_vani = (0, 148, 0)
boja_pauze_nutra = (48, 212, 0)

lista_boja = [boja_note_vani, boja_note_nutra, boja_note_vani, boja_note_nutra, boja_note_vani, boja_note_nutra, boja_pauze_vani, boja_pauze_nutra]

#pygame clock
clock = pygame.time.Clock()
#variable which exits the program
crashed = False

pic_prvi_takt = pygame.image.load('../image/prvi_takt.png')
pic_drugi_takt = pygame.image.load('../image/drugi_takt.png')
pic_zadnji_takt = pygame.image.load('../image/zadnji_takt.png')
pic_plavi_okvir = pygame.image.load('../image/rub_plavi.png')
pic_kljucevi = pygame.image.load('../image/kljucevi.png')
pic_cursor = pygame.image.load('../image/cursor.png')
pic_slova = pygame.image.load('../image/slova.png')

#loading cursor sprites into list
#cursor_color = 0
list_sprite_cursor = []
for i in range(0,6):
    pic_cursor.set_clip(pygame.Rect(pozicijaSprite(i,3),0,3,7))
    list_sprite_cursor.append(pic_cursor.subsurface(pic_cursor.get_clip()))

#loading letter sprites into list
list_sprite_slova = []
#range of letters in the list
#range_slova = 24
range_slova = len(spriteSlova)
for i in range(0,range_slova):
    pic_slova.set_clip(pygame.Rect(pozicijaSprite(i,3),0,3,5))
    list_sprite_slova.append(pic_slova.subsurface(pic_slova.get_clip()))

#bliting functions
#bliting of the first bar
def blit_prvi_takt(x,y):
    screen.blit(pygame.transform.scale(pic_prvi_takt, (97*display_scale_factor, 61*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#bliting of the second bar
def blit_drugi_takt(x,y):
    screen.blit(pygame.transform.scale(pic_drugi_takt, (96*display_scale_factor, 61*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#bliting of the last bar line
def blit_zadnji_takt(x,y):
    screen.blit(pygame.transform.scale(pic_zadnji_takt, (9*display_scale_factor, 61*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#bliting the blue border
def blit_rub(x,y):
    screen.blit(pygame.transform.scale(pic_plavi_okvir, (18*display_scale_factor, 90*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#bliting of clefs
def blit_kljucevi(x,y):
    screen.blit(pygame.transform.scale(pic_kljucevi, (18*display_scale_factor, 121*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#bliting of the cursor
def blit_cursor(x_left,y_left,x_right,y_right,sprite):
    if sprite == 0:
        screen.blit(pygame.transform.scale(list_sprite_cursor[0], (3*display_scale_factor, 7*display_scale_factor)), (x_left*display_scale_factor, y_left*display_scale_factor))
        screen.blit(pygame.transform.scale(list_sprite_cursor[1], (3*display_scale_factor, 7*display_scale_factor)), (x_right*display_scale_factor, y_right*display_scale_factor))
    elif sprite == 1:
        screen.blit(pygame.transform.scale(list_sprite_cursor[2], (3*display_scale_factor, 7*display_scale_factor)), (x_left*display_scale_factor, y_left*display_scale_factor))
        screen.blit(pygame.transform.scale(list_sprite_cursor[3], (3*display_scale_factor, 7*display_scale_factor)), (x_right*display_scale_factor, y_right*display_scale_factor))
    else:
        screen.blit(pygame.transform.scale(list_sprite_cursor[4], (3*display_scale_factor, 7*display_scale_factor)), (x_left*display_scale_factor, y_left*display_scale_factor))
        screen.blit(pygame.transform.scale(list_sprite_cursor[5], (3*display_scale_factor, 7*display_scale_factor)), (x_right*display_scale_factor, y_right*display_scale_factor))

#bliting of a letter
def blit_slovo(x, y, slovo):
        screen.blit(pygame.transform.scale(list_sprite_slova[slovo%range_slova], (3*display_scale_factor, 5*display_scale_factor)), (x*display_scale_factor, y*display_scale_factor))

#cursor init
#curosr offset in pixel
trajanje_offset = 4
#cursor init in grid values
obj_cursor = cursor(0, 20, 0) #numbers are pixels in which the cursor is initialized

lista_nota = []
shift_status = 0

drugi_takt_lijevi = 115
drugi_takt_desni = 115
broj_taktova = 4

fake_scroll = 0
midi_notes = []
tempo = 120
midiplay = 0

def ajdemi():
    obj_cursor.apsolute_x = obj_cursor.pozicija - (obj_cursor.bg_scroll_x) - fake_scroll
    print("obj_cursor.apsolute_x", obj_cursor.apsolute_x)
    print("obj_cursor.pozicija", obj_cursor.pozicija)
    print("obj_cursor.bg_scroll_x", obj_cursor.bg_scroll_x)
    print("fake_scroll", fake_scroll)

#modes defined
insert_mode = 0
insert_mode_cursor_length = 0
old_mode = 0
g_mode = 0
def modes():
    return(insert_mode + old_mode + g_mode)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

#Keyboard buttons without MODS
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() == 0:

                #modes defined

                #= enter old mode
                if event.key == pygame.K_EQUALS and not modes():
                    old_mode = 1

                #i insert note before the current cursor possition
                if event.key == pygame.K_i and not modes():
                    insert_mode = 1
                    obj_cursor.trajanje = insert_mode_cursor_length

                #i insert note before the current cursor possition
                if event.key == pygame.K_g and not modes():
                    g_mode = 1

                if event.key == pygame.K_ESCAPE:
                    old_mode = 0
                    insert_mode = 0
                    g_mode = 0
                    insert_mode_cursor_length = obj_cursor.trajanje
                    obj_cursor.trajanje = 0

                #no modes keys
                if not modes():
                    if event.key in (pygame.K_RIGHT, pygame.K_l):
                        obj_cursor.pozicija += 1
                    if event.key in (pygame.K_LEFT, pygame.K_h):
                        if obj_cursor.pozicija > -15:
                            obj_cursor.pozicija -= 1
                    if event.key in (pygame.K_UP, pygame.K_k):
                        if obj_cursor.ton < 40:
                            obj_cursor.ton += 1
                    if event.key in (pygame.K_DOWN, pygame.K_j):
                        if obj_cursor.ton > 0:
                            obj_cursor.ton -= 1

                    #w: Move forward to the beginning of a word.
                    if event.key == pygame.K_w:
                        x = [ (i.pozicija,i.ton) for i in lista_nota if i.pozicija > obj_cursor.pozicija ]
                        if x:
                            obj_cursor.pozicija, obj_cursor.ton = min(x, key = lambda t: t[0])

                    #b: Move backward to the beginning of a word.
                    if event.key == pygame.K_b:
                        x = [ (i.pozicija,i.ton) for i in lista_nota if i.pozicija < obj_cursor.pozicija ]
                        if x:
                            obj_cursor.pozicija, obj_cursor.ton = max(x, key = lambda t: t[0])

                    #e: Move to the end of a word.
                    if event.key == pygame.K_e:
                        for i,y in enumerate(list(lista_nota)): #prolazi kroz sve note i broji po redu
                            if findNote(y, obj_cursor.pozicija, obj_cursor.trajanje) in (1,2):
                                obj_cursor.pozicija = y.pozicija + y.trajanje

                    #a: Append text following current cursor position
                    if event.key == pygame.K_a:
                        insert_mode = 1
                        obj_cursor.pozicija += 1

                    #o Open up a bar following the current bar and add notes there
                    if event.key == pygame.K_o:
                        insert_mode = 1
                        obj_cursor.pozicija = int(obj_cursor.pozicija / 16) * 16 + 16
                        fake_scroll = -20
                        if lista_nota:
                            for i in lista_nota:
                                if i.pozicija >= obj_cursor.pozicija:
                                    i.pozicija += 16
                        broj_taktova += 1

                    #x  delete (cut) current character
                    if event.key == pygame.K_x:
                        x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                        if x:
                            for i in x:
                                if i in lista_nota:
                                    lista_nota.remove(i)

                    #p play note as midi
                    if event.key == pygame.K_p:
                        if midiplay == 0:
                            midi_notes = [[i,time.clock(), 0] for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]

                    # testing
                    if event.key == pygame.K_y:
                        obj_cursor.apsolute_x = obj_cursor.pozicija - (obj_cursor.bg_scroll_x) - fake_scroll
                        print("obj_cursor.apsolute_x", obj_cursor.apsolute_x)
                        print("obj_cursor.pozicija", obj_cursor.pozicija)
                        print("obj_cursor.bg_scroll_x", obj_cursor.bg_scroll_x)
                        print("fake_scroll", fake_scroll)

                #insert mode
                if insert_mode:

                    if event.key == pygame.K_RIGHT:
                        obj_cursor.pozicija += 1
                    if event.key == pygame.K_LEFT:
                        if obj_cursor.pozicija > -15:
                            obj_cursor.pozicija -= 1
                    if event.key == pygame.K_UP:
                        if obj_cursor.ton < 40:
                            obj_cursor.ton += 1
                    if event.key == pygame.K_DOWN:
                        if obj_cursor.ton > 0:
                            obj_cursor.ton -= 1

                    if event.key == pygame.K_1:
                        obj_cursor.trajanje = 15
                    if event.key == pygame.K_2:
                        obj_cursor.trajanje = 7
                    if event.key == pygame.K_4:
                        obj_cursor.trajanje = 3
                    if event.key == pygame.K_8:
                        obj_cursor.trajanje = 1
                    if event.key == pygame.K_6:
                        obj_cursor.trajanje = 0
                    if event.key == pygame.K_3:
                        obj_cursor.trajanje = 1

                    if event.key == pygame.K_RETURN:
                        #if list is not empty
                        if lista_nota:
                            for i in lista_nota:
                                if i.pozicija >= obj_cursor.pozicija:
                                    i.pozicija += obj_cursor.trajanje + 1
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 0))
                            obj_cursor.pozicija += obj_cursor.trajanje + 1
                        #if list jet is empty first time only
                        else:
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 0))
                            obj_cursor.pozicija += obj_cursor.trajanje + 1

                    if event.key == pygame.K_SPACE:
                        #if list is not empty
                        if lista_nota:
                            for i in lista_nota:
                                if i.pozicija >= obj_cursor.pozicija:
                                    i.pozicija += obj_cursor.trajanje + 1
                            #lista_nota.append(dodaj_notu(obj_cursor.pozicija, 20, obj_cursor.trajanje, 3))
                            obj_cursor.pozicija += obj_cursor.trajanje + 1
                        #if list jet is empty first time only
                        else:
                            #lista_nota.append(dodaj_notu(obj_cursor.pozicija, 20, obj_cursor.trajanje, 3))
                            obj_cursor.pozicija += obj_cursor.trajanje + 1

                    if event.key == pygame.K_BACKSPACE:
                        obj_cursor.pozicija -= obj_cursor.trajanje + 1
                        x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                        if x:
                            for i in x:
                                if i in lista_nota:
                                    lista_nota.remove(i)
                        if lista_nota:
                            for i in lista_nota:
                                if i.pozicija >= obj_cursor.pozicija:
                                    i.pozicija -= obj_cursor.trajanje + 1

                    if event.key == pygame.K_DELETE:
                        x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                        if x:
                            for i in x:
                                if i in lista_nota:
                                    lista_nota.remove(i)
                        if lista_nota:
                            for i in lista_nota:
                                if i.pozicija > obj_cursor.pozicija:
                                    i.pozicija -= obj_cursor.trajanje + 1

                    #p play note as midi
                    if event.key == pygame.K_p:
                        if midiplay == 0:
                            midi_notes = [[i,time.clock(), 0] for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]



                #old mode
                if old_mode:

                    if event.key == pygame.K_RIGHT:
                        obj_cursor.pozicija += 1
                    if event.key == pygame.K_LEFT:
                        if obj_cursor.pozicija > -15:
                            obj_cursor.pozicija -= 1
                    if event.key == pygame.K_UP:
                        if obj_cursor.ton < 40:
                            obj_cursor.ton += 1
                    if event.key == pygame.K_DOWN:
                        if obj_cursor.ton > 0:
                            obj_cursor.ton -= 1

                    if event.key == pygame.K_y:
                        print(obj_cursor.apsolute_y)
                        print(obj_cursor.bg_scroll_y)


                    if event.key == pygame.K_RETURN:
                        #if list is not empty
                        if lista_nota:
                            x = [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                            #if notes in way
                            if x:
                                if ((obj_cursor.ton not in [y.ton for y in x]) and all(obj_cursor.pozicija == y.pozicija for y in x) and all(obj_cursor.trajanje == y.trajanje for y in x)):
                                    lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 0))
                                else:
                                    obj_cursor.sprite = 2
                            #if no note in way
                            else:
                                lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 0))
                        #if list jet is empty first time only
                        else:
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 0))

                    if event.key == pygame.K_1:
                        obj_cursor.trajanje = 15
                    if event.key == pygame.K_2:
                        obj_cursor.trajanje = 7
                    if event.key == pygame.K_4:
                        obj_cursor.trajanje = 3
                    if event.key == pygame.K_8:
                        obj_cursor.trajanje = 1
                    if event.key == pygame.K_6:
                        obj_cursor.trajanje = 0
                    if event.key == pygame.K_3:
                        obj_cursor.trajanje = 1

                    if event.key == pygame.K_t:
                        broj_taktova += 1

                    if event.key == pygame.K_HOME:
                      obj_cursor.bg_scroll_x = 0
                      obj_cursor.bg_scroll_y = 0
                      obj_cursor.pozicija = 0
                      obj_cursor.ton = 20

                    if event.key == pygame.K_END:
                      obj_cursor.pozicija = 16*broj_taktova
                      obj_cursor.bg_scroll_x = obj_cursor.pozicija

                    if event.key == pygame.K_PAGEUP:
                        if 0 < obj_cursor.bg_scroll_y < 8:
                            obj_cursor.bg_scroll_y = 8
                        elif obj_cursor.bg_scroll_y <= 0:
                            obj_cursor.bg_scroll_y += 8
                        obj_cursor.apsolute_y = obj_cursor.ton - 20 - (obj_cursor.bg_scroll_y)
                        if obj_cursor.apsolute_y < -12:
                            obj_cursor.ton += abs(obj_cursor.apsolute_y) - 12

                    if event.key == pygame.K_PAGEDOWN:
                        if -8 < obj_cursor.bg_scroll_y < 0:
                            obj_cursor.bg_scroll_y = -8
                        elif obj_cursor.bg_scroll_y >= 0:
                            obj_cursor.bg_scroll_y -= 8
                        obj_cursor.apsolute_y = obj_cursor.ton - 20 - (obj_cursor.bg_scroll_y)
                        if obj_cursor.apsolute_y > 12:
                            obj_cursor.ton -= abs(obj_cursor.apsolute_y) - 12

                    #adding rests
                    if event.key == pygame.K_r:
                        obj_cursor.sprite = 2
                        max_doba = (broj_taktova+1)*16
                        stepo = (16, 8, 4, 2, 1)
                        swap_cursor = (obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje)
                        obj_cursor.ton = 20
                        for step in stepo:
                          obj_cursor.trajanje = step - 1
                          if not lista_nota:
                            print("nema liste nota")
                            for pozicija in range(0, max_doba , obj_cursor.trajanje+1):
                              obj_cursor.pozicija = pozicija
                              lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 3))
                              print("dodajem notu na poziciju "+str(pozicija))
                          else:
                            for pozicija in range(0, max_doba, obj_cursor.trajanje+1):
                              obj_cursor.pozicija = pozicija
                              zastava_dodaj = 0
                              for nota in lista_nota:
                                if checkXColision(nota, obj_cursor.pozicija, obj_cursor.trajanje):
                                  zastava_dodaj += 1
                              if zastava_dodaj == 0:
                                lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 3))
                                print("dodajem notu na poziciju "+str(obj_cursor.pozicija))
                        #obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje = swap_cursor

                    if event.key == pygame.K_l:
                        print("making lilypond output")
                        text_file = open("output.ly", "w")
                        lista_nota.sort(key=operator.attrgetter('pozicija'))
                        print("\\language \"deutsch\"", file=text_file)
                        print("{", file=text_file)

                        zastava = 0
                        for nota in lista_nota:
                            if zastava > 0:
                                zastava -= 1
                            else:

                                #add bar line
                                if nota.pozicija%16 == 0 and nota.pozicija != 0:
                                    print("|", file=text_file)

                                x = [i for i in lista_nota if i.pozicija == nota.pozicija]
                                print(len(x))
                                #if chord
                                if len(x) > 1:
                                    zastava = len(x)-1
                                    print("<", end="", file=text_file)
                                    for chord_note in x:
                                        #add natural notes, predikat = 0
                                        if chord_note.predikat == 0:
                                            print(kljucevi[chord_note.ton][0] + kljucevi[chord_note.ton][1], end=" ", file=text_file)

                                        #add sharp notes, predikat = 1
                                        elif chord_note.predikat == 1:
                                            print(kljucevi[chord_note.ton][0] + "is" + kljucevi[chord_note.ton][1], end=" ", file=text_file)

                                        #add flat notes, predikat = 2
                                        elif chord_note.predikat == 2:
                                            if kljucevi[chord_note.ton][0] == "h":
                                                print("b" + kljucevi[chord_note.ton][1], end=" ", file=text_file)
                                            elif kljucevi[chord_note.ton][0] == "a":
                                                print("as" + kljucevi[chord_note.ton][1], end=" ", file=text_file)
                                            elif kljucevi[chord_note.ton][0] == "e":
                                                print( "es" + kljucevi[chord_note.ton][1], end=" ", file=text_file)
                                            else:
                                                print( kljucevi[chord_note.ton][0] + "s" + kljucevi[chord_note.ton][1], end=" ", file=text_file)
                                        #add tie by adding ~
                                        if chord_note.ligatura == True:
                                            print( "~", end=" ", file=text_file)
                                    print(">" + rijecnikNotnihVrijednosti[nota.trajanje], end=' ', file=text_file)

                                #no chord tones
                                elif len(x) == 1:
                                    #add natural notes, predikat = 0
                                    if nota.predikat == 0:
                                        print(kljucevi[nota.ton][0] + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)

                                    #add sharp notes, predikat = 1
                                    elif nota.predikat == 1:
                                        print(kljucevi[nota.ton][0] + "is" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)

                                    #add flat notes, predikat = 2
                                    elif nota.predikat == 2:
                                        if kljucevi[nota.ton][0] == "h":
                                            print("b" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                                        elif kljucevi[nota.ton][0] == "a":
                                            print("as" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                                        elif kljucevi[nota.ton][0] == "e":
                                            print( "es" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)

                                    #add rests, predikat = 3
                                    elif nota.predikat == 3:
                                        print("r" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)

                                    #add tie by adding ~
                                    if nota.ligatura == True:
                                        print( "~", end=" ", file=text_file)

                        #add bar line at the end of the file
                        print("\\bar \"|.\" }", file=text_file)
                        text_file.close()

                    if event.key == pygame.K_d:
                        x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                        if x:
                            for i in x:
                                if i in lista_nota and (obj_cursor.ton == i.ton):
                                    lista_nota.remove(i)

                    #add and remove ligature
                    if event.key == pygame.K_BACKQUOTE:
                        for i,y in enumerate(list(lista_nota)): #prolazi kroz sve note i broji po redu
                            #print(i,y.pozicija)
                            if findNote(y, obj_cursor.pozicija, obj_cursor.trajanje) in (1,2,3):
                                if lista_nota[i].ligatura == False:
                                  print("ligatura +" + str(i))
                                  lista_nota[i].ligatura=True
                                else:
                                  print("ligatura -" + str(i))
                                  lista_nota[i].ligatura=False
                                print(lista_nota[i].ligatura)

                    #split note at left cursor with added ligature
                    if event.key == pygame.K_s:
                        for i,y in enumerate(list(lista_nota)): #prolazi kroz sve note i broji po redu
                            #print(i,y.pozicija)
                            if findNote(y, obj_cursor.pozicija, obj_cursor.trajanje) in (2,3):
                                swap_trajanje = (y.pozicija + y.trajanje) - obj_cursor.pozicija
                                swap_ligatura = y.ligatura
                                y.trajanje =  obj_cursor.pozicija - y.pozicija - 1
                                y.ligatura = True
                                lista_nota.append(dodaj_notu(obj_cursor.pozicija, y.ton, swap_trajanje , y.predikat))
                                if swap_ligatura:
                                    lista_nota[-1].ligatura = True

                    #join note at left cursor with removing ligature
                    if event.key == pygame.K_j:
                        for y in lista_nota: #prolazi kroz sve note i broji po redu
                            #print(i,y.pozicija)
                            if (findNote(y, obj_cursor.pozicija, obj_cursor.trajanje) in (1,2,3)) and y.ligatura:
                                for i,x in enumerate(list(lista_nota)):
                                    if (y.pozicija + y.trajanje + 1 == x.pozicija) and (y.ton == x.ton) and (y.predikat == x.predikat):
                                        swap_trajanje = x.pozicija + x.trajanje
                                        y.trajanje = x.pozicija + x.trajanje - y.pozicija
                                        y.ligatura = x.ligatura
                                        print(i)
                                        lista_nota.pop(i)
                                        break

                    if event.key == pygame.K_c:
                        for i,y in enumerate(list(lista_nota)): #prolazi kroz sve note i broji po redu
                            #print(i,y.pozicija)
                            if findNote(y, obj_cursor.pozicija, obj_cursor.trajanje) in (2,3):
                                y.trajanje =  obj_cursor.pozicija - y.pozicija - 1

                    #p play note as midi
                    if event.key == pygame.K_p:
                        print("oj")
                        if midiplay == 1:
                            for i in midi_notes:
                                if i[2] == 1:
                                    pass
                                    #midiout.send_message([144, nota2MidiNumber(i[0]), 0])
                                    #midi_notes.remove(i)
                                    print("svira", i[0].pozicija)
                                else:
                                    midi_notes.remove(i)
                                    print("removed", i[0].pozicija)
                        elif midiplay == 0:
                            midi_notes = [[i,time.clock(), 0] for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]


                #if g_mode:
                #    if event.key == pygame.K_p:
                #        pass
                #    if event.key == pygame.K_g:
                #      obj_cursor.bg_scroll_x = 0
                #      obj_cursor.bg_scroll_y = 0
                #      obj_cursor.pozicija = 0
                #      obj_cursor.ton = 20
                #    g_mode = 0


#Keyboard buttons with LSHIFT as mod
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:

                #modes defined
                #no modes
                if not modes():
                    pass
                
                #I insert note at the beginning of the bar
                if event.key == pygame.K_i:
                    insert_mode = 1
                    obj_cursor.trajanje = insert_mode_cursor_length
                    obj_cursor.pozicija = int(obj_cursor.pozicija / 16) * 16

                #A append cursor to the end of current bar
                if event.key == pygame.K_a:
                    insert_mode = 1
                    obj_cursor.pozicija = int(obj_cursor.pozicija / 16) * 16 + 15

                #O Open up a new bar in front of the current bar and add notes there
                if event.key == pygame.K_o:
                    insert_mode = 1
                    obj_cursor.pozicija = int(obj_cursor.pozicija / 16) * 16
                    #obj_cursor.bg_scroll_x = obj_cursor.pozicija - 2
                    if lista_nota:
                        for i in lista_nota:
                            if i.pozicija >= obj_cursor.pozicija:
                                i.pozicija += 16
                    broj_taktova += 1

                if insert_mode:
                    #enlarge CURSOR.lenght by 1
                    if event.key == pygame.K_RIGHT:
                        if obj_cursor.trajanje < 15:
                            obj_cursor.trajanje += 1

                    #reduce CURSOR.lenght by 1
                    if event.key == pygame.K_LEFT:
                        if obj_cursor.trajanje > 0:
                            obj_cursor.trajanje -= 1


                if old_mode:
                    obj_cursor.sprite = 1
                    if event.key == pygame.K_RIGHT:
                            if obj_cursor.trajanje < 15:
                                obj_cursor.trajanje += 1
                    if event.key == pygame.K_LEFT:
                            if obj_cursor.trajanje > 0:
                                obj_cursor.trajanje -= 1
                    if event.key == pygame.K_t:
                        if broj_taktova > 0:
                          broj_taktova -= 1

                    #add a sharp note
                    if event.key == pygame.K_RETURN:
                        if lista_nota:
                            x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                            if x:
                                if ((obj_cursor.ton not in [y.ton for y in x]) and all(obj_cursor.pozicija == y.pozicija for y in x) and all(obj_cursor.trajanje == y.trajanje for y in x)):
                                    lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 1))
                                else:
                                    obj_cursor.sprite = 2
                            else:
                                lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 1))
                        else:
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 1))

#Keyboard buttons with LCTRL as mod
            if ((pygame.key.get_mods() & pygame.KMOD_LCTRL)):

                if not modes():

                    #save project to file
                    if event.key == pygame.K_s:
                        pickle.dump(lista_nota, open( args.projectname, "wb" ))
                        print("save")

                    #load project from file
                    if event.key == pygame.K_l:
                        lista_nota = pickle.load(open( args.projectname, "rb" ))
                        print("load")

                if old_mode:
                    obj_cursor.sprite = 1
                    if event.key == pygame.K_RIGHT:
                            if obj_cursor.trajanje > 0:
                                obj_cursor.trajanje -= 1
                                obj_cursor.pozicija += 1
                    if event.key == pygame.K_LEFT:
                            if obj_cursor.trajanje < 16:
                                obj_cursor.trajanje += 1
                                obj_cursor.pozicija -= 1

                    if event.key == pygame.K_RETURN:
                        if lista_nota:
                            x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                            if x:
                                if ((obj_cursor.ton not in [y.ton for y in x]) and all(obj_cursor.pozicija == y.pozicija for y in x) and all(obj_cursor.trajanje == y.trajanje for y in x)):
                                    lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 2))
                                else:
                                    obj_cursor.sprite = 2
                            else:
                                lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 2))
                        else:
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 2))

                    #remove all notes under the cursor
                    if event.key == pygame.K_d:
                        x =  [i for i in lista_nota if findNote(i,obj_cursor.pozicija, obj_cursor.trajanje)]
                        if x:
                            for i in x:
                                if i in lista_nota:
                                    lista_nota.remove(i)

#Keyboard buttons with LALT as mod
            if pygame.key.get_mods() & pygame.KMOD_LALT:

                if not modes():
                    pass

                if old_mode:
                    obj_cursor.sprite = 1
                    if event.key == pygame.K_UP:
                        if obj_cursor.bg_scroll_y < 8:
                            obj_cursor.bg_scroll_y +=1
                            obj_cursor.ton +=1
                    if event.key == pygame.K_DOWN:
                        if obj_cursor.bg_scroll_y > -8:
                            obj_cursor.bg_scroll_y -=1
                            obj_cursor.ton -=1
                    if event.key == pygame.K_LEFT:
                        obj_cursor.bg_scroll_x -=1
                    if event.key == pygame.K_RIGHT:
                        obj_cursor.bg_scroll_x +=1

                if event.key == pygame.K_f:
                    #print("obj_cursor.ton", obj_cursor.ton)
                    print("obj_cursor.ton", obj_cursor.ton)
                    print("obj_cursor.pozicija", obj_cursor.pozicija)
                    print("obj_cursor.bg_scroll_x", obj_cursor.bg_scroll_x)
                    print("obj_cursor.bg_scroll_y", obj_cursor.bg_scroll_y)
                    print("obj_cursor.apsolute_x", obj_cursor.apsolute_x)
                    print("obj_cursor.apsolute_y", obj_cursor.apsolute_y)
                    print("---------------------")


        if event.type == pygame.KEYUP:
            if pygame.key.get_mods()==0 & pygame.KMOD_LSHIFT:
                obj_cursor.sprite = 0
                #shift_status = 0
                #left = 0
                #right = 0

# playing midi notes ###############################################################
    if midi_notes:
        midiplay = 1
        swap_pozicija = obj_cursor.pozicija
        for i in midi_notes:
            start_point = (i[0].pozicija - swap_pozicija)*(60/tempo/4) + i[1]
            #print(start_point, end_point)
            end_point = (i[0].pozicija - swap_pozicija + i[0].trajanje + 1)*(60/tempo/4) + i[1]
            if (i[2] == 0 and (time.clock() >= start_point)):
                    i[2] = 1
                    print(str(nota2MidiNumber(i[0])) + " on")
                    midiout.send_message([144, nota2MidiNumber(i[0]), 100])
                    #print(time.clock())
            if (i[2] == 1 and (time.clock() >= end_point)):
                    print(str(nota2MidiNumber(i[0])) + " off")
                    midiout.send_message([144, nota2MidiNumber(i[0]), 0])
                    midi_notes.remove(i)
    else:
        midiplay = 0


# bliting #########################################################################

    #racunanje bg_scroll-a
    #pozicija cursora u svakom trenutku ovisno na okvir screen-a
    obj_cursor.apsolute_y = obj_cursor.ton - 20 - (obj_cursor.bg_scroll_y)
    obj_cursor.apsolute_x = obj_cursor.pozicija - (obj_cursor.bg_scroll_x) - fake_scroll


    if (int(obj_cursor.apsolute_x) - int(abs(fake_scroll))) == 2:
        fake_scroll = 0

    if obj_cursor.apsolute_y > 12:
        obj_cursor.bg_scroll_y += 1
    elif obj_cursor.apsolute_y < -12:
        obj_cursor.bg_scroll_y -= 1

    if obj_cursor.apsolute_x < 0:
        #obj_cursor.bg_scroll_x -=1
        x = (obj_cursor.apsolute_x - 1)
        obj_cursor.bg_scroll_x -= round(math.log(abs(x))*0.6, 1)
        ajdemi()
    elif obj_cursor.apsolute_x + obj_cursor.trajanje > 22:
        x = (obj_cursor.apsolute_x + obj_cursor.trajanje - 21)
        obj_cursor.bg_scroll_x += round(math.log(x)*0.6, 1)
        #print(round(x, 1))
        ajdemi()

    bg_scroll_x = obj_cursor.bg_scroll_x * 6
    bg_scroll_y = obj_cursor.bg_scroll_y * 3

    #flipanje
    screen.fill(color_white)
    blit_prvi_takt(18-bg_scroll_x,bg_scroll_y-15+30)

    #if drugi_takt_lijevi-bg_scroll_x < 67:
    for i in range(0, broj_taktova):
      blit_drugi_takt(drugi_takt_desni+i*96-bg_scroll_x,bg_scroll_y-15+30)

    blit_zadnji_takt(drugi_takt_desni+broj_taktova*96-bg_scroll_x,bg_scroll_y-15+30)


    for i in lista_nota:
        pygame.draw.rect(screen, lista_boja[i.predikat*2], [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y)*display_scale_factor,(trajanje2Pixel(i.trajanje)-1)*display_scale_factor,3*display_scale_factor] )
        pygame.draw.rect(screen, lista_boja[i.predikat*2+1], [(pozicija2Pixel(i.pozicija)+3-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+3+bg_scroll_y+predikati[i.predikat])*display_scale_factor,(trajanje2Pixel(i.trajanje)-3)*display_scale_factor,(3-2)*display_scale_factor] )
        #show ligatures
        if i.ligatura == True:
            if [x for x in lista_nota if ((x.pozicija == (i.pozicija + i.trajanje + 1)) and (x.ton == i.ton) and (x.predikat == i.predikat))]:
                pygame.draw.rect(screen, boja_note_vani, [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x+trajanje2Pixel(i.trajanje)-1)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y+1)*display_scale_factor,3*display_scale_factor,1*display_scale_factor] )
            else:
                pygame.draw.rect(screen, boja_note_vani, [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x+trajanje2Pixel(i.trajanje)-1)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y+1)*display_scale_factor,1*display_scale_factor,1*display_scale_factor] )



    blit_cursor(pozicija2Pixel(obj_cursor.pozicija)-bg_scroll_x,ton2Pixel(obj_cursor.ton)+bg_scroll_y,pozicija2Pixel(obj_cursor.pozicija)+trajanje2Pixel(obj_cursor.trajanje)-bg_scroll_x,ton2Pixel(obj_cursor.ton)+bg_scroll_y,obj_cursor.sprite)

    #show lilypond note value
    for i,j in enumerate(kljucevi[obj_cursor.ton][0] + kljucevi[obj_cursor.ton][1] + rijecnikNotnihVrijednosti[obj_cursor.trajanje]):
        blit_slovo((i*4)+20,90-5,slovoPozicija(j))

    #show measure number
    for i,j in enumerate("B" + str(int(obj_cursor.pozicija/16)+1)):
        blit_slovo((i*4)+20,0,slovoPozicija(j))

    #show insert mod
    if insert_mode:
        for i,j in enumerate("-- INSERT --"):
            blit_slovo((i*4)+112,90-5,slovoPozicija(j))

    #show old mod
    if old_mode:
        for i,j in enumerate("-- OLD --"):
            blit_slovo((i*4)+112,90-5,slovoPozicija(j))

    ##show visual mod
    #if visual_mode:
    #    for i,j in enumerate("-- VISUAL --"):
    #        blit_slovo((i*4)+112,90-5,slovoPozicija(j))

    #plavi okvir
    blit_kljucevi(0,-15+bg_scroll_y)
    blit_rub(0,0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()
