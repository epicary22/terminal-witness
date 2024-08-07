import typing


class Grid:
	def __init__(self, t: type, height: int, width: int) -> None:
		self.t = t
		self.height = height
		self.width = width
		self.grid = [[None] * width for _ in range(height)]
		self.locked = False
	
	def value_at(self, point: tuple[int, int]) -> typing.Any:
		self._point_in_bounds(point)
		return self.grid[point[0]][point[1]]
	
	def lock(self) -> None:
		self.locked = True
		
	def unlock(self) -> None:
		self.locked = False
	
	@staticmethod
	def _lockable(func: ()) -> ():
		def wrapper(self: "Grid", *args, **kwargs):
			if not self.locked:
				func(self, *args, **kwargs)
		return wrapper
	
	@_lockable
	def set_point(self, point: tuple[int, int], value: typing.Any) -> None:
		self._check_value_type(value)
		try:
			self._point_in_bounds(point)
		except ValueError:
			return
		y, x = point
		self.grid[y][x] = value
		
	@_lockable
	def add_rect(self, height: int, width: int, top_left: tuple[int, int], value: typing.Any) -> None:
		self._check_value_type(value)
		start_y, start_x = top_left
		end_y = min(start_y + height - 1, self.height - 1)
		end_x = min(start_x + width - 1, self.width - 1)
		for y in range(start_y, end_y + 1):
			for x in range(start_x, end_x + 1):
				self.set_point((y, x), value)
		
	@_lockable
	def set_all(self, value: typing.Any) -> None:
		self._check_value_type(value)
		self.grid = [[value for column in row] for row in self.grid]
		
	def _check_value_type(self, value: typing.Any) -> None:
		if type(value) is not self.t:
			raise TypeError(
				f"Value '{value}' (type '{type(value).__name__}') must be of type '{self.t.__name__}' for "
				f"{self} ({self.height}x{self.width})"
			)
		
	def _point_in_bounds(self, point: tuple[int, int]) -> None:
		y, x = point
		if 0 <= y < self.height and 0 <= x < self.width:
			return
		else:
			raise ValueError(f"Point {point} is not in bounds for {self} ({self.height}x{self.width})")
			