class CollisionsLayer:
	def __init__(self, y_size: int, x_size: int, top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Creates a new collision layer, with rectangular bounds. This can be used for sensing whether a coordinate is
		inside or outside of a given area.
		
		Initially, the entire area is non-colliding. Its relative top-left coordinate is (0, 0), with +y being down and
		+x being right.
		:param y_size: The height of the collision layer.
		:param x_size: The width of the collision layer.
		:param top_left: The top left of this collisions layer with respect to some other coordinate system. Given in
			(y, x) form. Defaults to (0, 0).
		"""
		self.y_size = y_size
		self.x_size = x_size
		self.top_y, self.left_x = top_left
		self.is_locked = False
		"""
		Whether the layer should be able to be changed or not. Can be set to True with the ``self.lock()`` method, and
		set to False with the ``self.unlock()`` method.
		"""
		self.collisions = [False] * (self.y_size * self.x_size)
		"""
		Internal list of coordinates' collision or non-collision. A coordinate at (y, x) would be found at list position
		``[y * self.x_size + x]``, given ``x < self.x_size``.
		"""
		
	def lock(self) -> None:
		"""
		Locks the CollisionLayer, preventing it from being changed.
		"""
		self.is_locked = True
		
	def unlock(self) -> None:
		"""
		Unlocks the CollisionLayer, letting it be changed freely.
		"""
		self.is_locked = False
		
	def value_at(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds the value of a point, with coordinates relative to the top-left of this layer.
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate
		:return: The value of the point.
		"""
		index = self.relative_point_to_index(y_coord, x_coord)
		if index == -1:  # the coordinate wasn't on this CollisionLayer
			return False
		return self.collisions[index]
		
	def collides(self, other: "CollisionsLayer") -> bool:
		"""
		Finds whether a different CollisionsLayer collides with this CollisionsLayer.
		:param other: The other CollisionsLayer that may collide with this CollisionsLayer.
		:return: Whether the two CollisionsLayers are colliding (True) or not (False).
		"""
		# TODO finish this method
		for y in range(self.top_y, self.y_size):
			for x in range(self.left_x, self.x_size):
				if other.collides_point((y, x)):
					return True
		return False
	
	def collides_point(self, other_point: tuple[int, int]) -> bool:
		"""
		Finds whether this CollisionsLayer collides with a point, both of which share a coordinate system.
		:param other_point: The point to find whether this CollisionsLayer collides with. In (y, x) form.
		:return: Whether the CollisionsLayer collides with the point (True) or not (False).
		"""
		relative_y = other_point[0] - self.top_y
		relative_x = other_point[1] - self.left_x
		return self.value_at(relative_y, relative_x)
		
	def set_all(self, colliding: bool) -> None:
		"""
		Sets all the points to either be colliding or not, depending on the given boolean.
		
		Does nothing if this layer is locked.
		:param colliding: Whether the points should be colliding (True) or not (False).
		"""
		if not self.is_locked:
			self.collisions = [colliding] * (self.y_size * self.x_size)
	
	def invert_all(self) -> None:
		"""
		Inverts all of the coordinates' collisions, so colliding becomes non-colliding and vice versa.
		
		Does nothing if this layer is locked.
		"""
		if not self.is_locked:
			self.collisions = [not coord for coord in self.collisions]
			
	def set_point(self, colliding: bool, y_coord: int, x_coord: int) -> None:
		"""
		Sets the collision of a single point, relative to the top-left of this layer. If the point is out of bounds,
		this does nothing.
		
		If this layer is locked, this does nothing.
		:param colliding: Whether the point should be colliding (True) or not (False).
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate.
		"""
		if self.is_locked:
			return
		index = self.relative_point_to_index(y_coord, x_coord)
		if index < 0 or index >= len(self.collisions):
			return
		self.collisions[index] = colliding
		
	def add_rect(self, colliding: bool, y_size: int, x_size: int, relative_top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Adds a rectangular area of collision or non-collision. If a part goes outside of the layer bounds, it will be
		ignored.
		
		If this layer is locked, this does nothing.
		:param colliding: Whether the rectangular area should be colliding (True) or non-colliding (False).
		:param y_size: The height of the rectangular area.
		:param x_size: The width of the rectangular area.
		:param relative_top_left: The top-left coordinate of the rectangle, relative to the top left of this
			CollisionsLayer. Is in (y, x) form. Defaults to (0, 0) (the top left coordinate of this CollisionsLayer)
		"""
		if self.is_locked:
			return
		
		top_y = relative_top_left[0]
		left_x = relative_top_left[1]
		bottom_y = top_y + y_size
		right_x = left_x + x_size
		
		if top_y > bottom_y or left_x > right_x:  # if the "top left" is not really the top left
			return
		
		for y_coord in range(top_y, bottom_y):
			for x_coord in range(left_x, right_x):
				self.set_point(colliding, y_coord, x_coord)
	
	def reset_top_left(self, new_top_left: tuple[int, int]) -> None:
		"""
		Sets the top left of this CollisionsLayer to a new point with respect to a main coordinate system.

		Does nothing if the layer is locked.
		:param new_top_left: The new top-left point.
		"""
		if not self.is_locked:
			self.top_y, self.left_x = new_top_left
	
	def relative_point_to_index(self, y_coord: int, x_coord: int) -> int:
		"""
		Given a point relative to the top-left of this CollisionsLayer, returns the index of that point in
		the ``self.collisions`` list.
		:param y_coord: The y-coordinate of the point.
		:param x_coord: The x-coordinate of the point.
		:return: The index of the point in the ``self.collisions`` list. -1 if the point is out of bounds.
		"""
		if self.relative_point_in_bounds(y_coord, x_coord):
			return y_coord * self.x_size + x_coord
		return -1
	
	def index_to_relative_point(self, index: int) -> tuple[int, int]:
		"""
		Given an index in the ``self.collisions`` list, gives the corresponding point on this CollisionLayer.
		:param index: The index in the ``self.collisions`` list.
		:return: The point relative to the top-left of this CollisionsLayer. (-1, -1) if the index is out of bounds.
		"""
		if index < 0 or index >= len(self.collisions):
			return -1, -1
		y_coord = index // self.x_size
		x_coord = index % self.x_size
		return y_coord, x_coord
	
	def relative_point_in_bounds(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds whether the given point relative to the top-left of this CollisionsLayer is in its bounds.
		:param y_coord: The point's y-coordinate.
		:param x_coord: The point's x-coordinate.
		:return: Whether the point is in bounds (True) or not (False).
		"""
		return not (y_coord < 0 or y_coord >= self.y_size or x_coord < 0 or x_coord >= self.x_size)
