from grid.layer import Layer


class BitmapLayer(Layer):
	def __init__(self, height: int, width: int, top_left: tuple[int, int]) -> None:
		super().__init__(bool, height, width, top_left)
		self.set_all(False)
	
	def intersect(self, other: "BitmapLayer", movement_percent: float = 0.0) -> "BitmapLayer":
		if movement_percent >= Layer.MIN_MOVEMENT_PERCENT:
			self_tl = self.position.lerp(movement_percent)
			other_tl = other.position.lerp(movement_percent)
		else:
			self_tl = self.position.position()
			other_tl = other.position.position()
		
		self_br = (self_tl[0] + self.height - 1, self_tl[1] + self.width - 1)
		other_br = (other_tl[0] + other.height - 1, other_tl[1] + other.width - 1)
		intersect_tl = (max(self_tl[0], other_tl[0]), max(self_tl[1], other_tl[1]))
		intersect_br = (min(self_br[0], other_br[0]), min(self_br[1], other_br[1]))
		intersect_height = intersect_br[0] - intersect_tl[0] + 1
		intersect_width = intersect_br[1] - intersect_tl[1] + 1
		if intersect_width > 0 and intersect_width > 0:
			intersection = BitmapLayer(intersect_height, intersect_width, intersect_tl)
		else:
			return BitmapLayer(0, 0, (0, 0))
		
		for y in range(intersect_tl[0], intersect_br[0] + 1):
			for x in range(intersect_tl[1], intersect_br[1] + 1):
				if self.r_value_at((y, x), movement_percent) and other.r_value_at((y, x), movement_percent):
					intersection.r_set_point((y, x), True, movement_percent)
		
		return intersection
	
	def collides(self, other: "BitmapLayer", movement_percent: float) -> bool:
		intersect_grid = self.intersect(other, movement_percent).grid
		for row in intersect_grid:
			for value in row:
				if value:
					return True
		return False
	