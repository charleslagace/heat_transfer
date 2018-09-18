import os
import webbrowser
from random import randint
from tkinter import 

from xlwt import Workbook

from data import Data
from exceptions import HeatmapError, UniformFieldError
from heatmap import Heatmap
from object import Object
from window import Window

class MainInterface(Frame):
	"""Main interface in the heat transfer simulation window.
	Inherits from the Tkinter Frame widget.
	
	Widgets in the interface:
		
	self.root
		Class Tk. Root interface of the simulation. Contains the Menu.
		
	self.objectmenu
		Class Menu. Contains the commands to add of modify an object.
		
	self.settemp
		Classe DoubleVar. Variable of the field temperature entry.
		
	self.temp_label
		Class Label. Text indicating to write the field temperature.
	
	self.temp_entry
		Class Entry. Contains the variable representing the initial
		field temperature.
		
	self.settout
		Classe DoubleVar. Variable of the outside temperature entry.
		
	self.tout_label
		Class Label. Text indicating to write the outside temperature.
	
	self.tout_entry
		Class Entry. Contains the variable representing the outside
		temperature.
	
	self.startbutton
		Class Button. Command to start numerical simulation.
		When pressed, changes text and command to pause simulation.
		When paused, changes text and command to resume simulation.
		When simulation is ended, returns to its original function.
		
	self.endbutton
		Class Button. Command to end numerical simulation.
		Disabled until simulation is started.
		
	self.map
		Class PhotoImage. Contains the actual image for the heatmap
		when simulation is not running Used to initialize the map
		and to show objects before simulation starts.
	
	self.simulation
		Class Label. Contains the heatmap as an image.
		Is modified with the appropriate heatmap at each iteration.
		
	self.dimensions
		Label indicating the dimensions of heatmap.
	
	self.temperature
		Label indicating temperature scaling in heatmap, with the
		widgets self.red_image, seld.red, self.green_image,
		self.green, self.blue_image and self.blue.
		
	
	Other attributes:
	
	self.data
		Data instance which contains the temperature field.
		Initialized when simulation starts, deleted when it ends.
	
	self.heatmap
		Heatmap instance which contains the image where a color is
		calculated for each temperature value in the field.
		Initialized when simulation starts, deleted when it ends.
	
	self.isrunning
		Is True if simulation is running, is False otherwise.
		
	self.temp
		Initial temperature of the field. Is None until a suitable
		temperature is set.
		
	self.tout
		Outside temperature. Is None until a suitable temperature is set.
		
	self.wb
		Workbook object used to export data to an Excel file.
	
	self.ws
		Work sheet used to write data in an Excel file.
	
	self.points
		List of followed points. The temperature at each time incrementation
		will be kept in an Excel file if user used the "Export" command.
	

	Methods defined here:
	
	__init__(self, root):
		MainInterface class builder.
		
	_initmenu(self):
		Method to initialize the menu bar of the interface.
	
	_showerror(self, error):
		Used to show any error that the user may encounter.
	
	addobject(self):
		Command of the "Add Object" option in "Object" menu.
		Creates an Object object to support object creation.
		If created, object is shown on the heatmap.
		
	addpoint(self):	
		Asks user to choose a point that will be followed by
		an Excel worksheet.
		
	addwindow(self):
		Command of the "Add Window" option in "Window" menu.
		Creates a Window object to support window creation.
		
	delobject(self, name):
		Deletes an object and erases it from the heatmap.
	
	delwindow(self, name):
		Deletes a window and erases it from the heatmap.
	
	end(self):
		Command of self.endbutton. Used to end simulation.
		Heatmap will be reinitialized and cannot be recovered.
	
	export(self):
		Export the work sheet to an Excel file for further
		data manipulation.
		
	fieldtemp(self, *args):
		Callback method of the field temperature entry.
		Verifies if the entry can be treated as a number.
		
	fill(self, color):
		Fill image with a color = (r, b, g). Used at
		initialization of interface and at end of simulation.
		
	help(self):	
		Command of "Help" in the main menu. Opens a html 
		page with some guidelines on how to use this program.
		
	newpoint(self):
		Adds a new point to ths list of points for which the
		temperature values will be kept in an Excel work sheet.
		
	outsidetemp(self. *args):	
		Callback method of the outside temperature entry.
		Verifies if the entry can be treated as a number.
	
	pause(self):
		Command to pause simulation.
		
	quit(self):
		Method called when the user interface is closed.
	
	resume(self):
		Command to resume simulation.
		
	run(self):
		Iterate numerical data and update heatmap.
		
	showobject(self, object):	
		Show the object on the heatmap.
		
	showwindow(self, window):
		Show the window on the heatmap.
	
	start(self):	
		Default command of self.startbutton. Starts simulation.
		If no object or window is added, raises UniformFieldError.
		Otherwise, creates the data array and the initial heatmap.
		
	todelete_object(self):
		Allows user to choose the object he wants to delete.
		
	todelete_window(self):
		Allows user to choose the window he wants to delete.
	
	tomodify_object(self):
		Allows user to choose the object he wants to modify.
	
	tomodify_window(self):
		Allows user to choose the window he wants to modify.
		
	
	Exceptions handled:
	
	AttributeError
		When user attempts to start simulation without any value
		for the field temperature or the outside temperature.
		
	ValueError
		When the field temperature entry is either physically
		impossible or unsuitable for the simulation.
		
	UniformFieldError
		When user tries to start simulation with no object or window.
	"""
	
	def __init__(self, root):
		"""MainInterface class builder."""
		
		Frame.__init__(self, root)
		
		self.root = root
		self.root.title("Heat Transfer Simulation")
		
		self._initmenu()
		
		self.settemp = StringVar()
		self.temp_label = Label(self, text="Set Temperature in Field : ")
		self.temp_label.grid(row=0, column=1, columnspan=2, sticky=E)
		self.temp_entry = Entry(self, textvariable=self.settemp, width=10)
		self.temp_entry.grid(row=0, column=3, sticky=W)
		self.settemp.trace("w", self.fieldtemp)
		
		self.settout = StringVar()
		self.tout_label = Label(self, text="Set Temperature Outside : ")
		self.tout_label.grid(row=1, column=1, columnspan=2, sticky=E)
		self.tout_entry = Entry(self, textvariable=self.settout, width=10, state=DISABLED)
		self.tout_entry.grid(row=1, column=3, sticky=W)
		self.settout.trace("w", self.outsidetemp)
		
		self.startbutton = Button(self, text="Start Simulation", command=self.start, fg="green", width=13)
		self.startbutton.grid(row=2, column=1)
		self.endbutton = Button(self, text="End Simulation", command=self.end, fg="grey", width=13, state=DISABLED)
		self.endbutton.grid(row=2, column=2, columnspan=2)
		
		self.map = PhotoImage(width=Data.nb_x, height=Data.nb_y)
		self.fill(self.map, (255, 255, 255))
		self.simulation = Label(self, image=self.map)
		self.simulation.grid(row=3, rowspan=4, column=1, columnspan=3)
		
		self.dimensions = Label(self, text="""Dimensions:
		\nx-axis: {} m
		\ny-axis: {} m""".format(Data.dx * Data.nb_x, Data.dy * Data.nb_y))
		self.dimensions.grid(row=0, rowspan=3, column=4)
		
		self.temperature = Label(self, text="Temperature:")
		self.temperature.grid(row=3, column=4)
		self.red_image = PhotoImage(file="/Users/Guy/Desktop/Projets/Python/Heat Transfer Simulations/image/red.gif")
		self.red = Label(self, image=self.red_image, text=" = 0.0 K  ", compound=LEFT)
		self.red.grid(row=4, column=4)
		self.green_image = PhotoImage(file="/Users/Guy/Desktop/Projets/Python/Heat Transfer Simulations/image/green.gif")
		self.green = Label(self, image=self.green_image, text=" = 0.0 K  ", compound=LEFT)
		self.green.grid(row=5, column=4)
		self.blue_image = PhotoImage(file="/Users/Guy/Desktop/Projets/Python/Heat Transfer Simulations/image/blue.gif")
		self.blue = Label(self, image=self.blue_image, text=" = 0.0 K  ", compound=LEFT)
		self.blue.grid(row=6, column=4)
		
		self.grid(sticky=W+E+N+S)
		
		self.isrunnung = False
		self.temp = None
		self.tout = None
		
		self.wb = Workbook()
		self.ws = self.wb.add_sheet("Simulation1")
		self.nb_simulation = 1
		self.points = []
		
	def _initmenu(self):
		"""Method to initialize the menu bar of the interface."""
		
		menubar = Menu(self.root)
		self.root.config(menu=menubar)
		
		self.filemenu = Menu(menubar)
		self.filemenu.add_command(label="Follow Point", underline=7, command=self.addpoint)
		self.filemenu.add_command(label="Export Data", underline=0, command=self.export)
		
		self.objectmenu = Menu(menubar)
		self.objectmenu.add_command(label="Add Object", underline=0, command=self.addobject)
		
		self.windowmenu = Menu(menubar)
		self.windowmenu.add_command(label="Add Window", command=self.addwindow)
		
		menubar.add_cascade(label="File", underline=0, menu=self.filemenu)
		menubar.add_cascade(label="Object", underline=0, menu=self.objectmenu)
		menubar.add_cascade(label="Window", underline=0, menu=self.windowmenu)
		menubar.add_command(label="Help", underline=0, command=self.help)
		
	def _showerror(self, error):
		"""Used to show any error that the user may encounter."""
	
		top = Toplevel()
		top.title("Error")
		
		msg = Message(top, text=error, aspect=500, justify=CENTER)
		msg.grid()
		
		button = Button(top, text="OK", command=top.destroy)
		button.grid()
		
	def addobject(self):
		"""Command of the "Add Object" option in "Object" menu.
		Creates an Object object to support object creation.
		"""
		
		newobj = Object(self)
		newobj.config()
		
	def addpoint(self):
		"""Asks user to choose a point that will be followed.
		Each temperature value of this point will be written in
		an Excel worksheet that can be saved with the "Export"
		command.
		"""
		
		self.top = Toplevel()
		self.top.title("Follow Point")
		
		self.name = StringVar(value="Point{}".format(len(self.points) + 1))
		name_label = Label(self.top, text="Point name:", width=15)
		name_entry = Entry(self.top, textvariable=self.name, width=15)
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
		
		follow = Button(self.top, text="Follow Point", command=self.newpoint)
		follow.grid(row=3, column=2)
		
	def addwindow(self):
		"""Command of the "Add Window" option in "Window" menu.
		Creates a Window object to support window creation.
		"""
		
		newwindow = Window(self)
		newwindow.config()
		
	def delobject(self, name):
		"""Deletes an object and erases it from the heatmap."""
		
		for object in Object.objects:
			if object["name"] == name:
				i = object["left"]
				while i <= object["right"]:
					self.map.put("white", (i, object["bottom"]))
					self.map.put("white", (i, object["top"]))
					i += 1
				
				j = object["top"]
				while j <= object["bottom"]:
					self.map.put("white", (object["left"], j))
					self.map.put("white", (object["right"], j))
					j += 1
				
				self.simulation["image"] = self.map
				
		Object.objects = [object for object in Object.objects if object["name"] != name]
		
		if Object.objects == []:
			self.objectmenu.delete("Modify Object")
			self.objectmenu.delete("Delete Object")
			
	def delwindow(self, name):
		"""Deletes a window and erases it from the heatmap."""
		
		for window in Window.windows:
			if window["name"] == name:
				if window["side"].lower() == "left" or window["side"].lower() == "right":
					if window["side"].lower() == "left":
						i = 0
					elif window["side"].lower() == "right":
						i = Data.nb_x - 1
					j = window["min"]
					while j <= window["max"]:
						self.map.put("white", (i, j))
						self.map.put("white", (i, j))
						j += 1
			
				elif window["side"].lower() == "top" or window["side"].lower() == "bottom":
					if window["side"].lower() == "top":
						j = 0
					elif window["side"].lower() == "bottom":
						j = Data.nb_y - 1
					i = window["min"]
					while i <= window["max"]:
						self.map.put("blue", (i, j))
						self.map.put("blue", (i, j))
						i += 1
		
		Window.windows = [window for window in Window.windows if window["name"] != name]
		
		if Window.windows == []:
			self.windowmenu.delete("Modify Window")
			self.windowmenu.delete("Delete Window")
	
	def end(self):
		"""Command of self.endbutton. Used to end simulation.
		Heatmap will be reinitialized and cannot be recovered.
		"""
	
		self.isrunning = False
		self.points = []
		del self.data
		del self.heatmap

		self.nb_simulation += 1
		self.ws = self.wb.add_sheet("Simulation{}".format(self.nb_simulation))
		
		self.temp = None
		self.tout = None
		self.settemp.set("")
		self.settout.set("")
		self.temp_entry["state"] = NORMAL
		self.tout_entry["state"] = DISABLED
		self.endbutton.config(fg="grey", state=DISABLED)
		self.startbutton.config(text="Start Simulation", command=self.start, fg="green")
		self.objectmenu.entryconfig(1, state=NORMAL)
		self.windowmenu.entryconfig(1, state=NORMAL)
		
		try:
			self.objectmenu.delete("Modify Object")
			self.objectmenu.delete("Delete Object")
			self.windowmenu.delete("Modify Window")
			self.windowmenu.delete("Delete Window")
		except TclError:
			pass
		
		self.map = PhotoImage(width=Data.nb_x, height=Data.nb_y)
		self.fill(self.map, (255, 255, 255))
		self.simulation["image"] = self.map
		
	def export(self):
		"""Export the work sheet to an Excel file for further
		data manipulation."""
		
		filename = str(randint(1, 9999999999))
		self.wb.save(filename + ".xls")
		
	def fieldtemp(self, *args):
		"""Callback method of the field temperature entry.
		Verifies if the entry can be treated as a number.
		"""
		
		try:
			temp = float(self.settemp.get())
			assert temp >= 0
			
		except ValueError:
			if self.settemp.get() is "" or self.settemp.get() is "-":
				pass
			else:
				try:
					raise ValueError("Field temperature must be an integer or decimal number.")
				except ValueError as error:
					self._showerror(error)
		
		except AssertionError:
			try:
				raise ValueError("Field temperature must be in Kelvin and no less than absolute zero.")
			except ValueError as error:
				self._showerror(error)
		
		else:
			self.temp = temp
		
	def fill(self, image, color):
		"""Fill image with a color in (r, g, b) format. Used at
		initialization of interface and at end of simulation.
		"""
	
		r, g, b = color
		width = image.width()
		height = image.height()
		hexcode = "#%02x%02x%02x" % (r, g, b)
		horizontal_line = "{" + " ".join([hexcode] * width) + "}"
		image.put(" ".join([horizontal_line] * height))
		
	def help(self):
		"""Command of "Help" in the main menu. Opens a html 
		page with some guidelines on how to use this program.
		"""
		
		webbrowser.open("file://" + os.path.realpath("help.html"))
		
	def newpoint(self):
		"""Adds a new point to ths list of points for which the
		temperature values will be kept in an Excel work sheet.
		"""
		
		name = self.name.get()
		
		try:
			xpos = self.xpos.get()
			ypos = self.ypos.get()
			ipos = round(xpos/Data.dx)
			jpos = Data.nb_y - round(ypos/Data.dy)
			
			if not 0 <= ipos < Data.nb_x or not 0 <= jpos < Data.nb_y:
				raise HeatmapError("The point {} must be in the visible heatmap.".format(name))
					
		except TclError:
			try:
				raise ValueError("The x- and y- positions of point {} need to be integers or decimal numbers.".format(name))
			except ValueError as error:
				self._showerror(error)
				
		except HeatmapError as error:
			self._showerror(error)
			
		else:
			self.ws.write(0, len(self.points) + 1, name)
			self.points.append((ipos, jpos))
			self.top.destroy()
		
	def outsidetemp(self, *args):
		"""Callback method of the outside temperature entry.
		Verifies if the entry can be treated as a number.
		"""
		
		try:
			tout = float(self.settout.get())
			assert tout >= 0
			
		except ValueError:
			if self.settout.get() is "" or self.settout.get() is "-":
				pass
			else:
				try:
					raise ValueError("Outside temperature must be an integer or decimal number.")
				except ValueError as error:
					self._showerror(error)
		
		except AssertionError:
			try:
				raise ValueError("Outside temperature must be in Kelvin and no less than absolute zero.")
			except ValueError as error:
				self._showerror(error)
		
		else:
			self.tout = tout
	
	def pause(self):
		"""Command to pause simulation."""
		
		self.isrunning = False
		self.startbutton.config(text="Resume Simulation", command=self.resume, fg="green")
		
	def quit(self):
		"""Method called when the user interface is closed."""
		
		self.wb.close()
		Misc.quit(self)
		
	def resume(self):
		"""Command to resume simulation."""
	
		self.isrunning = True
		self.startbutton.config(text="Pause Simulation", command=self.pause, fg="red")
		self.run()
		
	def run(self):
		"""Iterate numerical data and update heatmap."""
		
		n = 1
		while self.isrunning:
			self.ws.write(n, 0, n * Data.dt)
			for i, p in enumerate(self.points):
				self.ws.write(n, i + 1, self.data.field[p[1]][p[0]])
			self.data.iterate()
			self.simulation["image"] = self.heatmap.get(self.data.field)
			self.update()
			n += 1
			
	def showobject(self, object):
		"""Show the object on the heatmap."""
		
		if Object.objects == []:
				self.objectmenu.add_command(label="Modify Object", underline=0, command=self.tomodify_object)
				self.objectmenu.add_command(label="Delete Object", underline=0, command=self.todelete_object)
			
		i = object["left"]
		while i <= object["right"]:
			self.map.put("red", (i, object["bottom"]))
			self.map.put("red", (i, object["top"]))
			i += 1
				
		j = object["top"]
		while j <= object["bottom"]:
			self.map.put("red", (object["left"], j))
			self.map.put("red", (object["right"], j))
			j += 1
				
		self.simulation["image"] = self.map
		
	def showwindow(self, window):
		"""Show the window on the heatmap."""
		
		if Window.windows == []:
				self.windowmenu.add_command(label="Modify Window", command=self.tomodify_window)
				self.windowmenu.add_command(label="Delete Window", command=self.todelete_window)
				self.tout_entry["state"] = NORMAL
			
		if window["side"].lower() == "left" or window["side"].lower() == "right":
			if window["side"].lower() == "left":
				i = 0
			elif window["side"].lower() == "right":
				i = Data.nb_x - 1
			j = window["min"]
			while j <= window["max"]:
				self.map.put("blue", (i, j))
				self.map.put("blue", (i, j))
				j += 1
			
		elif window["side"].lower() == "top" or window["side"].lower() == "bottom":
			if window["side"].lower() == "top":
				j = 0
			elif window["side"].lower() == "bottom":
				j = Data.nb_y - 1
			i = window["min"]
			while i <= window["max"]:
				self.map.put("blue", (i, j))
				self.map.put("blue", (i, j))
				i += 1
				
		self.simulation["image"] = self.map
	
	def start(self):
		"""Default command of self.startbutton. Starts simulation.
		If no object has been added by user, raises NoObjectError.
		Otherwise, creates the data array and the initial heatmap.
		"""
		
		if Object.objects == [] and Window.windows == []:
			try:
				raise UniformFieldError("At least one object or window must be added to start simulation.")
			except UniformFieldError as error:
				self._showerror(error)
		
		elif self.temp is None:
			try:
				raise AttributeError("Value not found for the field temperature.")
			except AttributeError as error:
				self._showerror(error)
		
		elif self.tout is None and Window.windows != []:
			try:
				raise AttributeError("Value not found for the outside temperature.")
			except AttributeError as error:
				self._showerror(error)
		
		else:
			self.objectmenu.entryconfig(1, state=DISABLED)
			self.objectmenu.entryconfig(2, state=DISABLED)
			self.objectmenu.entryconfig(3, state=DISABLED)
			self.windowmenu.entryconfig(1, state=DISABLED)
			self.windowmenu.entryconfig(2, state=DISABLED)
			self.windowmenu.entryconfig(3, state=DISABLED)
			self.temp_entry["state"] = "readonly"
			self.tout_entry["state"] = "readonly"
			
			if self.tout is None:
				self.tout = self.temp
			self.data = Data(self.temp, self.tout, Object.objects, Window.windows)
			Object.objects = []
			Window.windows = []
			self.heatmap = Heatmap(self.data.range, self.data.haswindow)
			self.simulation["image"] = self.heatmap.get(self.data.field)			
			
			self.red["text"] = " = {} K".format(str(round(self.heatmap.red))[:5])
			self.green["text"] = " = {} K".format(str(round(self.heatmap.green))[:5])
			self.blue["text"] = " = {} K".format(str(round(self.heatmap.blue))[:5])
			self.startbutton.config(text="Pause Simulation", command=self.pause, fg="red")
			self.endbutton.config(fg="red", state=NORMAL)
			
			self.ws.write(0,0, "t")
			self.isrunning = True
			self.update_idletasks()
			self.run()
			
	def todelete_object(self):
		"""Allows user to choose the object he wants to delete."""
		
		newobj = Object(self)
		
		newobj.top = Toplevel()
		newobj.top.title("Delete Object")
		
		text = Label(newobj.top, text="Which object do you want to delete?")
		text.pack()
		
		def choose():
			delete_button["state"] = NORMAL
		
		newobj.name = StringVar()
		for object in Object.objects:
			radio = Radiobutton(newobj.top, text=object["name"], variable=newobj.name, value=object["name"], command=choose)
			radio.pack()
		
		delete_button = Button(newobj.top, text="Delete Object", command=newobj.delete, state=DISABLED)
		delete_button.pack()
		
	def todelete_window(self):
		"""Allows user to choose the window he wants to delete."""
		
		newwindow = Window(self)
		
		newwindow.top = Toplevel()
		newwindow.top.title("Delete Window")
		
		text = Label(newwindow.top, text="Which window do you want to delete?")
		text.pack()
		
		def choose():
			modify_button["state"] = NORMAL
		
		newwindow.name = StringVar()
		for window in Window.windows:
			radio = Radiobutton(newwindow.top, text=window["name"], variable=newwindow.name, value=window["name"], command=choose)
			radio.pack()
		
		modify_button = Button(newwindow.top, text="Delete Window", command=newwindow.delete, state=DISABLED)
		modify_button.pack()
	
	def tomodify_object(self):
		"""Allows user to choose the object he wants to modify."""
		
		newobj = Object(self)
		
		newobj.top = Toplevel()
		newobj.top.title("Modify Object")
		
		text = Label(newobj.top, text="Which object do you want to modify?")
		text.pack()
		
		def choose():
			modify_button["state"] = NORMAL
		
		newobj.name = StringVar()
		for object in Object.objects:
			radio = Radiobutton(newobj.top, text=object["name"], variable=newobj.name, value=object["name"], command=choose)
			radio.pack()
		
		modify_button = Button(newobj.top, text="Modify Object", command=newobj.modify, state=DISABLED)
		modify_button.pack()
		
	def tomodify_window(self):
		"""Allows user to choose the window he wants to modify."""
		
		newwindow = Window(self)
		
		newwindow.top = Toplevel()
		newwindow.top.title("Modify Window")
		
		text = Label(newwindow.top, text="Which window do you want to modify?")
		text.pack()
		
		def choose():
			modify_button["state"] = NORMAL
		
		newwindow.name = StringVar()
		for window in Window.windows:
			radio = Radiobutton(newwindow.top, text=window["name"], variable=newwindow.name, value=window["name"], command=choose)
			radio.pack()
		
		modify_button = Button(newwindow.top, text="Modify Window", command=newwindow.modify, state=DISABLED)
		modify_button.pack()