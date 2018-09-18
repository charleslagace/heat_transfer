class Data:
	"""Class designed to manipulate numerical data.

	Instance attributes:
	
	self.field
		2-dimensional temperature field represented with a 200 x 200 array.
		The initial field is generated when simulation starts.
		New T-values in field are generated while simulation is running.
		
	self.range
		A tuple containing the temperature extremums in field.
		
	self.haswindow
		List containing all the coordinates where there is a window.
	
	self.tout
		The outside temperature if there is at least one window.
	
	Class attributes:
	
	Data.alpha:
		Fixed constant for thermal diffusivity.
		
	Data.dt:
		Numerical time increment for simulation.
		
	Data.dx:
		Numerical x increment.
		
	Data.dy:
		Numerical y increment.
		
	Data.h
		Fixed constant for heat transfer coefficient.
	
	Data.nb_x
		Number of discrete x values in temperature field.
		
	Data.nb_y
		Number of discrete y values in tempeature field.
	
	
	Methods defined here:
		
	getfield(self, T_field, objects, windows):	
		Returns the initial field based on temperature of field
		and objects created by user.
		
	getrange(self, T_field, objects):
		Finds the range of the temperature values in the field.
		Returns a tuple containing the temperature extremums.
		
	iterate(self):	
		Find the new temperature field after time incrementation.
		
	window(self, windows):
		Creates the list of all border points in the field
		where there is a window.
	"""
	
	nb_x = 200
	nb_y = 200
	dx = 0.01
	dy = 0.01
	dt = 0.05
	alpha = 0.00005
	h = 10
	
	def __init__(self, T_field, T_outside, objects, windows):
		"""Data class builder."""
	
		self.field = self.getfield(T_field, objects)
		self.range = self.getrange(T_field, T_outside, objects)
		self.haswindow = self.window(windows)
		if self.haswindow != []:
			self.tout = T_outside

	def getfield(self, T_field, objects):
		"""Return the initial field based on temperature of field
		and the list of objects created by user.
		"""
	
		o = objects
	
		field = list(range(Data.nb_y))
		for j, elt in enumerate(field):
			field[j] = list(range(Data.nb_x))
			for i, elt in enumerate(field[j]):
				field[j][i] = T_field
			
		for object in o:
			j = object["top"]	
			while j <= object["bottom"]:
				i = object["left"]	
				while i <= object["right"]:
					field[j][i] = object["T"]
					i += 1
				j += 1
	
		return field
		
	def getrange(self, T_field, T_outside, objects):
		"""Finds the range of the temperature values in the field.
		Returns a tuple containing the temperature extremums.
		"""
		
		if T_field < T_outside:
			min = T_field
			max = T_outside
		else:
			min = T_outside
			max = T_field
		
		for object in objects:
			if object["T"] < min:
				min = object["T"]
			elif object["T"] > max:
				max = object["T"]
				
		return (min, max)

	def iterate(self):
		"""Find the new temperature field after time incrementation."""
	
		f = self.field
		nb_x = Data.nb_x
		nb_y = Data.nb_y
		dx = Data.dx
		dy = Data.dy
		dt = Data.dt
		alpha = Data.alpha
		h = Data.h
	
		j = 0
		while j < nb_y:
			i = 0
			while i < nb_x:
				if 0 < i < nb_x - 1 and 0 < j < nb_y - 1:
					f[j][i] = f[j][i] + dt * alpha * ((f[j][i+1] - 2 * f[j][i] + f[j][i-1]) / (dx**2) + (f[j+1][i] - 2 * f[j][i] + f[j-1][i]) / (dy**2))
				elif (i, j) in self.haswindow:
					f[j][i] = f[j][i] + dt * h * (self.tout - f[j][i])
				else:
					f[j][i] = f[j][i]
				i += 1
			j += 1
		
		self.field = f
		
	def window(self, windows):
		"""Creates the list of all border points in the field
		where there is a window."""
		
		haswindow = []
		
		for w in windows:
			if w["side"].lower() == "left":
				j = w["min"]
				while j <= w["max"]:
					haswindow.append((0, j))
					j += 1
			elif w["side"].lower() == "right":
				j = w["min"]
				while j <= w["max"]:
					haswindow.append((Data.nb_x - 1, j))
					j += 1
			elif w["side"].lower() == "top":
				i = w["min"]
				while i <= w["max"]:
					haswindow.append((i, 0))
			elif w["side"].lower() == "bottom":
				i = w["min"]
				while i <= w["max"]:
					haswindow.append((i, Data.nb_x - 1))
					
		return haswindow