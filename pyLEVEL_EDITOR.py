
import pygame
import os
from init.CONFIGURATIONS.CONFIGURATIONS import *
from copy import deepcopy
import tkinter
from tkinter.ttk import *
from tkinter import messagebox, scrolledtext
from tkinter import *
from tkinter import filedialog



class GUI:
	def __init__( self ):
		self.window = Tk()
		self.window.geometry( "200x200" )
		self.window.title( "Map editor" )
		self.window.iconbitmap("other/data/icons/Papirus-Team-Papirus-Mimetypes-App-x-plasma.ico")
		self.ImagePath =False
		self.text_file = False
		self.correct_length = True
		self.create = False


	def data_entry( self ):

		def load_file():
			self.file  = filedialog.askopenfilename( initialdir = "/", 
				title = "Select a Text file", 
				filetypes = (( "text files", "*.txt" ), ( "all files", "*.*" )) )
			
			try:

				self.txtfile = open(self.file, "r")
				verify_file = self.txtfile.read()

			except FileNotFoundError:
				pass
			selected_txt_file.append(str(self.file))



		self.load_file_button = Button( self.window, 
			text = "load file", 
			command = load_file, 
			width = 13 )


		self.load_file_button.grid( column = 0 , row = 0 )


		def create_file():
			self.root = Toplevel()
			self.root.geometry( "300x100" )
			self.file_name = Entry( self.root, width = 13 )


			def this_creates_text_file():
				self.created_file = open( str( self.file_name.get() )+".txt", "w" )
				self.filecreated = True
				self.created_file.close()
				self.root.destroy()


			save_name = Button( self.root,
				text = "save filename", 
				command = this_creates_text_file )


			save_name.grid( column = 2, row = 0 )
			self.file_name.grid( column = 1, row = 0 )
			self.enter_filename_label = Label(self.root, 
				text = "Enter file name:", 
				bg = "red", 
				fg = "white")


			self.enter_filename_label.grid(column = 0, row = 0)


		self.create_file_button = Button( self.window, 
			text = "create new file", 
			command = create_file, 
			width = 13 )


		self.create_file_button.grid( column = 1 , row = 0 )


		def open_visuale_map_editor(): 
			allow_import = False

			if len(selected_txt_file) > 0:
				self.text_file = True
			if len(dict_img_path) > 0:
				self.ImagePath = True

			if self.text_file == True and self.ImagePath == True:
				allow_import = True
			else:
				if self.text_file == False:
					allow_import = False
					messagebox.showerror("Error", "load text file")
				if self.ImagePath == False:
					allow_import = False
					messagebox.showerror("Error", "Enter image path")
					
			if allow_import == True:
				import init.init
				for boolean in playing:
					if boolean == False:
						self.window.destroy()


		self.next_module = Button( self.window, 
			text = "Next", 
			background = "Blue", 
			foreground = "white", 
			command = open_visuale_map_editor, 
			width = 13 )


		self.next_module.grid( column = 1, row = 1 )


		def load_img_GUI():
			self.load_img_window = Toplevel()
			self.load_img_window.geometry( "300x100" )
			self.load_img_window.title( "load_image" )
			self.enter_path = Entry( self.load_img_window )
			self.enter_path.grid( column = 1, row = 0 )


			def load_images_function():
				a = self.enter_path.get()
				try:
					del path[:]
					path.append(a)
					self.path = os.listdir( a )
					for file in self.path:
						if file[-4:] == ".png":
							image_in_file.append(str(file))
							image = pygame.image.load(str(a)+"\\"+str(file))
							image.set_colorkey(color_key)
							for_easy_access[file] = image.copy()
							dict_img_path[file] = str(a)+"\\"+str(file)
							self.load_img_window.destroy()
							
				except FileNotFoundError:
					messagebox.showerror("Error", "Enter a valid directory")


			self.enter_directory_label = Label(self.load_img_window, 
				text = "Enter image directory: ", 
				bg = "red",
				fg = "white")


			self.enter_directory_label.grid(column = 0, row = 0)
			self.done_button = Button( self.load_img_window, 
				text = "Done", 
				bg = "light green",
				command = load_images_function )


			self.done_button.grid( column = 2, row = 0 )


		self.load_img = Button( self.window, 
			text = "load images", 
			width = 13, 
			command = load_img_GUI )

		
		self.load_img.grid( column=0, row=1 )

		self.if_you_want_label = Label(self.window, text="If you want:", bg="Red", fg="White", width=30)
		self.if_you_want_label.grid( column = 0, row = 2, columnspan = 100)


		def how_to_play():
			self.file = open(How_to_play_variable, "r")
			self.htp_window = Toplevel()
			self.htp_window.geometry("1000x600")

			output_window = scrolledtext.ScrolledText(self.htp_window, width=600, height = 200)
			output_window.grid(column= 0, row=0)
			output_window.insert(tkinter.INSERT, self.file.read())


		self.load_howto_play = Button(self.window, text= "how to USE", width=30, bg= "green", command= how_to_play)
		self.load_howto_play.grid(column=0, row=4, columnspan=100)


	def mainloop( self ):
		self.data_entry()
		self.window.mainloop()




app = GUI()
app.mainloop()


