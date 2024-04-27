import curses


class Cursor:
	def __init__(self, starting_pos: tuple[int, int] = (0, 0)) -> None:
		"""
		A cursor meant to be used with the curses library. -y is up, and +x is right.
		The cursor uses transformations, meaning the update() method must be called to actually update the position.
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
		Adds a given distance up to the cursor's next transformation.
		:param distance: The amount to add to the transformation.
		"""
		self.transform_y -= distance
		
	def down(self, distance: int = 1) -> None:
		"""
		Adds a given distance down to the cursor's next transformation.
		:param distance: The amount to add to the transformation.
		"""
		self.transform_y += distance
		
	def right(self, distance: int = 1) -> None:
		"""
		Adds a given distance right to the cursor's next transformation.
		:param distance: The amount to add to the transformation.
		"""
		self.transform_x += distance
		
	def left(self, distance: int = 1) -> None:
		"""
		Adds a given distance left to the cursor's next transformation.
		:param distance: The amount to add to the transformation.
		"""
		self.transform_x -= distance
		
	def add_transform(self, transform: tuple[int, int]) -> None:
		"""
		Adds a transform to the cursor's next transform.
		:param transform: A transform to add. In the form (y, x), where -y is up, and +x is right.
		"""
		self.transform_y += transform[0]
		self.transform_x += transform[1]
		
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
		Returns the current position of the cursor, in (y, x) form.
		:return: The current position of the cursor.
		"""
		return self.y, self.x
	
	def transform(self) -> tuple[int, int]:
		"""
		Returns the current transform to be applied to the cursor, in (y, x) form.
		:return: The current transform to be applied to the cursor.
		"""
		return self.transform_y, self.transform_x
	
	def next_position(self) -> tuple[int, int]:
		"""
		Returns the position the cursor will have after applying its transform, in (y, x) form.
		:return: The position of the cursor after applying its transform.
		"""
		return self.y + self.transform_y, self.x + self.transform_x
	
	def update(self) -> None:
		"""
		Applies the current transform to the position of the cursor, updating its position.
		Resets the transformation to (0, 0).
		"""
		self.y, self.x = self.next_position()
		self.transform_y, self.transform_x = (0, 0)
		