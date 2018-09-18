class UniformFieldError(Exception):
	"""Exception raised when user tries to start simulation
	without defining any object or window.
	"""
	
	def __init__(self, message):
		"""UniformFieldError exception builder."""
		
		self.message = message

class HeatmapError(Exception):
	"""Exception raised when the area of an object or a
	window is not entirely contained in the heatmap.
	"""
	
	def __init__(self, message):
		"""HeatmapError exception builder."""
		
		self.message = message

class OverlapError(Exception):
	"""Exception raised when two objects or two windows
	are overlapping.
	"""
	
	def __init__(self, message):
		"""OverlapError exception builder."""
		
		self.message = message