#!/usr/bin/env python3

import pygame_sdl2 as pygame
from pygame_sdl2.locals import *
from korisneFunkcije import *
import operator

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
boja_note_nutra = (0, 0, 255)

boja_note_povisilica_vani = (0, 255, 255)
boja_note_povisilica_nutra = (0, 255, 255)

boja_note_snizilica_vani = (255, 0, 255)
boja_note_snizilica_nutra = (255, 0, 255)

boja_pauze_vani = (0, 148, 0)
boja_pauze_nutra = (48, 212, 0)

lista_boja = [boja_note_vani, boja_note_nutra, boja_note_povisilica_vani, boja_note_povisilica_nutra, boja_note_snizilica_vani, boja_note_snizilica_nutra, boja_pauze_vani, boja_pauze_nutra]

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
range_slova = 19
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
bg_scroll_x = 0
bg_scroll_y = 0

drugi_takt_lijevi = 115
drugi_takt_desni = 115
broj_taktova = 4

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() == 0:
                if event.key == pygame.K_RIGHT:
                    if obj_cursor.pozicija == 22:
                      bg_scroll_x += 6
                    else:
                      obj_cursor.pozicija += 1
                if event.key == pygame.K_LEFT:
                    if obj_cursor.pozicija == 0:
                      bg_scroll_x -= 6
                    else:
                      obj_cursor.pozicija -= 1
                if event.key == pygame.K_UP:
                    if obj_cursor.ton == 32 and pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y)<40: #spusta bg ako cursor dojde do margine
                      bg_scroll_y +=3  
                    else:
                      if(pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y))<40:
                        obj_cursor.ton += 1
                if event.key == pygame.K_DOWN:
                    if obj_cursor.ton == 8 and pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y)>0:
                      bg_scroll_y -=3
                    else:
                      if(pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y))>0:
                        obj_cursor.ton -= 1
                if event.key == pygame.K_RETURN:
                    if lista_nota:
                        zastava_return = 0 #zastava je zbog brisanja iz liste
                        for i in lista_nota:
                            if checkXColision(i,pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), obj_cursor.trajanje):
                                zastava_return += 1
                        if zastava_return:
                            obj_cursor.sprite = 2
                        else:
                            lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 0))
                    else:
                        lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 0))
                        #lista_nota.append(nota(obj_cursor.pozicija+pixel2Pozicija(bg_scroll_x), obj_cursor.ton-pixel2Ton(bg_scroll_y), obj_cursor.trajanje, 0))
                #if event.key == pygame.K_DELETE:

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
                  bg_scroll_x = 0
                  bg_scroll_y = 0
                  obj_cursor.pozicija = 0
                  obj_cursor.ton = 20
                if event.key == pygame.K_END:
                  bg_scroll_x = 96*broj_taktova
                  obj_cursor.pozicija = 0
                  #obj_cursor.ton = 19
                if event.key == pygame.K_PAGEUP:
                  bg_scroll_x += 96
                if event.key == pygame.K_PAGEDOWN:
                  bg_scroll_x -= 96
                if event.key == pygame.K_f:
                    print(pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y))
                if event.key == pygame.K_a:
                    obj_cursor.sprite = 2
                    #print(kljucevi[pixel2Ton(cursor.y_left)%27])
                    #print(slovoPozicija(removeLily(kljucevi[pixel2Ton(cursor.y_left)%27])))
                    #print(obj_cursor.trajanje)
                    #print(obj_cursor.pozicija)
                    #print(obj_cursor.ton)
                    #print(ton2Pixel(obj_cursor.ton))
                    #print(pixel2Ton(ton2Pixel(obj_cursor.ton)))
                    #print(ton2Pixel(pixel2Ton(ton2Pixel(obj_cursor.ton))))
                    #print("Y:" + str(cursor.y_left))
                    #print("BG:" + str(bg_scroll_y))
                    #print(pixel2Pozicija(cursor.x_left+bg_scroll_x))
                    #print(pixel2Ton(cursor.y_left))
                    #print(pixel2RezolucijaTrajanja(obj_cursor.trajanje))
                    #print(lista_nota)

                    #for i in lista_nota:
                    #    print(i.pozicija, i.ton, i.trajanje)
                    #print()
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
                          #blit_cursor(pozicija2Pixel(obj_cursor.pozicija),ton2Pixel(obj_cursor.ton),pozicija2Pixel(obj_cursor.pozicija)+trajanje2Pixel(obj_cursor.trajanje),ton2Pixel(obj_cursor.ton),obj_cursor.sprite)
                          #pygame.display.flip()
                          #input()
                      else:
                        for pozicija in range(0, max_doba, obj_cursor.trajanje+1):
                          obj_cursor.pozicija = pozicija
                          zastava_dodaj = 0
                          for nota in lista_nota:
                            #blit_cursor(pozicija2Pixel(obj_cursor.pozicija),ton2Pixel(obj_cursor.ton),pozicija2Pixel(obj_cursor.pozicija)+trajanje2Pixel(obj_cursor.trajanje),ton2Pixel(obj_cursor.ton),obj_cursor.sprite)
                            #pygame.display.flip()
                            #input("nota: " + str(nota.pozicija) + ", cursor_pozicija: " + str(obj_cursor.pozicija) +  ", trajanje: " + str( obj_cursor.trajanje ))
                            if checkXColision(nota, obj_cursor.pozicija, obj_cursor.trajanje):
                              zastava_dodaj += 1
                          if zastava_dodaj == 0:
                            lista_nota.append(dodaj_notu(obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje, 3))
                            print("dodajem notu na poziciju "+str(obj_cursor.pozicija))
                    obj_cursor.pozicija, obj_cursor.ton, obj_cursor.trajanje = swap_cursor

                if event.key == pygame.K_c:
                  text_file = open("output.ly", "w")
                  lista_nota.sort(key=operator.attrgetter('pozicija'))
                  print("{", file=text_file)
                  for nota in lista_nota:
                    if nota.pozicija%16 == 0 and nota.pozicija != 0:
                      print("|", file=text_file)
                    #predikat = 0
                    if nota.predikat == 0:
                      print(kljucevi[nota.ton][0] + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                    #predikat = 1, aka povisilica
                    elif nota.predikat == 1:
                      print(kljucevi[nota.ton][0] + "is" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                    #predikat = 2, aka snizilica
                    elif nota.predikat == 2:
                      if kljucevi[nota.ton][0] == "h":
                        print("b" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                      elif kljucevi[nota.ton][0] == "a":
                        print("as" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                      elif kljucevi[nota.ton][0] == "e":
                        print( "es" + kljucevi[nota.ton][1]  + "" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                    elif nota.predikat == 3:
                      print("r" + rijecnikNotnihVrijednosti[nota.trajanje], end=" ", file=text_file)
                  print("\\bar \"|.\" }", file=text_file)
                  text_file.close()

                if event.key == pygame.K_d:
                    zastava_delete=0
                    for i,y in enumerate(list(lista_nota)):
                        #print(i,y.pozicija)
                        if brisiNotu(y, pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), obj_cursor.trajanje):
                            print("brisi" + str(i))
                            lista_nota.pop(i-zastava_delete)
                            zastava_delete +=1

            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                obj_cursor.sprite = 1
                if event.key == pygame.K_RIGHT:
                        if obj_cursor.trajanje < 16:
                            obj_cursor.trajanje += 1
                if event.key == pygame.K_LEFT:
                        if obj_cursor.trajanje > 0:
                            obj_cursor.trajanje -= 1
                if event.key == pygame.K_t:
                    if broj_taktova > 0:
                      broj_taktova -= 1
                if event.key == pygame.K_RETURN:
                    if lista_nota:
                        zastava_return = 0 #zastava je zbog brisanja iz liste
                        for i in lista_nota:
                            if checkXColision(i,pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), obj_cursor.trajanje):
                                zastava_return += 1
                        if zastava_return:
                            obj_cursor.sprite = 2
                        else:
                            lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 1))
                    else:
                        lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 1))
            if ((pygame.key.get_mods() & pygame.KMOD_LCTRL)):
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
                        zastava_return = 0 #zastava je zbog brisanja iz liste
                        for i in lista_nota:
                            if checkXColision(i,pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), obj_cursor.trajanje):
                                zastava_return += 1
                        if zastava_return:
                            obj_cursor.sprite = 2
                        else:
                            lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 2))
                    else:
                        lista_nota.append(dodaj_notu(pixel2Pozicija(pozicija2Pixel(obj_cursor.pozicija)+bg_scroll_x), pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y), obj_cursor.trajanje, 2))
            if pygame.key.get_mods() & pygame.KMOD_LALT:
                obj_cursor.sprite = 1
                if event.key == pygame.K_UP:
                    print("LALT+K_UP")
                    bg_scroll_y +=3
                if event.key == pygame.K_DOWN:
                    print("LALT+K_DOWN")
                    bg_scroll_y -=3
                if event.key == pygame.K_LEFT:
                    print("LALT+K_LEFT")
                    bg_scroll_x -=6
                if event.key == pygame.K_RIGHT:
                    print("LALT+K_RIGHT")
                    bg_scroll_x +=6
             #FETISH CURSOR LEFT RIGHT
