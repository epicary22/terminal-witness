class CollisionsLayer:
	def __init__(self, y_size: int, x_size: int) -> None:
		"""
		Creates a new collision layer, with rectangular bounds. This can be used for sensing whether a coordinate is
		inside of or outside of a given area.
		
		Initially, the entire area is non-colliding. The top-left coordinate is (0, 0), with +y being down and +x being
		right.
		:param y_size: The height of the collision layer.
		:param x_size: The width of the collision layer.
		"""
		self.y_size = y_size
		self.x_size = x_size
		self.collisions = [False] * (self.y_size * self.x_size)
		"""
		Internal list of coordinates' collision or non-collision. A coordinate at (y, x) would be found at list position
		``[y * self.y_size + x * self.x_size]``.
		"""
		
	def set_all(self, colliding: bool) -> None:
		"""
		Sets all of the coordinates to either be colliding or not, depending on the given boolean.
		:param colliding: Whether the coordinates should be colliding or not. True for colliding,
			False for not colliding.
		"""
		self.collisions = [colliding] * (self.y_size * self.x_size)
	
	def invert_all(self) -> None:
		"""
		Inverts all of the coordinates' collisions, so colliding becomes non-colliding and vice versa.
		"""
		self.collisions = [not coord for coord in self.collisions]
		
	def coordinate_to_index(self, y_coord: int, x_coord: int) -> int:
		"""
		Given a set of coordinates, returns the index of that point in the ``self.collisions`` list.
		:param y_coord: The y-coordinate of the point.
		:param x_coord: The x-coordinate of the point.
		:return: The index of the point in the ``self.collisions`` list.
		"""
		return y_coord * self.y_size + x_coord * self.x_size
		
	def set_point(self, colliding: bool, y_coord: int, x_coord: int) -> None:
		"""
		Sets the collision of a single point. If the point is out of bounds, this does nothing.
		:param colliding: Whether the point should be colliding (True) or not (False).
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate.
		"""
		index = self.coordinate_to_index(y_coord, x_coord)
		if index < 0 or index >= len(self.collisions):
			return
		self.collisions[index] = colliding
		
	def add_rect(self, colliding: bool, y_size: int, x_size: int, top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Adds a rectangular area of collision or non-collision. If a part goes outside of the layer bounds, it will be
		ignored.
		:param colliding: Whether the rectangular area should be colliding (True) or non-colliding (False).
		:param y_size: The height of the rectangular area.
		:param x_size: The width of the rectangular area.
		:param top_left: The top-left coordinate of the rectangle, relative to the top left of this CollisionsLayer.
			Is in (y, x) form. Defaults to (0, 0) (the top left coordinate of this CollisionsLayer)
		"""
		top_y = top_left[0]
		left_x = top_left[1]
		bottom_y = top_y + y_size - 1
		right_x = left_x + x_size - 1
		
		if top_y > bottom_y or left_x > right_x:  # if the "top left" is not really the top left
			return
		
		for y_coord in range(top_y, bottom_y):
			for x_coord in range(left_x, right_x):
				self.set_point(colliding, y_coord, x_coord)
		