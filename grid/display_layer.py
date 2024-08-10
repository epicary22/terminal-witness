from grid.layer import Layer


class DisplayLayer(Layer):
	def __init__(self, height: int, width: int, top_left: tuple[int, int]) -> None:
		"""
		Type of each pixel: tuple[str, int]
		"""
		super().__init__(tuple[str, int], height, width, top_left)
		self.set_all(("", 0))
		
	def set_attribute_all(self, attribute: int) -> None:
		for row in self.grid:
			for pixel in row:
				if pixel:
					pixel[1] |= attribute
	
	def flip_attribute_all(self, attribute: int) -> None:
		for row in self.grid:
			for pixel in row:
				if pixel:
					pixel[1] ^= attribute
					