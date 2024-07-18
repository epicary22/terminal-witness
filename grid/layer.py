from grid.grid import Grid
from transform_vector_2 import TransformVector2
import typing


class Layer(Grid):
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
		
	def r_point(self, point: tuple[int, int], use_future_positions: bool) -> tuple[int, int]:
		if use_future_positions:
			top_left = self.position.next_position()
		else:
			top_left = self.position.position()
		return point[0] - top_left[0], point[1] - top_left[1]
	
	def r_value_at(self, point: tuple[int, int], use_future_positions: bool) -> typing.Any:
		return self.value_at(self.r_point(point, use_future_positions))
	
	def r_set_point(self, point: tuple[int, int], value: typing.Any, use_future_positions: bool) -> None:
		self.set_point(self.r_point(point, use_future_positions), value)
		