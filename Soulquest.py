import pygame
import sys
import openai
from openai import OpenAI
import requests
import io
from PIL import Image
import re
import os
import json
# Configura tu clave de API
openai.api_key = 'sk-proj-TVFfuaFUBlEVrcpLnRQVT3BlbkFJXs4vSSz0CP1NLl8DbzDe'
# Configuración del cliente OpenAI
client = OpenAI(api_key='sk-proj-TVFfuaFUBlEVrcpLnRQVT3BlbkFJXs4vSSz0CP1NLl8DbzDe')
# Inicializa Pygame
pygame.init()
pygame.mixer.init()
# Cambia el título de la ventana
pygame.display.set_caption("Soulquest")
# Carga el icono de la ventana
icon = pygame.image.load("icono.jpg")  # Reemplaza "icono.png" con la ruta de tu archivo de icono
pygame.display.set_icon(icon)
#inicializa el reloj
clock = pygame.time.Clock()
# Define los colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Define la fuente y el tamaño del texto
font = pygame.font.Font('Monocraft.ttf',30)
class Data:
    def _init_(self):
        self.prompt_text = ""
        self.prompt_text1=""
        self.playerName = ""
        self.wrapped_text=""
        self.parte2=""
        self.Respuesta=[]
        self.options_list=[]
        self.reactivos=[]
        self.screen_width = 0
        self.screen_height = 0
        self.correcto=0
        self.error=0
        self.Pregunta=0
        self.Hist=0
        self.audio_once = pygame.mixer.Sound('D:\Soulquest\beep.mp3')
        self.audio_loop=pygame.mixer.Sound('aprendizaje musica.mp3')
        self.historia=""
        self.matematicas=""
        self.español=""
        self.ingles=""
        self.educacionfisica=""
        self.materia=0
        self.image=""
def main(data):
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    # Define la pantalla para el resiza
    option12 = ["Modo aprendizaje","Modo historia","Guardar y Salir"]
    option1=0
    a=True
    previous_eje = 0
    data.audio_loop.stop()
    button_2_pressed = False
    Imagen= pygame.image.load("inicio.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        for event in pygame.event.get():
            if joystick_count>0:
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        button_2_pressed = False
                # Lectura de los ejes del joystick
                eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
        # Comprobamos si el eje ha cruzado el umbral desde el estado previo
                if eje >= .9 and previous_eje < .9:
                    option1 = (option1 + 1) % len(option12)
                elif eje <= -1 and previous_eje > -1:
                    option1 = (option1 - 1) % len(option12)
                if joystick.get_button(0)==1 and button_2_pressed == False:
                    print("Opción seleccionada:", option12[option1])
                    if option12[option1]=="Modo historia":
                        if data.Hist==1:
                            print("hola")
                            text(data)
                        history(data)
                    if option12[option1]=="Modo aprendizaje":
                        if data.Pregunta>0:
                            preguntas(data)
                        Materias(data)
                    if option12[option1]=="Guardar y salir":
                        guardar(data)
        # Actualizamos el estado previo del eje
                previous_eje = eje
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   option1 = (option1 - 1) % len(option12)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   option1 = (option1 + 1) % len(option12)
               elif event.key == pygame.K_RETURN:
                   print("Opción seleccionada:", option12[option1])
                   if option12[option1]=="Modo historia":
                       if data.Hist>0:
                           load2(data)
                       else:
                           load3(data)
                   if option12[option1]=="Modo aprendizaje":
                       data.audio_loop = pygame.mixer.Sound('aprendizaje musica.mp3')
                       data.audio_loop.set_volume(0.2)  # Ajusta el volumen del audio en loop a 50%
                       data.audio_loop.play(loops=-1)  # `loops=-1` indica que debe reproducirse en loop infinito
                       if data.Pregunta>0:
                           preguntas(data)
                       else:
                        Materias(data)
                   if option12[option1]=="Guardar y Salir":
                       guardar(data)
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface=font.render('Selecciona un Modo de Juego',False,'white')
        text_width1, text_height1 = text_surface.get_size()
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_surface, (text_x, text_y-240))
        for i, option in enumerate(option12):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=(text_x,(text_y+100) + i * 80))
            screen.blit(class_surface, class_rect)

        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=(text_x-30,(text_y+100) + option1 * 80))
        screen.blit(arrow_surface, arrow_rect)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
