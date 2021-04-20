

import pygame, sys
from pygame.locals import *
from copy import deepcopy
import math
import tkinter
from tkinter import messagebox
import numpy
pygame.init()
from init.CONFIGURATIONS.CONFIGURATIONS import *



class Editor(object):
	def __init__(self):
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Level Editor")
		self.icon = pygame.image.load("other/data/icons/app-x-plasma-icon.png")
		pygame.display.set_icon(self.icon)
		self.running = True
		self.click = False
		self.default_map = {}#[selected image tile, rotation, x, y, index of image]
		self.map_from_txt_file = {}
		self.file = dict_img_path
		self.selected_map = self.default_map
		self.add_to_lst = False
		self.count_the_num_of_lst = 0
		self.load_text_file()
		self.selected_tile_to_blit = ""
		self.the_range_of_images_being_displayed_on_widget = [0, 0]#[up, down]
		self.scroll_boolean_down = True
		self.scroll_boolean_up = True
		self.FPS = pygame.time.Clock()
		self.displayed_images_range()
		self.selecter_of_image = pygame.transform.scale(pygame.image.load("other/selecter_image/selecter_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
		self.save_button_image = pygame.transform.scale(pygame.image.load("other/selecter_image/save_button.png"), (100, 30))
		self.position_of_selecter_of_images = [0, 0]
		self.scroll = False
		self.scroll_x = 0
		self.scroll_y = 0
		self.rotation = 0
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		self.start_point = [0, 0]
		self.allow_scaled_selecter = False
		self.copy = False
		self.available_to_paste_and_delete = False
		self.copied_tiles = []
		self.paste = False
		self.start_copy_position = [0, 0]
		self.allow_paste = False
		self.start_value = [0, 0]
		self.mouse_X_For_Rect = 0
		self.mouse_Y_For_Rect = 0
		self.clicked_tile = False
		self.scroll_speed_config = open("other/data/scroll speed.txt", "r+")
		self.current_tile_in_in_file = ""
		self.switch_grid_on_and_off = 0
		self.scrolling_up = False
		self.scrolling_down = False
		self.scroll_boolean_down = False
		self.scroll_speed = int(self.scroll_speed_config.read())
		self.not_empty = False
		self.allow_save = False



	def set_map(self):
		file = 0
		if self.check_if_text_file_is_empty() == True:
			file = self.default_map
		if self.check_if_text_file_is_empty() == False:
			file = self.map_from_txt_file
		return file


	def load_text_file(self):
		image_lst_from_txtfile = []
		path_lst_from_txtfile = []
		image_and_directory = []
		locations_lst = []
		second_list_from_txt_file =  []
		list_version_of_text_file = []
		surface_list = []

		if self.check_if_text_file_is_empty() == False:
			try:
				for file in selected_txt_file:
					text_file = open(file, "r+")
					reading_txt_file = text_file.read()
					list_version_of_text_file = reading_txt_file.split("*+*")


				del list_version_of_text_file[-1]
				for i in list_version_of_text_file:
					second_list_from_txt_file.append(i.split(","))


				for tile in second_list_from_txt_file:
					image_lst_from_txtfile.clear()
					path_lst_from_txtfile.clear()
					for data in tile:
						if self.count_the_num_of_lst == 1:
							if self.add_to_lst == True:
								if data != '[' and data != ']':
									image_lst_from_txtfile.append(data)

						
						if self.count_the_num_of_lst == 2:
							if self.add_to_lst == True:
								if data != '[' and data != ']':
									self.count_the_num_of_lst = 0
									path_lst_from_txtfile.append(data)


						if data == '[':
							self.add_to_lst = True
							self.count_the_num_of_lst += 1


						elif data == ']':
							self.add_to_lst = False

					image_and_directory.clear()
					for image in image_lst_from_txtfile:
						if len(path_lst_from_txtfile) > 1:
							image_and_directory.append(path_lst_from_txtfile[image_lst_from_txtfile.index(image)]+"\\"+image)
						else:
							image_and_directory.append(path_lst_from_txtfile[0]+"\\"+image)
						

						locations_lst.clear()
						for integer in tile[len(image_lst_from_txtfile)+1:-len(path_lst_from_txtfile)-1]:
							if integer != '[' and integer != ']':
								locations_lst.append(integer)


					surface_list.clear()
					for i in image_and_directory:
						image_to_blit = pygame.image.load(i)
						surface_list.append(image_to_blit)
					loc = locations_lst[0]+":"+locations_lst[1]
							
			
					for i in image_and_directory:
						for p in path_lst_from_txtfile:
							if loc not in self.selected_map:
								if len(image_lst_from_txtfile) > 1:
									self.selected_map[loc] = [[img.copy() for img in surface_list], int(locations_lst[0]), int(locations_lst[1]), int(locations_lst[2]), [pth for pth in path_lst_from_txtfile], [i for i in image_lst_from_txtfile]]
								else:
									self.selected_map[loc] = [[image_to_blit.copy()], int(locations_lst[0]), int(locations_lst[1]), int(locations_lst[2]), [p], [image]]


			except FileNotFoundError:
				messagebox.showerror("Error", "corrupted text File")
				self.playing = False#this quits the app
				self.running = False#this quits the program
				playing.append(False)#this quits the tkinter gui
				dict_img_path.clear()
				for_easy_access.clear()


	def check_if_text_file_is_empty(self):
		for file in selected_txt_file:
			isEmpty = True
			open_file = open(file, "r")
			file = open_file


			if file.read() == "":
				isEmpty = True
			else:
				isEmpty = False
			return isEmpty


	def loop(self):
		self.playing = True
		while self.playing:
			self.window.fill(BLACK)
			self.load_images_on_window()
			self.images_in_image_path()
			self.copied_tiles_to_be_displayed()
			self.save_button()
			self.selecters_function()
			self.events()
			self.to_ensure_the_init_file_is_not_run()
			pygame.display.flip()
			self.FPS.tick(50)



	def to_ensure_the_init_file_is_not_run(self):
		if len(dict_img_path) < 1:
			print("Don't run this file, run the 'main.py' file") \


#------------------------------
#|	sets the image range      |
#------------------------------
	def displayed_images_range(self):
		if len(dict_img_path) > int(HEIGHT/BLOCK_SIZE):
			self.the_range_of_images_being_displayed_on_widget[1] = 14
		elif len(dict_img_path) < int(HEIGHT/BLOCK_SIZE):
			self.end = len(dict_img_path)


#---------------------------------
#resposible  for the tiles widget
#---------------------------------
	def images_in_image_path(self):
		self.x_value = 0
		self.y_value = 0
		self.mouse_rect = pygame.Rect(self.mouse_X_For_Rect, self.mouse_Y_For_Rect, 2, 2)

		if self.the_range_of_images_being_displayed_on_widget[1] > len(dict_img_path):
			self.scroll_boolean_down = False
		elif self.the_range_of_images_being_displayed_on_widget[0] == -len(dict_img_path):
			self.scroll_boolean_up = False
		else:
			self.scroll_boolean_down = True
			self.scroll_boolean_up = True

		pygame.draw.rect(self.window, GREEN, (WIDTH-BLOCK_SIZE, 0, 50, HEIGHT))
		

		for tiles_icon in image_in_file:
			self.window.blit(pygame.transform.scale(for_easy_access[tiles_icon], (40, 40)), (WIDTH-BLOCK_SIZE+5 ,self.y_value*50-self.the_range_of_images_being_displayed_on_widget[1]*50))
			TILES_selected = pygame.Rect(WIDTH-BLOCK_SIZE+5, self.y_value*50-self.the_range_of_images_being_displayed_on_widget[1]*50, 50, 50)
			self.y_value += 1
			if self.mouse_rect.colliderect(TILES_selected):
				if self.clicked_tile:
					self.current_tile_in_in_file = tiles_icon
					self.selected_tile_to_blit = dict_img_path[tiles_icon]

	def save_button(self):
		self.window.blit(self.save_button_image,(0, 100))
		self.save_button_rect = pygame.Rect(0, 100, 100, 30)
		self.mouse_rect2 = pygame.Rect(self.mouse_X_For_Rect, self.mouse_Y_For_Rect, 2, 2)
		if self.mouse_rect2.colliderect(self.save_button_rect):
			if self.clicked_tile:
				self.allow_save = True
			else:
				self.allow_save = False


#------------------------------------------------
#selecter's position and sets image being blitted
#------------------------------------------------
	def selecters_function(self):
		self.check_whether_valid_or_not = int(self.position_of_selecter_of_images[0]+self.position_of_selecter_of_images[1])
		self.selecter_of_image.set_colorkey((BLACK))
		

		if self.scroll == True:
			self.position_of_selecter_of_images[0] = 0
			self.position_of_selecter_of_images[1] = 0
			self.selected_tile_to_blit = ""
			

		elif self.check_whether_valid_or_not > 0 and self.scroll == False:
			self.window.blit(self.selecter_of_image, (self.position_of_selecter_of_images[0], self.position_of_selecter_of_images[1]*BLOCK_SIZE))


	def load_images_on_window(self):
		if len(self.selected_map) >0:
			for data in self.selected_map:
				for tile in self.selected_map[data][0]:
					image = pygame.transform.scale(tile, (BLOCK_SIZE, BLOCK_SIZE))
					image.set_colorkey(color_key)
					self.window.blit(image, (int(self.selected_map[data][2]*BLOCK_SIZE-self.scroll_x), int(self.selected_map[data][1]*BLOCK_SIZE-self.scroll_y)))
					

	def draw_text(self, text, colour, x, y, font_size):
		font = pygame.font.SysFont('comicsans', font_size)
		final_text = font.render(text, 1, colour)
		self.window.blit(final_text, (x, y))


	def copied_tiles_to_be_displayed(self):
		if len(self.copied_tiles) > 0:
			self.available_to_paste_and_delete = True
		else:
			self.available_to_paste_and_delete = False


		pygame.draw.rect(self.window, GREEN, (0, 0, width_of_menu, HEIGHT))
		self.draw_text("copied : ", WHITE, 0, 10, 23)#copied_variable
		self.draw_text(" "+str(self.available_to_paste_and_delete), WHITE, 58, 10, 22)#value_of_copied_variale


#-------------------------------------------
#    all the controls are the
#-------------------------------------------
	def events(self):
		
		self.mouse_x_pos, self.mouse_y_pos = pygame.mouse.get_pos()
		self.mouse_index_in_grid = self.mouse_x_pos , self.mouse_y_pos
		self.mouse_in_widget = self.mouse_y_pos//BLOCK_SIZE, self.mouse_x_pos//BLOCK_SIZE
		self.mouse_index_in_grid_2 = int((self.scroll_x + self.mouse_index_in_grid[0])//BLOCK_SIZE), int((self.scroll_y +self.mouse_index_in_grid[1])//BLOCK_SIZE)
		self.mouse_index_in_widget = (self.mouse_y_pos)//BLOCK_SIZE
		self.mouse_X_For_Rect = self.mouse_index_in_grid[0]
		self.mouse_Y_For_Rect = self.mouse_index_in_grid[1]

		key = pygame.key.get_pressed()
		copied_tiles_lst = []
		img_blitted_on_loc = []
		current_path_in_copied_tile = []
		current_image_in_copied_tile = []
		imge = None

		if self.up == True:
			self.scroll_y += int(self.scroll_speed)

		if self.down == True:
			self.scroll_y -= int(self.scroll_speed)

		if self.left == True:
			self.scroll_x-= int(self.scroll_speed)

		if self.right == True:
			self.scroll_x += int(self.scroll_speed)


		if len(self.selected_tile_to_blit) > 0:
			self.not_empty = True
		else:
			self.not_empty = False

		if self.allow_save == True:
			self.write_to_text_file()
			print("done")

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				self.playing = False
				dict_img_path.clear()
				for_easy_access.clear()
				sys.exit()


			if pygame.mouse.get_pressed()[0]:
				self.click = True
				self.clicked_tile = True
			else:
				self.click = False
				self.clicked_tile = False


			if self.mouse_x_pos > WIDTH-BLOCK_SIZE and self.mouse_x_pos > end_of_values_returned_menu:
				if self.click:
					self.selected_tile_to_blit = ""

					self.position_of_selecter_of_images[0] = WIDTH-BLOCK_SIZE
					self.position_of_selecter_of_images[1] = self.mouse_in_widget[0]


			if self.mouse_x_pos < WIDTH-BLOCK_SIZE and self.mouse_x_pos > end_of_values_returned_menu:
				if ( self.click and event.type == MOUSEMOTION ) or ( self.click ) and self.allow_scaled_selecter == False:
					if self.not_empty:
						loc = str(self.mouse_index_in_grid_2[1])+":"+str(self.mouse_index_in_grid_2[0])
						if loc not in self.selected_map:
							for p in path:
								self.selected_map[loc] = [[for_easy_access[self.current_tile_in_in_file]], self.mouse_index_in_grid_2[1], self.mouse_index_in_grid_2[0], self.rotation, [p], [self.current_tile_in_in_file]]
								self.scroll_speed += 0.1

						elif for_easy_access[self.current_tile_in_in_file] not in self.selected_map[loc][0] and len(self.selected_map[loc][0]) <= 2:
								self.selected_map[loc][0].append(for_easy_access[self.current_tile_in_in_file])
								self.selected_map[loc][-1].append(self.current_tile_in_in_file)
								for pth in path:
									if pth not in self.selected_map[loc][4]:
										self.selected_map[loc][4].append(pth)
								self.scroll_speed += 0.1



				if pygame.mouse.get_pressed()[2]:
					loc = str(self.mouse_index_in_grid_2[1])+":"+str(self.mouse_index_in_grid_2[0])
					try:
						del self.selected_map[loc]
						del self.copied_tiles[self.copied_tiles.index(loc)]
					except:
						pass				

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 5:
					if self.scroll_boolean_down == True:
						self.scroll = True
						self.the_range_of_images_being_displayed_on_widget[0] += 2		
						self.the_range_of_images_being_displayed_on_widget[1] += 2
				else:
					self.scroll = False


				if event.button == 4:
					if self.scroll_boolean_up == True:
						self.scroll = True
						self.the_range_of_images_being_displayed_on_widget[0] -= 2
						self.the_range_of_images_being_displayed_on_widget[1] -= 2
				else:
					self.scroll = False



			if event.type == KEYDOWN:
				if event.key == ord("w"):
					self.up = True

				if event.key ==ord("s"):
					self.down = True

				if event.key == ord("d"):
					self.right = True


				if event.key == ord("a"):
					self.left = True


				if event.key == ord("r"):
					self.allow_scaled_selecter = True


				if event.key == ord("p"):
					pass


				if event.key == ord("c"):
					self.copy = True

				if event.key == ord("g"):
					THICKNESS = 10
					self.switch_grid_on_and_off += 1
				elif self.switch_grid_on_and_off == 2:
					self.switch_grid_on_and_off = 0
					THICKNESS = 0
					


				if event.key ==  K_BACKSPACE:
					if len(self.copied_tiles) > 0:
						for i in self.copied_tiles:
							del self.selected_map[i]
							self.available_to_paste_and_delete = False
						del self.copied_tiles[:]


				if event.key == ord("v"):
					self.paste = True


			if event.type == KEYUP:
				if event.key == ord("w"):
					self.up = False
					

				if event.key ==ord("s"):
					self.down = False
					

				if event.key == ord("d"):
					self.right = False
			

				if event.key == ord("a"):
					self.left = False


				if event.key == ord("r"):
					self.allow_scaled_selecter = False
					self.start_point[0] = 0
					self.start_point[1] = 0


				if event.key == ord("c"):
					self.copy = False


				if event.key == ord("v"):
					self.paste = False


		if self.allow_scaled_selecter == True:
				if self.mouse_x_pos < WIDTH-BLOCK_SIZE and self.mouse_x_pos > end_of_values_returned_menu:
					if self.click == True:
						self.start_point[0] = self.mouse_x_pos #start point x
						self.start_point[1] = self.mouse_y_pos #start point y


		if self.paste == True:
			if self.mouse_x_pos < WIDTH-BLOCK_SIZE and self.mouse_x_pos > end_of_values_returned_menu:
				if self.click == True:
					self.allow_paste = True 
					self.start_copy_position[0] = (self.scroll_x+self.mouse_x_pos)//BLOCK_SIZE
					self.start_copy_position[1] = (self.scroll_y+self.mouse_y_pos)//BLOCK_SIZE
					self.divided_scroll_x = self.scroll_x//BLOCK_SIZE
					self.divided_scroll_y = self.scroll_y//BLOCK_SIZE
				else:
					self.allow_paste = False
		
		if self.allow_paste:
			for tile in self.copied_tiles:
				try:
					self.start_value[0] = int(self.start_copy_position[0]+(int(self.selected_map[tile][2])-self.selected_map[self.copied_tiles[-1]][2]))
					self.start_value[1] = int(self.start_copy_position[1]+(int(self.selected_map[tile][1])-self.selected_map[self.copied_tiles[-1]][1]))


					loc = str(self.start_value[1])+":"+str(self.start_value[0])

					current_path_in_copied_tile = [pth for pth in self.selected_map[tile][4]]
					current_image_in_copied_tile = [img for img in self.selected_map[tile][-1]]
					

					img_blitted_on_loc.clear()
					for image in self.selected_map[tile][-1]:
						if len(self.selected_map[tile][4]) > 1:
							imge = current_path_in_copied_tile[ current_image_in_copied_tile.index(image) ]+"\\"+image
							img_blitted_on_loc.append(imge)

						else:
							imge = current_path_in_copied_tile[0]+"\\"+image
							img_blitted_on_loc.append(imge)


					copied_tiles_lst.clear()
					for copied_tile in img_blitted_on_loc:
						img2 = pygame.image.load(copied_tile)
						copied_tiles_lst.append(img2)

					for copied_tile2 in img_blitted_on_loc:
						for pth in path:
							image_to_blit_2 = pygame.image.load(copied_tile2)
							if len(self.selected_map[tile][-1]) > 1:
								self.selected_map[loc] = [[img.copy() for img in copied_tiles_lst],(self.start_value[1]),(self.start_value[0]),self.rotation,[pth for pth in current_path_in_copied_tile],[img for img in current_image_in_copied_tile]]
							else:
								self.selected_map[loc] = [[image_to_blit_2.copy()],(self.start_value[1]),(self.start_value[0]),self.rotation,[pth],[image]]

				except KeyError:
					continue


		if self.allow_scaled_selecter == True:
			if (self.start_point[0] + self.start_point[1]) > 0:
				pygame.draw.line(self.window,GREEN ,(self.mouse_x_pos,self.start_point[1]), (self.start_point[0],self.start_point[1]), 3)
				pygame.draw.line(self.window,GREEN ,(self.mouse_x_pos,self.mouse_y_pos), (self.start_point[0],self.mouse_y_pos), 3)
				pygame.draw.line(self.window,GREEN ,(self.mouse_x_pos,self.mouse_y_pos), (self.mouse_x_pos,self.start_point[1]), 3)
				pygame.draw.line(self.window,GREEN ,(self.start_point[0],self.mouse_y_pos), (self.start_point[0],self.start_point[1]), 3)	


				if self.copy == True:
					del self.copied_tiles[:]
					for tile in self.selected_map:	
						if self.selected_map[tile][2] < self.mouse_index_in_grid_2[0]+1 and self.selected_map[tile][1] < self.mouse_index_in_grid_2[1] and self.selected_map[tile][2] > (self.scroll_x+self.start_point[0])//BLOCK_SIZE and self.selected_map[tile][1] > (self.scroll_y+self.start_point[1])//BLOCK_SIZE:
							self.copied_tiles.append(tile)

						
						if self.selected_map[tile][2] > self.mouse_index_in_grid_2[0]+1 and self.selected_map[tile][1] > self.mouse_index_in_grid_2[1] and self.selected_map[tile][2] < (self.scroll_x+self.start_point[0])//BLOCK_SIZE and self.selected_map[tile][1] < (self.scroll_y+self.start_point[1])//BLOCK_SIZE:
							self.copied_tiles.append(tile)
						

						if self.selected_map[tile][2] < self.mouse_index_in_grid_2[0]+1 and self.selected_map[tile][1] > self.mouse_index_in_grid_2[1] and self.selected_map[tile][2] > (self.scroll_x+self.start_point[0])//BLOCK_SIZE and self.selected_map[tile][1] < (self.scroll_y+self.start_point[1])//BLOCK_SIZE:
							self.copied_tiles.append(tile)
						

						if self.selected_map[tile][2] > self.mouse_index_in_grid_2[0]+1 and self.selected_map[tile][1] < self.mouse_index_in_grid_2[1] and self.selected_map[tile][2] < (self.scroll_x+self.start_point[0])//BLOCK_SIZE and self.selected_map[tile][1] > (self.scroll_y+self.start_point[1])//BLOCK_SIZE:
							self.copied_tiles.append(tile)


		pygame.display.update()


	def write_to_text_file(self):
		tile_str = ''
		pth_str = ''
		for file in selected_txt_file:
			text_file = open(file, "w+")
			for tile in self.selected_map:
				if len(self.selected_map[tile][-1]) > 1:
					tile_str = ''
					pth_str = ''
					for image in self.selected_map[tile][-1]:
						tile_str += ","+str(image)
						for pth in self.selected_map[tile][4]:
							if (","+pth) != pth_str:
								pth_str += ","+pth
					text_file.write(f"[{tile_str},],{str(self.selected_map[tile][1])},{str(self.selected_map[tile][2])},{self.selected_map[tile][3]},[{pth_str},]"+"*+*")
				else:
					for i in self.selected_map[tile][-1]:
						for pth in self.selected_map[tile][4]:
							text_file.write(f"[,{i},],{str(self.selected_map[tile][1])},{str(self.selected_map[tile][2])},{self.selected_map[tile][3]},[,{pth},]"+"*+*")
							text_file.read()
							text_file.flush()
		end_scroll_speed = open("other/data/scroll speed.txt", "w+")
		end_scroll_speed.write(str(int(self.scroll_speed)))


g = Editor()


while g.running:
	g.loop()
	pygame.image.update()


