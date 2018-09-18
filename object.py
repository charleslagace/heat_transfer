from tkinter import *

from data import Data
from exceptions import HeatmapError, OverlapError

class Object:
	"""Class designed to create, modify or delete an
	object for the heat transfer numerical simulation.
	
	Instance attributes:
	
	self.interface
		MainInterface object from which the Object is 
		created. Used to call some methods of the
		MainInterface class.
	
	self.top
		Window used to configure, modify or delete an
		object.
	
	self.dict
		A dictionary which contains the name, the left
		and right i-values, the top and bottom j-values
		as well as the temperature of the new object.
		
	self.name
		Class StringVar. Contains the object name.
		
	self.xpos
		Class DoubleVar. Position of object on the x-axis.
		
	self.ypos
		Class DoubleVar. Position of object on the y-axis.
		
	self.xdim
		Class DoubleVar. Horizontal dimension of object.
		
	self.ydim
		Class DoubleVar. Vertical dimension of object.
		
	self.T
		Class DoubleVar. Temperature of object.
		
	Class attribute:
	
	Object.objects
		List of created objects.
		Each object has a dictionary with the following keys:
			name, x-pos, y-pos, x-dim, y-dim and T.
	
	
	Methods defined here:
	
	__init__(self):
		Object class builder.
		
	config(self):
		Shows the object creation window. Asks user to choose
		name, x-pos, y-pos, x-dim, y-dim and T of object.
		
	create(self):
		Handles all the necessary exceptions. If all
		conditions are satisfied, creates a new object.
		
	delete(self):
		Method to delete an object.
		
	modify(self):	
		Method to modify an object. Will delete the chosen
		object then ask the user to create a new one.
		
	
	Exceptions handled:
		
	HeatmapError
		When any object is not entirely contained in the heatmap.
		
	NameError
		When the user tries to give two objects the same name.
		
	OverlapError
		When two objects are overlapping in the heatmap.
		
	ValueError
		When any object parameter is either physically impossible
		or unsuitable for the simulation.
	"""
	
	objects = []
	
	def __init__(self, interface):
		"""Object class builder."""
		
		self.interface = interface
		self.dict = {}
		
	def config(self):
		"""Shows the object creation window. Asks user to choose
		name, x-pos, y-pos, x-dim, y-dim and T of object.
		"""
		
		self.top = Toplevel()
		self.top.title("New Object")
		
		self.name = StringVar(value="Object{}".format(len(Object.objects) + 1))
		name_label = Label(self.top, text="Name:", width=10)
		name_entry = Entry(self.top, textvariable=self.name, width=20)
		name_label.grid(row=0, column=0)
		name_entry.grid(row=0, column=1, columnspan=2)
		
		self.xpos = DoubleVar()
		xpos_label = Label(self.top, text="x-position:", width=20)
		xpos_entry = Entry(self.top, textvariable=self.xpos, width=10)
		xpos_label.grid(row=1, column=0, columnspan=2)
		xpos_entry.grid(row=1, column=2)

		self.ypos = DoubleVar()
		ypos_label = Label(self.top, text="y-position:", width=20)
		ypos_entry = Entry(self.top, textvariable=self.ypos, width=10)
		ypos_label.grid(row=2, column=0, columnspan=2)
		ypos_entry.grid(row=2, column=2)
		
		self.xdim = DoubleVar()
		xdim_label = Label(self.top, text="x-dimension:", width=20)
		xdim_entry = Entry(self.top, textvariable=self.xdim, width=10)
		xdim_label.grid(row=3, column=0, columnspan=2)
		xdim_entry.grid(row=3, column=2)
		
		self.ydim = DoubleVar()
		ydim_label = Label(self.top, text="y-dimension:", width=20)
		ydim_entry = Entry(self.top, textvariable=self.ydim, width=10)
		ydim_label.grid(row=4, column=0, columnspan=2)
		ydim_entry.grid(row=4, column=2)
		
		self.T = DoubleVar()
		T_label = Label(self.top, text="Temperature:", width=20)
		T_entry = Entry(self.top, textvariable=self.T, width=10)
		T_label.grid(row=5, column=0, columnspan=2)
		T_entry.grid(row=5, column=2)
		
		create = Button(self.top, text="Create Object", command=self.create)
		create.grid(row=6, column=2)
		
	def create(self):
		"""Handles all the necessary exceptions. If all
		conditions are satisfied, creates a new object.
		"""
		
		name = self.name.get()
		
		try:
			xpos = self.xpos.get()
			ypos = self.ypos.get()
			xdim = self.xdim.get()
			ydim = self.ydim.get()
			T = self.T.get()
				
			assert T >= 0
			
			ipos = round(xpos/Data.dx)
			jpos = Data.nb_y - round(ypos/Data.dy)
			idim = xdim/Data.dx
			jdim = ydim/Data.dy
			
			left = ipos - round(idim/2)
			right = ipos + round(idim/2)
			top = jpos - round(jdim/2)
			bottom = jpos + round(jdim/2)
			
			if left <= 0 or top <= 0 or right >= Data.nb_x or bottom >= Data.nb_y:
				raise HeatmapError("The object {} must be entirely contained in the visible heatmap.".format(name))
				
			for o in enumerate(Object.objects):
				if o["name"] == name:
					raise NameError("Another object already has the name {}".format(name))
				
				elif o["left"] <= left <= o["right"] or o["left"] <= right <= o["right"]:
					raise OverlapError("Two objects are overlapping on the x-axis: {} and {}".format(o["name"], name))
				elif o["top"] <= top <= o["bottom"] or o["top"] <= bottom <= o["bottom"]:
					raise OverlapError("Two objects are overlapping on the y-axis: {} and {}".format(o["name"], name))
				
		except TclError:
			try:
				raise ValueError("All parameters of object {} (except its name) need to be an integer or decimal number.".format(name))
			except ValueError as error:
				self.interface._showerror(error)
					
		except AssertionError:
			try:
				raise ValueError("Temperature of object {} must be in Kelvin and no less than absolute zero.".format(name))
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
			self.dict["left"] = left
			self.dict["right"] = right
			self.dict["top"] = top
			self.dict["bottom"] = bottom
			self.dict["T"] = T
			
			self.top.destroy()
			self.interface.showobject(self.dict)
			Object.objects.append(self.dict)
		
	def delete(self):
		"""Method to delete an object."""
		
		name = self.name.get()
		
		self.top.destroy()
		self.interface.delobject(name)
		
	def modify(self):
		"""Method to modify an object. Will delete the chosen
		object then ask the user to create a new one.
		"""
		
		self.delete()
		return self.config()