from tkinter import PhotoImage

from data import Data

class Heatmap:
	"""Class designed to produce the heatmap based on T-values in the field.
	
	Main attribute:
	
	self.heatmap
		2-dimensional heat map where colors tepend on temperature.
		A mathematical formula determines intensity of red, green and blue.
		Blue is very cold, red is very hot and green somewhere in between.
		
	
	Other attributes:
	
	self.blue
		Temperature for which a pixel in the heatmap will be blue.
		Corresponds to the lowest initial temperature in the field.
		
	self.green
		Temperature for which a pixel in the heatmap will be green.
		Corresponds to the midrange initial temperature in the field.
		
	self.red
		Temperature for which a pixel in the heatmap will be red.
		Corresponds to the highest initial temperature in the field.
		
	self.scale
		Variation rate of the color in (r, g, b) format with respect
		to the temperature.
		
	self.haswindow
		List containing all the coordinates where there is a window.
		
	
	Methods defined here:
	
	__init__(self):
		Heatmap class builder.
		
	color(self, T):
		Get the appropriate color for a pixel in the heatmap
		based on the corresponding T-value in the temperature field.
		Mathematical formula used to get r, g and b intensities.
		
	get(self, field):
		Create temperature color map based on the temperatures in field.
		A colored pixel is generated for each value in temperature field.
		Returns the heatmap containing all these pixels.
	"""
	
	def __init__(self, range, haswindow):
		"""Heatmap class builder."""
		
		self.heatmap = PhotoImage(width=Data.nb_x, height=Data.nb_y)		
		self.blue = range[0]
		self.red = range[1]
		self.green = (self.blue + self.red)/2
		self.scale = 2 * 255/(self.red - self.blue)
		self.haswindow = haswindow

	def color(self, T):
		"""Get the appropriate color for a pixel in the heatmap
		based on the corresponding T-value in the temperature field.
		Mathematical formula used to get r, g and b intensities.
		"""
		
		if T == self.blue:
			r = 0
			g = 0
			b = 255
		
		elif T < self.green:
			r = 0
			g = round((T-self.blue) * self.scale)
			b = 255 - round((T-self.blue) * self.scale)
			
		elif T < self.red:
			r = round((T-self.green) * self.scale)
			g = 255 - round((T-self.green) * self.scale)
			b = 0
			
		elif T == self.red:
			r = 255
			g = 0
			b = 0
			
		return (r, g, b)
	
	def get(self, field):
		"""Initialize temperature color map when simulation is started.
		A colored pixel is generated for each value in temperature field.
		Returns the heatmap containing all these pixels.
		"""
	
		f = field
		nb_x = Data.nb_x
		nb_y = Data.nb_y
	
		j = 0
		hexcode = ""
		while j < nb_y:
			i = 0
			hexcode += "{"
			while i < nb_x:
				(r, g, b) = self.color(f[j][i])
				hexcode += "#%02x%02x%02x" % (r, g, b)
				i += 1
				if i != nb_x:
					hexcode += " "
			j += 1
			hexcode += "} "
		
		self.heatmap.put(hexcode)
		return self.heatmap