def load3(data):
        # Define la pantalla para el resiza
        screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
        Imagen= pygame.image.load("inicio.jpeg")
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface3=font.render('Cargando...',False,'white')
        screen.blit(text_surface3, ( data.screen_width // 2+250,  data.screen_height//2+300))
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
        history(data)
def history(data):
    data.audio_loop = pygame.mixer.Sound('overworld-theme.mp3')
    data.audio_loop.set_volume(0.2)  # Ajusta el volumen del audio en loop a 50%
    data.audio_loop.play(loops=-1)  # `loops=-1` indica que debe reproducirse en loop infinito
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    previous_eje=0
    previous_eje1=0
    # Variables para entrada de texto
    text = ""
    # Define el cuadro de texto
    color_inactive = pygame.Color('dodgerblue2')
    color = color_inactive
    test_surface=pygame.Surface((800,600))
    test_surfacex,test_surfacey=test_surface.get_size()
    text_surface=font.render('Ingresa tu nombre Aventurer@',False,'white')
    text_width1, text_height1 = text_surface.get_size()
    a=True
    KEY_WIDTH = 50
    KEY_HEIGHT = 50
    # Índices de la tecla actualmente seleccionada
    selected_row = 0
    selected_col = 0
    button_2_pressed = False
    Imagen= pygame.image.load("historia.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        # Definir las teclas y sus posiciones en una cuadrícula
        keys = [
            {'char': 'Q', 'x':((data.screen_width-450) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 0},
            {'char': 'W', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 1},
            {'char': 'E', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 2},
            {'char': 'R', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 3},
            {'char': 'T', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 4},
            {'char': 'Y', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 5},
            {'char': 'U', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 6},
            {'char': 'I', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 7},
            {'char': 'O', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 8},
            {'char': 'P', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 0},
            {'char': 'A', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 1},
            {'char': 'S', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 2},
            {'char': 'D', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 3},
            {'char': 'F', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 4},
            {'char': 'G', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 5},
            {'char': 'H', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 6},
            {'char': 'J', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 7},
            {'char': 'K', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 8},
            {'char': 'L', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 0},
            {'char': 'Ñ', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 1},
            {'char': 'Z', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 2},
            {'char': 'X', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 3},
            {'char': 'C', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 4},
            {'char': 'V', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 5},
            {'char': 'B', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 6},
            {'char': 'N', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 7},
            {'char': 'M', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 8},
            {'char': 'DEL', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 0},  # Botón de retroceso
            {'char': 'GO', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 1},
            # Añadir más teclas según sea necesario
        ]
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
            eje1=joystick.get_axis(0)
       # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.9 and previous_eje < 0.9:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'down')
            elif eje <= -1 and previous_eje > -1:
                 selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'up')
            elif eje1 >= .9 and previous_eje1 < 0.9:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'right')
            elif eje1 <= -1 and previous_eje1 > -1:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'left')

            previous_eje=eje
            previous_eje1=eje1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            elif joystick_count>0:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 and not button_2_pressed:
                        key = get_key_at_position(selected_row, selected_col)
                        if key:
                            if key["char"] == "DEL":
                                text = text[:-1]  # Borra el último carácter
                            if key["char"]=="GO":
                               data.prompt_text+= "Nombre: "+text
                               print("Nombre del jugador:", text)
                               raza(data)
                            else:
                               text += key["char"]
                               button_2_pressed = True
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        button_2_pressed = False
            if event.type == pygame.KEYDOWN:
                    data.audio_once.play()
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'left')
                    elif  event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'right')
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'up')
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'down')
                    elif event.key == pygame.K_RETURN:
                        key = get_key_at_position(selected_row, selected_col)
                        if key:
                            if key["char"]=="DEL":
                                text = text[:-1]  # Borra el último carácter
                            elif key["char"]=="GO":
                                data.playerName=text
                                print("Nombre del jugador:", text)
                                raza(data)
                            else:
                                text += key["char"]
        screen.blit(Imagen, ( 0,0))
        input_box = pygame.Rect(((data.screen_width-300) // 2), ((data.screen_height -200) // 2), 300, 60)
        # Renderiza el texto ingresado por el usuario
        rendered_text = font.render(text, False, WHITE)
        text_width = rendered_text.get_width()
        # Ajusta el texto al ancho del cuadro de texto
        text_rendered = rendered_text if text_width < input_box.width else font.render(text[-13:], False, WHITE)
        # Dibuja el cuadro de texto
        pygame.draw.rect(screen, color, input_box, 2)
        # Dibuja el texto en el cuadro de texto
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_rendered, (input_box.x + 5, input_box.y+15))
        screen.blit(text_surface, (text_x, text_y-150))
        for key in keys:
            rect = pygame.Rect(key['x'], key['y'], KEY_WIDTH, KEY_HEIGHT)
            color = 'RED' if key['row'] == selected_row and key['col'] == selected_col else WHITE
            pygame.draw.rect(screen, color, rect)
            texto = font.render(key['char'], True, BLACK)
            texto_rect = texto.get_rect(center=(key['x'] + KEY_WIDTH // 2, key['y'] + KEY_HEIGHT // 2))
            screen.blit(texto, texto_rect)
        pygame.display.flip()
        clock.tick(30)
def move_selection(selected_row, selected_col, keys, direction):
    max_row =  max(key['row'] for key in keys if key['col'] == selected_col)
    max_col = max(key['col'] for key in keys if key['row'] == selected_row)
    if direction == 'left':
        selected_col -= 1
        if selected_col < 0:
            selected_col = max_col
    elif direction == 'right':
        selected_col = (selected_col + 1) % (max_col + 1)
    elif direction == 'up':
        selected_row -= 1
        if selected_row < 0:
            selected_row = max_row
    elif direction == 'down':
        selected_row = (selected_row + 1) % (max_row + 1)

    return selected_row, selected_col
 # Función para obtener la tecla en una posición de la cuadrícula
def get_key_at_position(row, col):
    keys = [
        {'char': 'Q', 'x':((data.screen_width-450) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 0},
        {'char': 'W', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 1},
        {'char': 'E', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 2},
        {'char': 'R', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 3},
        {'char': 'T', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 4},
        {'char': 'Y', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 5},
        {'char': 'U', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 6},
        {'char': 'I', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 7},
        {'char': 'O', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 8},
        {'char': 'P', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 0},
        {'char': 'A', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 1},
        {'char': 'S', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 2},
        {'char': 'D', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 3},
        {'char': 'F', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 4},
        {'char': 'G', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 5},
        {'char': 'H', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 6},
        {'char': 'J', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 7},
        {'char': 'K', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 8},
        {'char': 'L', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 0},
        {'char': 'Ñ', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 1},
        {'char': 'Z', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 2},
        {'char': 'X', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 3},
        {'char': 'C', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 4},
        {'char': 'V', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 5},
        {'char': 'B', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 6},
        {'char': 'N', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 7},
        {'char': 'M', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 8},
        {'char': 'DEL', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 0},  # Botón de retroceso
        {'char': 'GO', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 1},
        # Añadir más teclas según sea necesario
    ]
    for key in keys:
        if key['row'] == row and key['col'] == col:
            return key
    return None
def raza(data):
    a=True
    options = ["Elfo", "Humano", "Enano", "Dragonborn"]
    selected_option = 0
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    previous_eje=0
    button_2_pressed = False
    Imagen= pygame.image.load("historia.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
       Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
       joystick_count=pygame.joystick.get_count()
       if joystick_count>0:
           joystick = pygame.joystick.Joystick(0)
           joystick.init()
           eje = joystick.get_axis(1)
           if eje <= -1 and previous_eje > -1:
               selected_option = (selected_option - 1) % len(options)
           if eje >= 0.9 and previous_eje < 0.9:
               selected_option = (selected_option + 1) % len(options)
           previous_eje =eje
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
              pygame.quit()
           if event.type == pygame.VIDEORESIZE:
       # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
               screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
               data.screen_width, data.screen_height = event.w, event.h
           if joystick_count>0:
               if event.type == pygame.JOYBUTTONDOWN:
                   if event.button == 0 and not button_2_pressed:
                       button_2_pressed = True
                       print("Opción seleccionada:", options[selected_option])
                       if options[selected_option]=="Elfo":
                           data.prompt_text+= " y su raza es Elfo"
                           load(data)
                       if options[selected_option]=="Humano":
                           data.prompt_text+= " y su raza es Humano"
                           load(data)
                       if options[selected_option]=="Enano":
                           data.prompt_text+= " y su raza es Enano"
                           load(data)
                       if options[selected_option]=="Dragonborn":
                           data.prompt_text+= " y su raza es Dragonborn"
                           load(data)
               if event.type == pygame.JOYBUTTONUP:
                   if event.button == 0:
                       button_2_pressed = False
           if event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP :
                   selected_option = (selected_option - 1) % len(options)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN :
                   selected_option = (selected_option + 1) % len(options)
               elif event.key == pygame.K_RETURN :
                   print("Opción seleccionada:", options[selected_option])
                   if options[selected_option]=="Elfo":
                       data.prompt_text+= " y su raza es Elfo"
                       load(data)
                   if options[selected_option]=="Humano":
                       data.prompt_text+= " y su raza es Humano"
                       load(data)
                   if options[selected_option]=="Enano":
                       data.prompt_text+= " y su raza es Enano"
                       load(data)
                   if options[selected_option]=="Dragonborn":
                       data.prompt_text+= " y su raza es Dragonborn"
                       load(data)
       screen.blit(Imagen, ( 0,0))
       color_rectangulo = (0, 0, 0, 128)
       surface = pygame.Surface((1038,352), pygame.SRCALPHA)
       surface.fill(color_rectangulo)
       screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
       surface = pygame.Surface((988,322), pygame.SRCALPHA)
       surface.fill(color_rectangulo)
       screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
       for i, option in enumerate(options):
           class_surface = font.render(option, False, WHITE)
           class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-70,(( data.screen_height//2)+50) + i * 50))
           screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
       arrow_surface = font.render("->", False, WHITE)
       arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2 - 100,(( data.screen_height//2)+50) + selected_option * 50))
       screen.blit(arrow_surface, arrow_rect)
       text_surface=font.render('Selecciona una raza',False,'white')
       text_width1, text_height1 = text_surface.get_size()
       text_x = ( data.screen_width - text_width1) // 2
       text_y = ( data.screen_height - text_height1) // 2
       screen.blit(text_surface, (text_x, text_y-140))
       pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
       pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
       pygame.display.flip()
       clock.tick(30)
def text(data):
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
    a=True
    selected_option1 =0
    previous_eje=0
    font = pygame.font.Font('Monocraft.ttf',22)
    data.Hist=1
    Imagen= pygame.image.load("historia.jpeg")
    #Imagen = pygame.transform.scsle(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        y_offset = 0
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
        # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.9 and previous_eje < 0.9:
                   selected_option1 = (selected_option1 + 1) % len(data.options_list)
            elif eje <= -1 and previous_eje > -1:
                    selected_option1 = (selected_option1 - 1) % len(data.options_list)
            if joystick.get_button(0):
               print("\n"+data.options_list[selected_option1])
               data.prompt_text+= "selected option"+data.options_list[selected_option1]
               load(data)
        # Actualizamos el estado previo del eje
            previous_eje = eje
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width,  data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                data.audio_once.play()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selected_option1 = (selected_option1 - 1) % len(data.options_list)
                elif event.key== pygame.K_ESCAPE:
                    Pausa(data)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selected_option1 = (selected_option1 + 1) % len(data.options_list)
                elif event.key == pygame.K_RETURN:
                    print("\n"+data.options_list[selected_option1])
                    data.prompt_text+= "selected option"+data.options_list[selected_option1]
                    load(data)
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        for i, option in enumerate(data.options_list):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-450,(( data.screen_height//2+30)) + i * 40))
            screen.blit(class_surface, class_rect)
           # print(option)


        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2-470  ,(( data.screen_height//2+30)) + selected_option1 * 40))
        screen.blit(arrow_surface, arrow_rect)

        for line in data.wrapped_text:
            text_surface = font.render(line, False, WHITE)
            text_width, text_height = font.size(line)
            text_x1 = (( data.screen_width ) // 2)-500
            text_y1 = ( data.screen_height) // 2 + y_offset -330
            screen.blit(text_surface, (text_x1, text_y1))
            y_offset += font.get_height()
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        if data.image:
            image_rect = data.image.get_rect(topleft=(data.screen_width // 2+260,  data.screen_height//2-340))
            screen.blit(data.image, image_rect)
       # pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2+250,  data.screen_height//2-300,256 ,256), 6)# esto es para la ubiccacion del dibujo
        pygame.display.flip()
        clock.tick(30)
# Función para dividir el texto en líneas
def wrap_text(text, max_width):
    lines = []
    words = text.split()
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    return(lines)
def chat(data):
           #print(prompt.prompt_text)
           response = openai.chat.completions.create(
           model="gpt-4o-mini",  # El motor de IA que deseas utilizar
           messages = [
               {"role": "system", "content" : data.prompt_text},
               ]
          )
           response_text = response.choices[0].message.content
           print(response_text)
           data.prompt_text+=response_text
           Imagen_prompt="Este es el contexto para la imagen de que vas a generar de be ser en estilo pixel art y detallar el contexto de la situacion: "
           Imagen_prompt+=response_text
           text_before_options = ""
           if "Options listed:" in response_text:
               text_before_options, _ = response_text.split("Options listed:")
               print(text_before_options)
           else:
               text_before_options, _ = response_text
               print("La cadena 'Options listed:' no está presente en response_text.")
           data.options_list = re.findall(r'\d+\..*?(?=\d+\.|$)', response_text, re.DOTALL)
           data.options_list= [texto.rstrip('\n') for texto in data.options_list]
           data.wrapped_text = wrap_text(text_before_options.strip(),1350)
#           image_url = generate_image(Imagen_prompt)
 #          if image_url:
  #             data.image = download_image(image_url)
   #        else:
    #           data.image = None
           text(data)
def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error al generar la imagen: {e}")
        return None
def download_image(url):
    try:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None
def load(data):
        # Define la pantalla para el resiza
        screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface3=font.render('Cargando...',False,'white')
        screen.blit(text_surface3, ( data.screen_width // 2+250,  data.screen_height//2+300))
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
        chat(data)
def load2(data):
        # Define la pantalla para el resiza
        screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
        data.audio_loop = pygame.mixer.Sound('overworld-theme.mp3')
        data.audio_loop.set_volume(0.2)  # Ajusta el volumen del audio en loop a 50%
        data.audio_loop.play(loops=-1)  # `loops=-1` indica que debe reproducirse en loop infinito
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface3=font.render('Cargando...',False,'white')
        screen.blit(text_surface3, ( data.screen_width // 2+250,  data.screen_height//2+300))
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
        text(data)
def Materias(data):
    a=True
    options = ["Matemáticas","Español","Inglés","Historia","Educación Física"]
    selected_option = 0
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    previous_eje=0
    button_2_pressed = False
    Imagen= pygame.image.load("temas.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
       Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
       joystick_count=pygame.joystick.get_count()
       if joystick_count>0:
           joystick = pygame.joystick.Joystick(0)
           joystick.init()
           eje = joystick.get_axis(1)
           if eje <= -1 and previous_eje > -1:
               selected_option = (selected_option - 1) % len(options)
           if eje >= 0.9 and previous_eje < 0.9:
               selected_option = (selected_option + 1) % len(options)
           previous_eje =eje
       for event in pygame.event.get():
           if joystick_count>0:
               if event.type == pygame.JOYBUTTONUP:
                   if event.button == 0:
                       button_2_pressed = False
           if event.type == pygame.QUIT:
              pygame.quit()
           if event.type == pygame.VIDEORESIZE:
       # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
               screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
               data.screen_width, data.screen_height = event.w, event.h
           if joystick_count>0:
               if event.type == pygame.JOYBUTTONDOWN:
                   if event.button == 0 and button_2_pressed == False:
                       print("Opción seleccionada:", options[selected_option])
                       if options[selected_option]=="Matemáticas":
                           data.prompt_text1+=data.matematicas
                           data.materia=1
                           load1(data)
                       if options[selected_option]=="Español":
                           data.prompt_text1+=data.español
                           data.materia=2
                           load1(data)
                       if options[selected_option]=="Inglés":
                           data.prompt_text1+=data.ingles
                           data.materia=3
                           load1(data)
                       if options[selected_option]=="Historia":
                           data.prompt_text1+=data.historia
                           data.materia=4
                           load1(data)
                       if options[selected_option]=="Educación Física":
                           data.prompt_text1+=data.educacionfisica
                           data.materia=5
                           load1(data)
           if event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP :
                   selected_option = (selected_option - 1) % len(options)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN :
                   selected_option = (selected_option + 1) % len(options)
               elif event.key == pygame.K_RETURN :
                   print("Opción seleccionada:", options[selected_option])
                   if options[selected_option]=="Matemáticas":
                       data.prompt_text1=data.matematicas
                       data.materia=1
                       data.Pregunta=1
                       print("hey")
                       load1(data)
                   elif options[selected_option]=="Español":
                       data.prompt_text1=data.español
                       data.materia=2
                       data.Pregunta=1
                       print("hey")
                       load1(data)
                   elif options[selected_option]=="Inglés":
                       data.prompt_text1=data.ingles
                       data.materia=3
                       data.Pregunta=1
                       print("hey")
                       load1(data)
                   elif options[selected_option]=="Historia":
                       data.prompt_text1=data.historia
                       data.materia=4
                       data.Pregunta=1
                       print("hey")
                       load1(data)
                   elif options[selected_option]=="Educación Física":
                       data.prompt_text1=data.educacionfisica
                       data.materia=5
                       data.Pregunta=1
                       print("hey")
                       load1(data)
       screen.blit(Imagen, ( 0,0))
       color_rectangulo = (0, 0, 0, 128)
       surface = pygame.Surface((1038,352), pygame.SRCALPHA)
       surface.fill(color_rectangulo)
       screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
       surface = pygame.Surface((988,322), pygame.SRCALPHA)
       surface.fill(color_rectangulo)
       screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
       for i, option in enumerate(options):
           class_surface = font.render(option, False, WHITE)
           class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-70,(( data.screen_height//2)+100) + i * 40))
           screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
       arrow_surface = font.render("->", False, WHITE)
       arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2 - 100,(( data.screen_height//2)+100) + selected_option * 40))
       screen.blit(arrow_surface, arrow_rect)
       text_surface=font.render('Selecciona una Materia',False,'WHITE')
       text_width1, text_height1 = text_surface.get_size()
       text_x = ( data.screen_width - text_width1) // 2
       text_y = ( data.screen_height - text_height1) // 2
       screen.blit(text_surface, (text_x, text_y-140))
       pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
       pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
       pygame.display.flip()
       clock.tick(30)
def load1(data):
        # Define la pantalla para el resiza
        screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface3=font.render('Cargando...',False,'white')
        screen.blit(text_surface3, ( data.screen_width // 2+250,  data.screen_height//2+300))
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
        chat1(data)
def chat1(data):
           #print(prompt.prompt_text)
           response = openai.chat.completions.create(
           model="gpt-4o-mini",  # El motor de IA que deseas utilizar
           messages = [
               {"role": "system", "content" :data.prompt_text1},
               ]
          )
           response_text =response.choices[0].message.content
           print(response_text)
           data.reactivos = re.findall(r'[A-D]\)\s[^\n]+', response_text)
           print(data.reactivos)
           data.Respuesta=[]
           respuesta= data.reactivos[-1]
           data.reactivos= data.reactivos[:-1]
           data.Respuesta.append(respuesta)
           print(data.Respuesta)
           response_text=response_text.replace("**","")
           lineas=response_text.split('\n')
           response_text=lineas[0]
           # Ahora separamos "Pregunta 1" de la pregunta
           parte1, parte2 = response_text.split(":", 1)
           # Quitamos los espacios en blanco adicionales
           parte1 = parte1.strip()
           parte2 = parte2.strip()
           data.prompt_text1+="pregunta anterior:"
           data.prompt_text1+=parte2
           data.parte2 = wrap_text(parte2,1200)
           preguntas(data)
def preguntas(data):
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
    Imagen= pygame.image.load("descargar .png")
    Imagen.set_colorkey((255, 255, 255))
    scaled_image = pygame.transform.scale(Imagen, (30, 30))
    a=True
    selected_option1 =0
    previous_eje=0
    font = pygame.font.Font('Monocraft.ttf',25)
    arrow_rect=0
    imagen= pygame.image.load("temas.jpeg")
    #imagen = pygame.transform.scale(imagen, (1500,700))
    while a:
        imagen = pygame.transform.scale(imagen, (data.screen_width, data.screen_height))
        y_offset=0
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
        # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.9 and previous_eje < 0.9:
                   selected_option1 = (selected_option1 + 1) % len(data.reactivos)
            elif eje <= -1 and previous_eje > -1:
                    selected_option1 = (selected_option1 - 1) % len(data.reactivos)
            if joystick.get_button(0):
               print("\n"+data.reactivos[selected_option1])
               data.Pregunta+=1
               data.prompt_text1+="\nSiguiente pregunta Num:"
               data.prompt_text1+=str(data.Pregunta)
               if data.reactivos[selected_option1].strip() == data.Respuesta[0].strip():
                       print("Correcto")
                       Correcto=font.render('✔ Correcto', False, "GREEN")
                       screen.blit(Correcto,( data.screen_width // 2-360,  (data.screen_height//2-20)))
                       pygame.display.flip()
                       data.correcto+=1
                       pygame.time.delay(3000)
                       if data.Pregunta==11:
                           fin_preguntas(data)
                       load1(data)
               else:
                       print("Error")
                       respuesta=data.Respuesta[0]
                       textoincorrecto=f'Incorrecto,respuesta correcta:{respuesta}'
                       incorrecto=font.render(textoincorrecto, False, "RED")
                       screen.blit(incorrecto,( data.screen_width // 2-360,  (data.screen_height//2-20)))
                       pygame.display.flip()
                       data.error+=1
                       pygame.time.delay(3000)
                       if data.Pregunta==11:
                           cha1(data)
                       load1(data)
            previous_eje = eje
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width,  data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                data.audio_once.play()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selected_option1 = (selected_option1 - 1) % len(data.reactivos)
                elif event.key== pygame.K_ESCAPE:
                    Pausa(data)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selected_option1 = (selected_option1 + 1) % len(data.reactivos)
                elif event.key == pygame.K_RETURN:
                    print("\n"+data.reactivos[selected_option1])
                    data.Pregunta+=1
                    data.prompt_text1+="\nRespuesta del usuario:"
                    data.prompt_text1+=str(data.reactivos[selected_option1])
                    data.prompt_text1+="\nSiguiente pregunta"
                    opcion_seleccionada=data.reactivos[selected_option1][3:].strip()
                    respuesta=data.Respuesta[0][3:].strip()
                    if opcion_seleccionada == respuesta:
                        print("Correcto")
                        Correcto=font.render('✔ Correcto', False, "GREEN")
                        screen.blit(Correcto,( data.screen_width // 2-510,  (data.screen_height//2-20)))
                        pygame.display.flip()
                        data.correcto+=1
                        pygame.time.delay(3000)
                        if data.Pregunta==11:
                            fin_preguntas(data)
                        load1(data)
                    else:
                        print("Error")
                        textoincorrecto=f'Incorrecto respuesta correcta:{respuesta}'
                        incorrecto=font.render(textoincorrecto, False, "RED")
                        screen.blit(incorrecto,( data.screen_width // 2-510,  (data.screen_height//2-20)))
                        pygame.display.flip()
                        data.error+=1
                        pygame.time.delay(3000)
                        if data.Pregunta==11:
                            fin_preguntas(data)
                        elif data.error==5:
                            cha1(data)
                        load1(data)
        screen.blit(imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        for i, option in enumerate(data.reactivos):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-440,(( data.screen_height//2+80)) + i * 40))
            screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2-460  ,(( data.screen_height//2+80)) + selected_option1 * 40))
        screen.blit(arrow_surface, arrow_rect)
        for line in data.parte2:
            text_surface = font.render(line, False, WHITE)
            text_width, text_height = font.size(line)
            text_x1 = (( data.screen_width ) // 2)-500
            text_y1 = ( data.screen_height) // 2 + y_offset -300
            screen.blit(text_surface, (text_x1, text_y1))
            y_offset += font.get_height()
        textpreg=f"Pregunta {data.Pregunta}"
        text_surface = font.render(textpreg, False, WHITE)
        text_x1 = (( data.screen_width ) // 2)-510
        text_y1 = ( data.screen_height) // 2 -330
        screen.blit(text_surface, (text_x1, text_y1))
        textpreg1="Vidas restantes:"
        text_surface1 = font.render(textpreg1, False, WHITE)
        text_x11 = (( data.screen_width ) // 2)+30
        text_y11 = ( data.screen_height) // 2 -340
        screen.blit(text_surface1, (text_x11, text_y11))
        a=5-data.error
        for i in range(a):
            screen.blit(scaled_image, (( data.screen_width // 2+300)+i*40,( data.screen_height//2-340)) )

        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
def fin_preguntas(data):
    #Imagen= pygame.image.load("D:\IA proyect\images (13).jpg")
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    # Define la pantalla para el resiza
    option12 = ["Continuar aprendiendo", "Menu principal"]
    option1=0
    a=True
    previous_eje = 0
    data.Preguntas=0
    audio=pygame.mixer.Sound("brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3")
    audio.play()
    Imagen= pygame.image.load("temas.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   option1 = (option1 - 1) % len(option12)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   option1 = (option1 + 1) % len(option12)
               elif event.key == pygame.K_RETURN:
                   print("Opción seleccionada:", option12[option1])
                   if option12[option1]=="Continuar aprendiendo":
                         data.Pregunta=0
                         if data.materia==1:
                             data.prompt_text1+=data.matematicas
                         elif data.materia==2:
                             data.prompt_text1+=data.español
                         elif data.materia==3:
                             data.prompt_text1+=data.ingles
                         elif data.materia==4:
                             data.prompt_text1+=data.historia
                         elif data.materia==5:
                             data.prompt_text1+=data.educacionfisica
                         Materias(data)
                   elif option12[option1]=="Menu principal":
                       data.Pregunta=0
                       main(data)
        if joystick_count>0:
            # Lectura de los ejes del joystick
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
    # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.2 and previous_eje < 0.2:
                option1 = (option1 + 1) % len(option12)
            elif eje <= -0.2 and previous_eje > -0.2:
                option1 = (option1 - 1) % len(option12)
            if joystick.get_button(0)==1:
                print("Opción seleccionada:", option12[option1])
                if option12[option1]=="Continuar aprendiendo":
                        data.Pregunta=0
                        Materias(data)
                if option12[option1]=="Menu principal":
                    data.Pregunta=0
                    main(data)
    # Actualizamos el estado previo del eje
            previous_eje = eje
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface=font.render('*Felicidades en completar la leccion*',False,'white')
        text_width1, text_height1 = text_surface.get_size()
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_surface, (text_x, text_y-230))
        for i, option in enumerate(option12):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-300,(( data.screen_height//2+100)) + i * 80))
            screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2-310  ,(( data.screen_height//2+100)) + option1 * 80))
        screen.blit(arrow_surface, arrow_rect)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
def fin_preguntas2(data,texto):
    #Imagen= pygame.image.load("D:\IA proyect\images (13).jpg")
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    # Define la pantalla para el resiza
    option12 = ["Continuar aprendiendo", "Menu principal"]
    option1=0
    a=True
    previous_eje = 0
    data.Preguntas=0
    audio=pygame.mixer.Sound("videogame-death-sound-43894.mp3")
    audio.play()
    Imagen= pygame.image.load("temas.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        y_offset=0
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   option1 = (option1 - 1) % len(option12)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   option1 = (option1 + 1) % len(option12)
               elif event.key == pygame.K_RETURN:
                   print("Opción seleccionada:", option12[option1])
                   if option12[option1]=="Continuar aprendiendo":
                         data.Pregunta=0
                         if data.materia==1:
                             data.prompt_text1+=data.matematicas
                         if data.materia==2:
                             data.prompt_text1+=data.español
                         if data.materia==3:
                             data.prompt_text1+=data.ingles
                         if data.materia==4:
                             data.prompt_text1+=data.historia
                         if data.materia==5:
                             data.prompt_text1+=data.educacionfisica
                         Materias(data)
                   if option12[option1]=="Menu principal":
                       data.Pregunta=0
                       main(data)
        if joystick_count>0:
            # Lectura de los ejes del joystick
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
    # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.2 and previous_eje < 0.2:
                option1 = (option1 + 1) % len(option12)
            elif eje <= -0.2 and previous_eje > -0.2:
                option1 = (option1 - 1) % len(option12)
            if joystick.get_button(0)==1:
                print("Opción seleccionada:", option12[option1])
                if option12[option1]=="Continuar aprendiendo":
                        data.Pregunta=0
                        Materias(data)
                if option12[option1]=="Menu principal":
                    data.Pregunta=0
                    main(data)
    # Actualizamos el estado previo del eje
            previous_eje = eje
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface=font.render('GAME OVER',False,'red')
        text_width1, text_height1 = text_surface.get_size()
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height) // 2 -340
        screen.blit(text_surface, (text_x, text_y))
        for i, option in enumerate(option12):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=( data.screen_width // 2-300,(( data.screen_height//2+100)) + i * 80))
            screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=( data.screen_width // 2-310  ,(( data.screen_height//2+100)) + option1 * 80))
        screen.blit(arrow_surface, arrow_rect)
        for line in texto:
            text_surface = font.render(line, False, WHITE)
            text_width, text_height = font.size(line)
            text_x1 = (( data.screen_width ) // 2)-500
            text_y1 = ( data.screen_height) // 2 + y_offset -300
            screen.blit(text_surface, (text_x1, text_y1))
            y_offset += font.get_height()
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
def cha1(data):
           data.prompt_text1+="El estudiante se equivoco mas de 5 veces y fallo la leccion, imagina que estas hablando con el estudiante y dale consejos para que pueda mejorar, que sobre todo sea breve no mas de 40 palabras y intenta hacerlo con todo de historia de fantasia "

           #print(prompt.prompt_text)
           response = openai.chat.completions.create(
           model="gpt-4o-mini",  # El motor de IA que deseas utilizar
           messages = [
               {"role": "system", "content" : data.prompt_text1},
               ]
          )
           response_text =response.choices[0].message.content
           print(response_text)
           response_text = wrap_text(response_text,1000)
           fin_preguntas2(data,response_text)
def Pausa(data):
    paused = True
    screen = pygame.display.set_mode(( data.screen_width,  data.screen_height), pygame.RESIZABLE)
    Opciones=["Continuar","Menu principal"]
    opcion=0
    previous_eje=0
    while paused:
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
        # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.9 and previous_eje < 0.9:
                   opcion = (opcion + 1) % len(Opciones)
            elif eje <= -1 and previous_eje > -1:
                    opcion = (opcion - 1) % len(Opciones)
            if joystick.get_button(0):
                if Opciones[opcion]=="Continuar":
                    return
                if Opciones[opcion]=="Menu principal":
                     main(data)
            previous_eje=eje
        for event in pygame.event.get():
           if event.type == pygame.VIDEORESIZE:
       # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
               screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
               data.screen_width,  data.screen_height = event.w, event.h
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   opcion = (opcion - 1) % len(Opciones)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   opcion = (opcion + 1) % len(Opciones)
               if event.key == pygame.K_RETURN:  # Presiona 'P' para reanudar
                   if Opciones[opcion]=="Continuar":
                       return
                   if Opciones[opcion]=="Menu principal":
                        main(data)
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        for i, option in enumerate(Opciones):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=( (data.screen_width // 2)-100,(( data.screen_height//2+100)) + i * 80))
            screen.blit(class_surface, class_rect)
        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=( (data.screen_width // 2)-135  ,(( data.screen_height//2+100)) + opcion * 80))
        screen.blit(arrow_surface, arrow_rect)
        text_surface3=font.render('PAUSA',False,'white')
        screen.blit(text_surface3, ( (( data.screen_width ) // 2)-50, ( data.screen_height) // 2 -240))
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-375,  data.screen_height//2-250,750 ,260), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-350, data.screen_height//2+10, 700,230), 6)
        pygame.display.flip()
        clock.tick(30)
def start(data):
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    # Define la pantalla para el resiza
    option12 = ["Nueva Partida", "Continuar Partida","Salir"]
    option1=0
    a=True
    previous_eje = 0
    Imagen= pygame.image.load("inicio.jpeg")
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   option1 = (option1 - 1) % len(option12)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   option1 = (option1 + 1) % len(option12)
               elif event.key == pygame.K_RETURN:
                   print("Opción seleccionada:", option12[option1])
                   if option12[option1]=="Nueva Partida":
                           Inicio(data)
                   if option12[option1]=="Continuar Partida":
                       cargar(data)
                   if option12[option1]=="Salir":
                       pygame.quit()
        if joystick_count>0:
            # Lectura de los ejes del joystick
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
    # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= .9 and previous_eje < .9:
                option1 = (option1 + 1) % len(option12)
            elif eje <= -1 and previous_eje > -1:
                option1 = (option1 - 1) % len(option12)
            if joystick.get_button(0)==1:
                print("Opción seleccionada:", option12[option1])
                if option12[option1]=="Nueva Partida":
                        Inicio(data)
                if option12[option1]=="Continuar Partida":
                    cargar(data)
                if option12[option1]=="Salir":
                    pygame.quit()
    # Actualizamos el estado previo del eje
            previous_eje = eje
        screen.blit(Imagen, ( 0,0))
        color_rectangulo = (0, 0, 0, 128)
        surface = pygame.Surface((1038,352), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-519, data.screen_height//2-344))
        surface = pygame.Surface((988,322), pygame.SRCALPHA)
        surface.fill(color_rectangulo)
        screen.blit(surface, (data.screen_width // 2-494, data.screen_height//2+14))
        text_surface=font.render('Bienvenido a SoulQuest',False,'white')
        text_width1, text_height1 = text_surface.get_size()
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_surface, (text_x, text_y-200))
        for i, option in enumerate(option12):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=(text_x,(text_y+150) + i * 80))
            screen.blit(class_surface, class_rect)

        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=(text_x-30,(text_y+150) + option1 * 80))
        screen.blit(arrow_surface, arrow_rect)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)

def Inicio(data):
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    previous_eje=0
    previous_eje1=0
    # Variables para entrada de texto
    text = ""
    # Define el cuadro de texto
    color_inactive = pygame.Color('dodgerblue2')
    color = color_inactive
    test_surface=pygame.Surface((800,600))
    test_surfacex,test_surfacey=test_surface.get_size()
    text_surface=font.render('Ingresa tu nombre',False,'white')
    text_width1, text_height1 = text_surface.get_size()
    a=True
    KEY_WIDTH = 50
    KEY_HEIGHT = 50
    # Índices de la tecla actualmente seleccionada
    selected_row = 0
    selected_col = 0
    button_2_pressed = False
    Imagen= pygame.image.load("inicio.jpeg")
    data.prompt_text = "Eres un asistente que me ayudara a desarrollar la historia del entorno en el que se desarrolla el juego, tu trabajo sera el principio explicar un poco de la historia del mundo actual y/o del jugador, debes narrar en no mas de 150 palabras despues en un listado llamado 'Options listed:'con acciones ennumeradas que puedo realizar que sean simples y definidas en maximo 5 palabras no incluyas nada de texto despues de las acciones como por ejemplo:Which action would you like to take? , despues te mencionare la acción que se llevo a cabo, y volveras a repetir este proceso donde me describas la situacion y me des las acciones. estos son los datos del jugador:  "
    data.prompt_text1= ""
    data.historia= """
                       Eres un asistente de aprendizaje especializado en Historia Mexicana para niños de primaria. Tu tarea es hacer preguntas sobre hechos históricos básicos y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre hechos históricos básicos, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4.El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Quién fue el primer presidente de México?

**Reactivos:**
A) Benito Juárez
B) Vicente Guerrero
C) Guadalupe Victoria
D) Porfirio Díaz

**Respuesta correcta:** C) Guadalupe Victoria

Empecemos con la primera pregunta.
                       """
    data.matematicas="""
                       Eres un asistente de aprendizaje especializado en matemáticas básicas, específicamente en sumas y restas. Tu tarea es hacer preguntas sobre este tema y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre matemáticas básicas (sumas y restas),una por una y te indicare cuando darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema (sumas y restas) y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es el resultado de 8 + 5?

**Reactivos:**
A) 10
B) 12
C) 13
D) 14

**Respuesta correcta:** C) 13
Empecemos con la primera pregunta.
                       """
    data.español= """
                       Eres un asistente de aprendizaje especializado en Español para niños de primaria. Tu tarea es hacer preguntas sobre vocabulario y gramática básica y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre vocabulario y gramática básica, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es el sinónimo de "feliz"?

**Reactivos:**
A) Triste
B) Alegre
C) Enojado
D) Cansado

**Respuesta correcta:** B) Alegre

Empecemos con la primera pregunta.
                       """
    data.ingles="""
                       Eres un asistente de aprendizaje especializado en Inglés para niños de primaria. Tu tarea es hacer preguntas sobre vocabulario y gramática básica en inglés y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre vocabulario y gramática básica, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** What is the English word for "perro"?

**Reactivos:**
A) Cat
B) Dog
C) Bird
D) Fish

**Respuesta correcta:** B) Dog

Empecemos con la primera pregunta.
                       """
    data.educacionfisica="""
                       Eres un asistente de aprendizaje especializado en Educación Física para niños de primaria. Tu tarea es hacer preguntas sobre conceptos básicos de ejercicios y deportes y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre conceptos básicos de ejercicios y deportes, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es un ejercicio cardiovascular?

**Reactivos:**
A) Levantamiento de pesas
B) Yoga
C) Correr
D) Estiramientos

**Respuesta correcta:** C) Correr

Empecemos con la primera pregunta.
                       """
    data.correcto=0
    data.error=0
    data.options_list=[]
    data.wrapped_text=""
    data.reactivos=[]
    data.Respuesta=[]
    data.parte2=""
    data.Hist=0
    data.Pregunta=0
    data.playerName=""
    data.materia=0
    #Imagen = pygame.transform.scale(Imagen, (1500,700))
    while a:
        Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        # Definir las teclas y sus posiciones en una cuadrícula
        keys = [
            {'char': 'Q', 'x':((data.screen_width-450) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 0},
            {'char': 'W', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 1},
            {'char': 'E', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 2},
            {'char': 'R', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 3},
            {'char': 'T', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 4},
            {'char': 'Y', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 5},
            {'char': 'U', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 6},
            {'char': 'I', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 7},
            {'char': 'O', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height -60) // 2), 'row': 0, 'col': 8},
            {'char': 'P', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 0},
            {'char': 'A', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 1},
            {'char': 'S', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 2},
            {'char': 'D', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 3},
            {'char': 'F', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 4},
            {'char': 'G', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 5},
            {'char': 'H', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 6},
            {'char': 'J', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 7},
            {'char': 'K', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +40) // 2), 'row': 1, 'col': 8},
            {'char': 'L', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 0},
            {'char': 'Ñ', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 1},
            {'char': 'Z', 'x': ((data.screen_width-250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 2},
            {'char': 'X', 'x': ((data.screen_width-150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 3},
            {'char': 'C', 'x': ((data.screen_width-50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 4},
            {'char': 'V', 'x': ((data.screen_width+50) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 5},
            {'char': 'B', 'x': ((data.screen_width+150) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 6},
            {'char': 'N', 'x': ((data.screen_width+250) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 7},
            {'char': 'M', 'x': ((data.screen_width+350) // 2), 'y': ((data.screen_height +140) // 2), 'row': 2, 'col': 8},
            {'char': 'DEL', 'x': ((data.screen_width-450) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 0},  # Botón de retroceso
            {'char': 'GO', 'x': ((data.screen_width-350) // 2), 'y': ((data.screen_height +240) // 2), 'row': 3, 'col': 1},
            # Añadir más teclas según sea necesario
        ]
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
            eje1=joystick.get_axis(0)
       # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= .9 and previous_eje < .9:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'down')
            elif eje <= -1 and previous_eje > -1:
                 selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'up')
            elif eje1 >= .9 and previous_eje1 < .9:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'right')
            elif eje1 <= -1 and previous_eje1 > -1:
                   selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'left')

            previous_eje=eje
            previous_eje1=eje1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if joystick_count>0:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 and not button_2_pressed:
                        key = get_key_at_position(selected_row, selected_col)
                        if key:
                            if key["char"] == "DEL":
                                text = text[:-1]  # Borra el último carácter
                            if key["char"]=="GO":
                               data.playerName=text
                               print("Nombre del jugador:", text)
                               main(data)
                            else:
                               text += key["char"]
                               button_2_pressed = True
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        button_2_pressed = False
            if event.type == pygame.KEYDOWN:
                    data.audio_once.play()
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'left')
                    elif  event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'right')
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'up')
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        selected_row, selected_col = move_selection(selected_row, selected_col, keys, 'down')
                    elif event.key == pygame.K_RETURN:
                        key = get_key_at_position(selected_row, selected_col)
                        if key:
                            if key["char"]=="DEL":
                                text = text[:-1]  # Borra el último carácter
                            elif key["char"]=="GO":
                                data.playerName=text
                                print("Nombre del jugador:", text)
                                main(data)
                            else:
                                text += key["char"]
        screen.blit(Imagen, ( 0,0))
        input_box = pygame.Rect(((data.screen_width-300) // 2), ((data.screen_height -200) // 2), 300, 60)
        # Renderiza el texto ingresado por el usuario
        rendered_text = font.render(text, False, WHITE)
        text_width = rendered_text.get_width()
        # Ajusta el texto al ancho del cuadro de texto
        text_rendered = rendered_text if text_width < input_box.width else font.render(text[-13:], False, WHITE)
        # Dibuja el cuadro de texto
        pygame.draw.rect(screen, color, input_box, 2)
        # Dibuja el texto en el cuadro de texto
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_rendered, (input_box.x + 5, input_box.y+15))
        screen.blit(text_surface, (text_x, text_y-150))
        for key in keys:
            rect = pygame.Rect(key['x'], key['y'], KEY_WIDTH, KEY_HEIGHT)
            color = 'RED' if key['row'] == selected_row and key['col'] == selected_col else WHITE
            pygame.draw.rect(screen, color, rect)
            texto = font.render(key['char'], True, BLACK)
            texto_rect = texto.get_rect(center=(key['x'] + KEY_WIDTH // 2, key['y'] + KEY_HEIGHT // 2))
            screen.blit(texto, texto_rect)
        pygame.display.flip()
        clock.tick(30)
def guardar(data):
    from IPython.display import clear_output
    clear_output(wait=True)
    filename = data.playerName + "_savegame.txt"
    try:
        with open(filename, "w") as file:
            saved_data = {
                'prompt_text': data.prompt_text,
                'prompt_text1': data.prompt_text1,
                'playerName': data.playerName,
                'wrapped_text': data.wrapped_text,
                'parte2': data.parte2,
                'Respuesta': data.Respuesta,
                'options_list': data.options_list,
                'reactivos': data.reactivos,
                'screen_width': data.screen_width,
                'screen_height': data.screen_height,
                'correcto': data.correcto,
                'error': data.error,
                'Pregunta': data.Pregunta,
                'Hist': data.Hist,
                'historia': data.historia,
                'matematicas': data.matematicas,
                'español': data.español,
                'ingles': data.ingles,
                'educacionfisica': data.educacionfisica,
                'materia': data.materia,
            }
            json.dump(saved_data, file, indent=4)
        print("Juego guardado exitosamente como '" + filename + "'.")
        start(data)
    except Exception as e:
        print("Error: Fallo al guardar el juego como '" + filename + "':", e)
        return

def cargar(data):
    #Imagen= pygame.image.load("D:\IA proyect\images (13).jpg")
    # Define la pantalla para el resiza
    screen = pygame.display.set_mode((data.screen_width, data.screen_height), pygame.RESIZABLE)
    # Define la pantalla para el resiza
    save_games=[]
    save_dir = '.'
    for filename in os.listdir(save_dir):
        if filename.endswith("_savegame.txt"):
            save_games.append(filename)
    option1=0
    a=True
    previous_eje = 0
    while a:
        #Imagen = pygame.transform.scale(Imagen, (data.screen_width, data.screen_height))
        joystick_count=pygame.joystick.get_count()
        if joystick_count>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
        # Cambia el tamaño de la pantalla si el usuario cambia el tamaño de la ventana
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                data.screen_width, data.screen_height = event.w, event.h
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
               data.audio_once.play()
               if event.key == pygame.K_w or event.key == pygame.K_UP:
                   option1 = (option1 - 1) % len(save_games)
               elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                   option1 = (option1 + 1) % len(save_games)
               elif event.key == pygame.K_RETURN:
                   print("Opción seleccionada:", save_games[option1])
                   filename = save_games[option1]
                   try:
                       with open(filename, "r") as file:
                           saved_data = json.load(file)
                           data.prompt_text = saved_data['prompt_text']
                           data.prompt_text1 = saved_data['prompt_text1']
                           data.playerName = saved_data['playerName']
                           data.wrapped_text = saved_data['wrapped_text']
                           data.parte2 = saved_data['parte2']
                           data.Respuesta = saved_data['Respuesta']
                           data.options_list = saved_data['options_list']
                           data.reactivos = saved_data['reactivos']
                           data.screen_width = saved_data['screen_width']
                           data.screen_height = saved_data['screen_height']
                           data.correcto = saved_data['correcto']
                           data.error = saved_data['error']
                           data.Pregunta = saved_data['Pregunta']
                           data.Hist = saved_data['Hist']
                           data.historia=saved_data['historia']
                           data.matematicas=saved_data['matematicas']
                           data.español=saved_data['español']
                           data.ingles=saved_data['ingles']
                           data.educacionfisica=saved_data['educacionfisica']
                           data.materia=saved_data['materia']
                       print("Juego cargado exitosamente.")
                       main(data)
                   except FileNotFoundError:
                       print(f"No se encontró el juego con el nombre '{filename}'.")
        if joystick_count>0:
            # Lectura de los ejes del joystick
            eje = joystick.get_axis(1)  # Aquí usamos el eje 0 como ejemplo
    # Comprobamos si el eje ha cruzado el umbral desde el estado previo
            if eje >= 0.2 and previous_eje < 0.2:
                option1 = (option1 + 1) % len(save_games)
            elif eje <= -0.2 and previous_eje > -0.2:
                option1 = (option1 - 1) % len(save_games)
            if joystick.get_button(0)==1:
                print("Opción seleccionada:", save_games[option1])
                if save_games[option1]=="Nueva Partida":
                        Inicio(data)
                if save_games[option1]=="Continuar Partida":
                    cargar(data)
    # Actualizamos el estado previo del eje
            previous_eje = eje
        #screen.blit(Imagen, (0, 0))
        screen.fill(BLACK)
        text_surface=font.render('ELige una partida',False,'white')
        text_width1, text_height1 = text_surface.get_size()
        text_x = (data.screen_width - text_width1) // 2
        text_y = (data.screen_height - text_height1) // 2
        screen.blit(text_surface, (text_x, text_y-200))
        for i, option in enumerate(save_games):
            class_surface = font.render(option, False, WHITE)
            class_rect = class_surface.get_rect(midleft=(text_x,(text_y+70) + i * 80))
            screen.blit(class_surface, class_rect)

        # Dibujar flecha junto a la opción seleccionada
        arrow_surface = font.render("->", False, WHITE)
        arrow_rect = arrow_surface.get_rect(midright=(text_x-30,(text_y+70) + option1 * 80))
        screen.blit(arrow_surface, arrow_rect)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-525,  data.screen_height//2-350,1050 ,364), 6)
        pygame.draw.rect(screen, 'BLUE', ( data.screen_width // 2-500, data.screen_height//2+10, 1000,334), 6)
        pygame.display.flip()
        clock.tick(30)
if __name__ == "__main__":
    data=Data()
    data.screen_width=1500
    data.screen_height=700
    data.prompt_text = "Eres un asistente que me ayudara a desarrollar la historia del entorno en el que se desarrolla el juego, tu trabajo sera el principio explicar un poco de la historia del mundo actual y/o del jugador, debes narrar en no mas de 150 palabras despues en un listado llamado 'Options listed:'con acciones ennumeradas que puedo realizar que sean simples y definidas en maximo 5 palabras no incluyas nada de texto despues de las acciones como por ejemplo:Which action would you like to take? , despues te mencionare la acción que se llevo a cabo, y volveras a repetir este proceso donde me describas la situacion y me des las acciones. estos son los datos del jugador:  "
    data.prompt_text1= ""
    data.historia= """
                       Eres un asistente de aprendizaje especializado en Historia Mexicana para niños de primaria. Tu tarea es hacer preguntas sobre hechos históricos básicos y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre hechos históricos básicos, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4.El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Quién fue el primer presidente de México?

**Reactivos:**
A) Benito Juárez
B) Vicente Guerrero
C) Guadalupe Victoria
D) Porfirio Díaz

**Respuesta correcta:** C) Guadalupe Victoria

Empecemos con la primera pregunta.
                       """
    data.matematicas="""
                       Eres un asistente de aprendizaje especializado en matemáticas básicas, específicamente en sumas y restas. Tu tarea es hacer preguntas sobre este tema y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre matemáticas básicas (sumas y restas),una por una y te indicare cuando darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema (sumas y restas) y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es el resultado de 8 + 5?

**Reactivos:**
A) 10
B) 12
C) 13
D) 14

**Respuesta correcta:** C) 13
Empecemos con la primera pregunta.
                       """
    data.español= """
                       Eres un asistente de aprendizaje especializado en Español para niños de primaria. Tu tarea es hacer preguntas sobre vocabulario y gramática básica y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre vocabulario y gramática básica, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es el sinónimo de "feliz"?

**Reactivos:**
A) Triste
B) Alegre
C) Enojado
D) Cansado

**Respuesta correcta:** B) Alegre

Empecemos con la primera pregunta.
                       """
    data.ingles="""
                       Eres un asistente de aprendizaje especializado en Inglés para niños de primaria. Tu tarea es hacer preguntas sobre vocabulario y gramática básica en inglés y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre vocabulario y gramática básica, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** What is the English word for "perro"?

**Reactivos:**
A) Cat
B) Dog
C) Bird
D) Fish

**Respuesta correcta:** B) Dog

Empecemos con la primera pregunta.
                       """
    data.educacionfisica="""
                       Eres un asistente de aprendizaje especializado en Educación Física para niños de primaria. Tu tarea es hacer preguntas sobre conceptos básicos de ejercicios y deportes y proporcionar opciones de respuesta. A continuación, se detallan los requisitos:
    0. Harás las preguntas como una historia de fantasía.
1. Harás preguntas sobre conceptos básicos de ejercicios y deportes, una por una y te indicaré cuándo darme la siguiente pregunta.
2. Para cada pregunta, proporcionarás un listado de 4 reactivos (opciones de respuesta) etiquetados como A, B, C, y D. Entre estas opciones, una debe ser la respuesta correcta.
3. Las opciones de respuesta (reactivos) deben ser listadas bajo el título "Reactivos".
4. El reactivo correcto debe ser listado por separado bajo el título "Respuesta correcta".
5. Si el usuario comete más de 5 errores, proporcionarás una explicación del tema y sugerencias para mejorar el aprendizaje del tema.
6. Cada pregunta debe ser numerada secuencialmente.
7.no repitas preguntas.
A continuación se muestra un ejemplo del formato esperado:

**Pregunta 1:** ¿Cuál es un ejercicio cardiovascular?

**Reactivos:**
A) Levantamiento de pesas
B) Yoga
C) Correr
D) Estiramientos

**Respuesta correcta:** C) Correr

Empecemos con la primera pregunta.
                       """
    data.correcto=0
    data.error=0
    data.options_list=[]
    data.wrapped_text=""
    data.reactivos=[]
    data.Respuesta=[]
    data.parte2=""
    data.Hist=0
    data.Pregunta=0
    data.playerName=""
    data.materia=0
    data.image=""
    data.audio_once = pygame.mixer.Sound('beep.mp3')
    data.audio_once.set_volume(1.0)
    data.audio_loop = pygame.mixer.Sound('aprendizaje musica.mp3')
    data.audio_loop.set_volume(0.2)  # Ajusta el volumen del audio en loop a 50%
    start(data)
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()