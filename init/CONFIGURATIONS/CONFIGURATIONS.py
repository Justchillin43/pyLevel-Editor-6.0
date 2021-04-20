import pygame
import numpy

#WINDOW setting
WIDTH = 1350
HEIGHT = 650


#COLOR setting
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 155, 100)


#INTERACTION BETWEEN main and GUI
path = []
img_path = []
dict_img_path = {}
for_easy_access = {}
image_in_file = []
positions_of_tiles_lst = []
pathdir = ""
end_range = 14
start_range = 0
selected_txt_file = []
RUNNING = True
playing = []
end_of_values_returned_menu = 100
width_of_menu = 100
color_key = WHITE
How_to_play_variable = "other/HowTo_play/howToPlay.txt"



#GRID settings
grid_width = 1350 
grid_height = 1300
BLOCK_SIZE = 50
THICKNESS = 0


#TILE setting
tile_size = 50
x_length_of_tile = 50
y_length_of_tile = 50

