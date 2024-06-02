class BitmapLayer:
	def __init__(self, y_size: int, x_size: int, top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Creates a new bitmap layer, with rectangular bounds. This can be used to make bitmap collisions, textures, you
		name it!
		
		Initially, the entire area is off. Its relative top-left coordinate is (0, 0), with +y being down and
		+x being right.
		:param y_size: The height of the layer.
		:param x_size: The width of the layer.
		:param top_left: The top left of this layer with respect to some other coordinate system. Given in
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
		self.flattened_bitmap = [False] * (self.y_size * self.x_size)
		"""
		Internal list of values at points on the bitmap. A point at (y, x) would be found at list position
		``[y * self.x_size + x]``, given ``x < self.x_size``.
		"""
		
	def top_left(self) -> tuple[int, int]:
		"""
		Returns the top-left position of this BitmapLayer.
		:return: The top-left position of this BitmapLayer.
		"""
		return self.top_y, self.left_x
	
	def lock(self) -> None:
		"""
		Locks the layer, preventing it from being changed.
		"""
		self.is_locked = True
		
	def unlock(self) -> None:
		"""
		Unlocks the layer, letting it be changed freely.
		"""
		self.is_locked = False
		
	def relative_yx(self, y_coord: int, x_coord: int) -> tuple[int, int]:
		"""
		Finds the bitmap's relative (y, x) of a point in the main coordinate system.
		:param y_coord: The main coordinate system's point's x value.
		:param x_coord: The main coordinate system's point's y value.
		:return: The bitmap's relative (y, x).
		"""
		relative_y = y_coord - self.top_y
		relative_x = x_coord - self.left_x
		return relative_y, relative_x
	
	def bit_at_point(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds the value at a point on this layer.
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate
		:return: The value of the point.
		"""
		index = self.point_to_index(y_coord, x_coord)
		if index == -1:  # the coordinate wasn't on this CollisionLayer
			return False
		return self.flattened_bitmap[index]
		
	def collides(self, other: "BitmapLayer") -> bool:
		"""
		Finds whether a different layer collides with this layer. That means both have True at the same point.
		:param other: The other layer that may collide with this layer.
		:return: Whether the two layers are colliding (True) or not (False).
		"""
		# define the area of possible collision
		intersect_top_y = max(self.top_y, other.top_y)
		intersect_left_x = max(self.left_x, other.left_x)
		intersect_bottom_y = min(self.top_y + self.y_size, other.top_y + other.y_size)
		intersect_right_x = min(self.left_x + self.x_size, other.left_x + other.x_size)
		
		for y in range(intersect_top_y, intersect_bottom_y):
			for x in range(intersect_left_x, intersect_right_x):
				if self.collides_point(y, x) and other.collides_point(y, x):
					return True
		return False
	
	def collides_point(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds whether this layer collides with a point in the main coordinate system.
		:param y_coord: The y-coordinate of the point.
		:param x_coord: The x-coordinate of the point.
		:return: Whether the layer collides with the point (True) or not (False).
		"""
		relative_point = self.relative_yx(y_coord, x_coord)
		return self.bit_at_point(*relative_point)
		
	def set_all(self, state: bool) -> None:
		"""
		Sets all the state of every point on the bitmap.
		
		Does nothing if this layer is locked.
		:param state: Whether the points should be on (True) or off (False).
		"""
		if not self.is_locked:
			self.flattened_bitmap = [state] * (self.y_size * self.x_size)
	
	def invert(self) -> None:
		"""
		Inverts the bitmap, so on becomes off and vice versa.
		
		Does nothing if this layer is locked.
		"""
		if not self.is_locked:
			self.flattened_bitmap = [not coord for coord in self.flattened_bitmap]
			
	def set_point(self, state: bool, y_coord: int, x_coord: int) -> None:
		"""
		Sets the state of a single point on this layer. If the point is out of bounds, this does nothing.
		
		If this layer is locked, this does nothing.
		:param state: Whether the point should be on (True) or off (False).
		:param y_coord: The y-coordinate.
		:param x_coord: The x-coordinate.
		"""
		if self.is_locked:
			return
		index = self.point_to_index(y_coord, x_coord)
		if index == -1:
			return
		self.flattened_bitmap[index] = state
		
	def add_rect(self, state: bool, y_size: int, x_size: int, top_left: tuple[int, int] = (0, 0)) -> None:
		"""
		Turns a rectangular area on or off. If a part goes outside of the layer bounds, it will be ignored.
		
		If this layer is locked, this does nothing.
		:param state: Whether the rectangular area should be on (True) or off (False).
		:param y_size: The height of the rectangular area.
		:param x_size: The width of the rectangular area.
		:param top_left: The top-left coordinate of the rectangle in (y, x) form. Defaults to (0, 0).
		"""
		if self.is_locked:
			return
		
		top_y = top_left[0]
		left_x = top_left[1]
		bottom_y = top_y + y_size
		right_x = left_x + x_size
		
		if top_y > bottom_y or left_x > right_x:  # if the "top left" is not really the top left
			return
		
		for y_coord in range(top_y, bottom_y):
			for x_coord in range(left_x, right_x):
				self.set_point(state, y_coord, x_coord)
	
	def set_top_left(self, new_top_left: tuple[int, int]) -> None:
		"""
		Sets the top left of this layer to a new point in the main coordinate system.

		Does nothing if the layer is locked.
		:param new_top_left: The new top-left point, in (y, x) form.
		"""
		if not self.is_locked:
			self.top_y, self.left_x = new_top_left
	
	def point_to_index(self, y_coord: int, x_coord: int) -> int:
		"""
		Returns the flattened bitmap's index of a point on this bitmap.
		
		:param y_coord: The y-coordinate of the point.
		:param x_coord: The x-coordinate of the point.
		:return: The flattened bitmap's index of the point. -1 if the point is out of bounds.
		"""
		if self.point_in_bounds(y_coord, x_coord):
			return y_coord * self.x_size + x_coord
		return -1
	
	def index_to_point(self, index: int) -> tuple[int, int]:
		"""
		Given an index in the flattened bitmap, returns the point it corresponds to.
		:param index: The index in the flattened bitmap.
		:return: The point, in (y, x) form. (-1, -1) if the index is out of bounds.
		"""
		if index < 0 or index >= len(self.flattened_bitmap):
			return -1, -1
		y_coord = index // self.x_size
		x_coord = index % self.x_size
		return y_coord, x_coord
	
	def point_in_bounds(self, y_coord: int, x_coord: int) -> bool:
		"""
		Finds whether the given point (relative to the top-left of this layer) is in bounds.
		:param y_coord: The point's y-coordinate.
		:param x_coord: The point's x-coordinate.
		:return: Whether the point is in bounds (True) or not (False).
		"""
		return not (y_coord < 0 or y_coord >= self.y_size or x_coord < 0 or x_coord >= self.x_size)
