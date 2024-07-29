from grid.grid import Grid
from transform_vector_2 import TransformVector2
import typing


class Layer(Grid):
	MIN_MOVEMENT_PERCENT = 0.001
	MAX_MOVEMENT_PERCENT = 1.000
	
	def __init__(self, t: type, height: int, width: int, top_left: tuple[int, int]) -> None:
		super().__init__(t, height, width)
		self.position = TransformVector2(top_left)
		self._top_left = self.position.position()
	
	# @staticmethod
	# def _use_future_positions(func: ()) -> ():
	# 	def wrapper(self: "Layer", other: "Layer", *args, **kwargs):
	# 		self_old_position = self._top_left
	# 		other_old_position = other._top_left
	# 		self._top_left = self.position.next_position()
	# 		other._top_left = other.position.next_position()
	# 		return_value = func(self, other, *args, **kwargs)
	# 		self._top_left = self_old_position
	# 		other._top_left = other_old_position
	# 		return return_value
	# 	return wrapper
		
	def r_point(self, point: tuple[int, int], movement_percent: float = 0.0) -> tuple[int, int]:
		if movement_percent >= Layer.MIN_MOVEMENT_PERCENT:
			top_left = self.position.lerp(movement_percent)
		else:
			top_left = self.position.position()
		return point[0] - top_left[0], point[1] - top_left[1]
	
	def r_value_at(self, point: tuple[int, int], movement_percent: float = 0.0) -> typing.Any:
		return self.value_at(self.r_point(point, movement_percent))
	
	def r_set_point(self, point: tuple[int, int], value: typing.Any, movement_percent: float = 0.0) -> None:
		self.set_point(self.r_point(point, movement_percent), value)
		
	def r_add_rect(self, height: int, width: int, top_left: tuple[int, int], value: typing.Any, movement_percent: float = 0.0) -> None:
		self.add_rect(height, width, self.r_point(top_left, movement_percent), value)
	