#            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
#                cursor_color = 1
#                print("SHIFT")
#                shift_status = 1
#                if event.key == pygame.K_RIGHT:
#                    if ((left == 0) & (right == 0)):
#                        right = 1
#                    if ((left == 0) & (right == 1)): #right mod
#                        obj_cursor.trajanje += 6
#                    if ((left == 1) & (right == 0)): #left mod
#                        obj_cursor.trajanje -= 6
#                        cursor.x_left += 6
#                if event.key == pygame.K_LEFT:
#                    if ((left == 0) & (right == 0)):
#                        left = 1
#                    if ((left == 0) & (right == 1)):#right mod
#                        obj_cursor.trajanje -= 6
#                    if ((left == 1) & (right == 0)):#left mod
#                        obj_cursor.trajanje += 6
#                        cursor.x_left -=6
        if event.type == pygame.KEYUP:
            if pygame.key.get_mods()==0 & pygame.KMOD_LSHIFT:
                obj_cursor.sprite = 0
                #shift_status = 0
                #left = 0
                #right = 0

    #flipanje
    screen.fill(color_white)
    blit_prvi_takt(18-bg_scroll_x,bg_scroll_y-15+30)

    #if drugi_takt_lijevi-bg_scroll_x < 67:
    for i in range(0, broj_taktova):
      blit_drugi_takt(drugi_takt_desni+i*96-bg_scroll_x,bg_scroll_y-15+30)

    blit_zadnji_takt(drugi_takt_desni+broj_taktova*96-bg_scroll_x,bg_scroll_y-15+30)


    for i in lista_nota:
        pygame.draw.rect(screen, lista_boja[i.predikat*2], [(pozicija2Pixel(i.pozicija)+2-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+2+bg_scroll_y)*display_scale_factor,(trajanje2Pixel(i.trajanje)-1)*display_scale_factor,3*display_scale_factor] )
        pygame.draw.rect(screen, lista_boja[i.predikat*2+1], [(pozicija2Pixel(i.pozicija)+3-bg_scroll_x)*display_scale_factor,(ton2Pixel(i.ton)+3+bg_scroll_y)*display_scale_factor,(trajanje2Pixel(i.trajanje)-3)*display_scale_factor,(3-2)*display_scale_factor] )

    blit_cursor(pozicija2Pixel(obj_cursor.pozicija),ton2Pixel(obj_cursor.ton),pozicija2Pixel(obj_cursor.pozicija)+trajanje2Pixel(obj_cursor.trajanje),ton2Pixel(obj_cursor.ton),obj_cursor.sprite)

    for i,j in enumerate(kljucevi[pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y)][0] + kljucevi[pixel2Ton(ton2Pixel(obj_cursor.ton)-bg_scroll_y)][1] + rijecnikNotnihVrijednosti[obj_cursor.trajanje]):
        blit_slovo((i*4)+20,90-5,slovoPozicija(j))

    #plavi okvir
    blit_kljucevi(0,-15+bg_scroll_y)
    blit_rub(0,0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()