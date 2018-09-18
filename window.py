from tkinter import *

from data import Data
from exceptions import HeatmapError, OverlapError

class Window:
	"""Class designed to create, modify or delete a
	window for the heat transfer numerical simulation.
	
	Instance attributes:
	
	self.interface
		MainInterface object from which the Window is 
		created. Used to call some methods of the
		MainInterface class.
	
	self.top
		Window used to configure, modify or delete a
		window.
	
	self.dict
		A dictionary which contains the name, the side
		and the position of both edges of the window.
		
	self.name
		Class StringVar. Contains the Window name.
		
	self.side
		Class StringVar. Controls whether the window will
		be on the right, left, top or bottom edge of heatmap.
		
	self.min
		Class DoubleVar. Lower or left edge of the window.
		
	self.max
		Class DoubleVar. Upper or right edge of the window.
		
		
	Class attribute:
	
	Window.windows
		List of created windows, where each window has a
		dictionary containing its name, its side, its
		minimum position ans its maximum position.
	
	
	Methods defined here:
	
	__init__(self):
		Window class builder.
		
	config(self):
		Shows the window creation window. Asks user to choose
		name, side, lower of left edge, and upper or right edge.
		
	create(self):
		Handles all the necessary exceptions. If all
		conditions are satisfied, creates a new window.
		
	delete(self):
		Method to delete a window.
		
	modify(self):	
		Method to modify a window. Will delete the chosen
		window then ask the user to create a new one.
		
	
	Exceptions handled:
		
	HeatmapError
		When any window is not entirely contained in the heatmap.
		
	NameError
		When the user tries to give two windows the same name.
		
	OverlapError
		When two windows are overlapping in the heatmap.
		
	ValueError
		When a window parameter is unsuitable for the simulation.
	"""
	
	windows = []
	
	def __init__(self, interface):
		"""Window class builder."""
		
		self.interface = interface
		self.dict = {}
		
	def config(self):
		"""Shows the window creation window. Asks user to choose
		name, side, lower of left edge, and upper or right edge.
		"""
		
		self.top = Toplevel()
		self.top.title("New Window")
		
		self.name = StringVar(value="Window{}".format(len(Window.windows) + 1))
		name_label = Label(self.top, text="Name:", width=10)
		name_entry = Entry(self.top, textvariable=self.name, width=20)
		name_label.grid(row=0, column=0)
		name_entry.grid(row=0, column=1, columnspan=2)
		
		self.side = StringVar(value="left")
		side_label = Label(self.top, text="Side:", width=20)
		side_entry = Entry(self.top, textvariable=self.side, width=10)
		side_label.grid(row=1, column=0, columnspan=2)
		side_entry.grid(row=1, column=2)

		self.min = DoubleVar()
		min_label = Label(self.top, text="Lower/left edge:", width=20)
		min_entry = Entry(self.top, textvariable=self.min, width=10)
		min_label.grid(row=2, column=0, columnspan=2)
		min_entry.grid(row=2, column=2)
		
		self.max = DoubleVar()
		max_label = Label(self.top, text="Upper/right edge:", width=20)
		max_entry = Entry(self.top, textvariable=self.max, width=10)
		max_label.grid(row=3, column=0, columnspan=2)
		max_entry.grid(row=3, column=2)
		
		side_help = Label(self.top, text="Side should be left, right, top or bottom.", anchor=W, width=30)
		side_help.grid(row=4, column=0, columnspan=3)
		
		create = Button(self.top, text="Create Window", command=self.create)
		create.grid(row=5, column=2)
		
	def create(self):
		"""Handles all the necessary exceptions. If all
		conditions are satisfied, creates a new window.
		"""
		
		name = self.name.get()
		side = self.side.get()
		
		try:
			min_entry = self.min.get()
			max_entry = self.max.get()
			
			if side.lower() == "left" or side.lower() == "right":
				max = Data.nb_y - round(min_entry/Data.dy)
				min = Data.nb_y - round(max_entry/Data.dy)
				if min <= 0 or max >= Data.nb_y:
					raise HeatmapError("The window {} must be entirely contained in the {} border of heatmap.".format(name, side.lower()))
			
			elif side.lower() == "top" or side.lower() == "bottom":
				min = round(min_entry/Data.dx)
				max = round(max_entry/Data.dx)
				if min <= 0 or max >= Data.nb_x:
					raise HeatmapError("The window {} must be entirely contained in the {} border of heatmap.".format(name, side.lower()))
			
			else:
				raise ValueError("Side must be one of the following: left, right, top or bottom.")
				
			for w in Window.windows:
				if w["name"] == name:
					raise NameError("Another window already has the name {}".format(name))
				
				elif w["side"] == side:
					if w["min"] <= min <= w["max"] or w["min"] <= max <= w["max"]:
						raise OverlapError("Two windows are overlapping: {} and {}".format(w["name"], name))
				
		except TclError:
			try:
				raise ValueError("The lower/left and upper/right edges of window {} need to be integers or decimal numbers.".format(name))
			except ValueError as error:
				self.interface._showerror(error)
					
		except ValueError as error:
			self.interface._showerror(error)
				
		except HeatmapError as error:
			self.interface._showerror(error)
			
		except NameError as error:
			self.interface._showerror(error)
			
		except OverlapError as error:
			self.interface._showerror(error)
				
		else:
			self.dict["name"] = name
			self.dict["side"] = side
			self.dict["min"] = min
			self.dict["max"] = max
		
			self.top.destroy()
			self.interface.showwindow(self.dict)
			Window.windows.append(self.dict)
		
	def delete(self):
		"""Method to delete an object."""
		
		name = self.name.get()
		
		self.top.destroy()
		self.interface.delwindow(name)
		
	def modify(self):
		"""Method to modify a window. Will delete the chosen
		window then ask the user to create a new one.
		"""
		
		self.delete()
		return self.config()