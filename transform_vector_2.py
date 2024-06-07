class TransformVector2:
	def __init__(self, starting_pos: tuple[int, int] = (0, 0)) -> None:
		"""
		A 2D vector that only moves when explicitly updated. -y is up, and +x is right.
		:param starting_pos: The initial position of the cursor.
		"""
		self.x, self.y = starting_pos
		self.transform_x, self.transform_y = (0, 0)
		
	def zero_axes(self, y: bool = True, x: bool = True) -> None:
		"""
		Zeroes the x axis, y axis, or both. Overwrites previous transformations not yet applied.
		:param y: If True, the y coordinate will be zeroed. True by default.
		:param x: If True, the x coordinate will be zeroed. True by default.
		"""
		if y:
			self.transform_y = -self.y
		if x:
			self.transform_x = -self.x
		
	def up(self, distance: int = 1) -> None:
		"""
		Adds a given up distance to the next transform.
		:param distance: The distance to add.
		"""
		self.transform_y -= distance
		
	def down(self, distance: int = 1) -> None:
		"""
		Adds a given down distance to the next transform.
		:param distance: The distance to add.
		"""
		self.transform_y += distance
		
	def right(self, distance: int = 1) -> None:
		"""
		Adds a given right distance to the next transform.
		:param distance: The distance to add.
		"""
		self.transform_x += distance
		
	def left(self, distance: int = 1) -> None:
		"""
		Adds a given left distance to the next transform.
		:param distance: The distance to add.
		"""
		self.transform_x -= distance
		
	def add_transform(self, transform: tuple[int, int]) -> None:
		"""
		Adds a transform to the cursor's next transform.
		:param transform: A transform to add, in (y, x) form.
		"""
		self.transform_y += transform[0]
		self.transform_x += transform[1]
		
	def goto(self, position: tuple[int, int]) -> None:
		"""
		Sets the vector's next position to the given position.
		:param position: The position for the vector to go to, in (y, x) form.
		"""
		self.zero_axes()
		self.transform_y += position[0]
		self.transform_x += position[1]
		
	def cancel_transform(self, y: bool = True, x: bool = True) -> None:
		"""
		Cancels the x, y, or both axes of the current transform.
		:param y: If True, will cancel the y transform. True by default.
		:param x: If True, will cancel the x transform. True by default.
		"""
		if y:
			self.transform_y = 0
		if x:
			self.transform_x = 0
		
	def position(self) -> tuple[int, int]:
		"""
		Returns the current vector, in (y, x) form.
		:return: The current vector.
		"""
		return self.y, self.x
	
	def transform(self) -> tuple[int, int]:
		"""
		Returns the current transform to be applied to the vector, in (y, x) form.
		:return: The current transform to be applied to the vector.
		"""
		return self.transform_y, self.transform_x
	
	def next_position(self) -> tuple[int, int]:
		"""
		Returns the position the vector will have after applying its transform, in (y, x) form.
		:return: The position of the vector after applying its transform.
		"""
		return self.y + self.transform_y, self.x + self.transform_x
	
	def update(self) -> None:
		"""
		Applies the current transform to the position of the vector.
		Resets the transformation to (0, 0).
		"""
		self.y, self.x = self.next_position()
		self.transform_y, self.transform_x = (0, 0)
		
	def apply_transform(self) -> None:
		"""
		Applies the current transform to the position of the vector.
		Does not reset the current transform.
		"""
		self.y, self.x = self.next_position()
		