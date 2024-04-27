class CollisionsLayer:
	def __init__(self, y_size: int, x_size: int, top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Creates a new collision layer, with rectangular bounds. This can be used for sensing whether a coordinate is
		inside of or outside of a given area.
		
		Initially, the entire area is non-colliding. The top-left coordinate is (0, 0), with +y being down and +x being
		right.
		:param y_size: The height of the collision layer.
		:param x_size: The width of the collision layer.
		:param top_left: The top left of this collisions layer with respect to some other coordinate system. Given in
			(y, x) form. Defaults to (0, 0).
		"""
		self.y_size = y_size
		self.x_size = x_size
		self.top_y, self.left_x = top_left
		self.collisions = [False] * (self.y_size * self.x_size)
		"""
		Internal list of coordinates' collision or non-collision. A coordinate at (y, x) would be found at list position
		``[y * self.x_size + x]``, given ``x < self.x_size``.
		"""
		
	def reset_top_left(self, new_top_left: tuple[int, int]) -> None:
		"""
		Sets the top left of this CollisionsLayer to a new coordinate with respect to a main coordinate system.
		:param new_top_left: The new top-left coordinate.
		"""
		self.top_y, self.left_x = new_top_left
		
	def collides(self, other: "CollisionsLayer") -> bool:
		"""
		STUB
		
		Finds whether a different CollisionsLayer collides with this CollisionsLayer.
		:param other: The other CollisionsLayer that may collide with this CollisionsLayer.
		:return: Whether the two CollisionsLayers are colliding (True) or not (False).
		"""
		# TODO finish this method
		return False
	
	def collides_point(self, other_point: tuple[int, int]) -> bool:
		"""
		Finds whether this CollisionsLayer collides with a point, both of which share a coordinate system.
		:param other_point: The point to find whether this CollisionsLayer collides with. In (y, x) form.
		:return: Whether the CollisionsLayer collides with the point (True) or not (False).
		"""
		relative_y = other_point[0] - self.top_y
		relative_x = other_point[1] - self.left_x
		index = self.relative_coordinate_to_index(relative_y, relative_x)
		if index == -1:  # the coordinate wasn't on this CollisionLayer
			return False
		return self.collisions[index]
		
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
		
	def relative_coordinate_to_index(self, y_coord: int, x_coord: int) -> int:
		"""
		Given a set of coordinates relative to the top-left of this CollisionsLayer, returns the index of that point in
		the ``self.collisions`` list.
		:param y_coord: The y-coordinate of the point.
		:param x_coord: The x-coordinate of the point.
		:return: The index of the point in the ``self.collisions`` list. -1 if the point is out of bounds.
		"""
		if self.relative_coordinate_in_bounds(y_coord, x_coord):
			return y_coord * self.x_size + x_coord
		return -1
		
	def index_to_relative_coordinate(self, index: int) -> tuple[int, int]:
		"""
		Given an index in the ``self.collisions`` list, gives the coordinate relative to the top-left of this
		CollisionsLayer that it corresponds to.
		:param index: The index in the ``self.collisions`` list.
		:return: The index's coordinates relative to the top-left of this CollisionsLayer.
			(-1, -1) if the index is out of bounds.
		"""
		if index < 0 or index >= len(self.collisions):
			return -1, -1
		y_coord = index // self.x_size
		x_coord = index % self.x_size
		return y_coord, x_coord
	
	def relative_coordinate_in_bounds(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds whether the given point relative to the top-left of this CollisionsLayer is in its bounds.
		:param y_coord: The point's y-coordinate.
		:param x_coord: The point's x-coordinate.
		:return: Whether the point is in bounds (True) or not (False).
		"""
		return not (y_coord < 0 or y_coord >= self.y_size or x_coord < 0 or x_coord >= self.x_size)
	
	def set_point(self, colliding: bool, y_coord: int, x_coord: int) -> None:
		"""
		Sets the collision of a single point. If the point is out of bounds, this does nothing.
		:param colliding: Whether the point should be colliding (True) or not (False).
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate.
		"""
		index = self.relative_coordinate_to_index(y_coord, x_coord)
		if index < 0 or index >= len(self.collisions):
			return
		self.collisions[index] = colliding
		
	def add_rect(self, colliding: bool, y_size: int, x_size: int, relative_top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Adds a rectangular area of collision or non-collision. If a part goes outside of the layer bounds, it will be
		ignored.
		:param colliding: Whether the rectangular area should be colliding (True) or non-colliding (False).
		:param y_size: The height of the rectangular area.
		:param x_size: The width of the rectangular area.
		:param relative_top_left: The top-left coordinate of the rectangle, relative to the top left of this
			CollisionsLayer. Is in (y, x) form. Defaults to (0, 0) (the top left coordinate of this CollisionsLayer)
		"""
		top_y = relative_top_left[0]
		left_x = relative_top_left[1]
		bottom_y = top_y + y_size
		right_x = left_x + x_size
		
		if top_y > bottom_y or left_x > right_x:  # if the "top left" is not really the top left
			return
		
		for y_coord in range(top_y, bottom_y):
			for x_coord in range(left_x, right_x):
				self.set_point(colliding, y_coord, x_coord)
		