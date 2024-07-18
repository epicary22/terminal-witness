from grid.layer import Layer


class BitmapLayer(Layer):
	def __init__(self, height: int, width: int, top_left: tuple[int, int]) -> None:
		super().__init__(bool, height, width, top_left)
		self.set_all(False)
	
	def intersect(self, other: "BitmapLayer", use_future_positions: bool) -> "BitmapLayer":
		if use_future_positions:
			self_tl = self.position.next_position()
			other_tl = other.position.next_position()
		else:
			self_tl = self.position.position()
			other_tl = other.position.position()
		
		self_br = (self_tl[0] + self.height - 1, self_tl[1] + self.width - 1)
		other_br = (other_tl[0] + other.height - 1, other_tl[1] + other.width - 1)
		intersect_tl = (max(self_tl[0], other_tl[0]), max(self_tl[1], other_tl[1]))
		intersect_br = (min(self_br[0], other_br[0]), min(self_br[1], other_br[1]))
		intersect_height = intersect_br[0] - intersect_tl[0] + 1
		intersect_width = intersect_br[1] - intersect_tl[1] + 1
		intersection = BitmapLayer(intersect_height, intersect_width, intersect_tl)
		
		for y in range(intersect_tl[0], intersect_br[0] + 1):
			for x in range(intersect_tl[1], intersect_br[1] + 1):
				if self.r_value_at((y, x), use_future_positions) and other.r_value_at((y, x), use_future_positions):
					intersection.r_set_point((y, x), True, use_future_positions)
		
		return intersection
	
	# @Layer._use_future_positions
	# def future_intersect(self, other: "BitmapLayer") -> "BitmapLayer":
	# 	self_old_position = self._top_left
	# 	other_old_position = other._top_left
	# 	self._top_left = self.position.next_position()
	# 	other._top_left = other.position.next_position()
	# 	intersection = self.intersect(other)
	# 	self._top_left = self_old_position
	# 	other._top_left = other_old_position
	# 	return intersection
	
	def collides(self, other: "BitmapLayer", use_future_positions: bool) -> bool:
		intersect_grid = self.intersect(other, use_future_positions).grid
		for row in intersect_grid:
			for value in row:
				if value:
					return True
		return False
	
	# @Layer._use_future_positions
	# def future_collides(self, other: "BitmapLayer") -> bool:
	# 	self_old_position = self._top_left
	# 	other_old_position = other._top_left
	# 	self._top_left = self.position.next_position()
	# 	other._top_left = other.position.next_position()
	# 	collides = self.collides(other)
	# 	self._top_left = self_old_position
	# 	other._top_left = other_old_position
	# 	return collides
	