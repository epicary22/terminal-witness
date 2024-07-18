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
		
	def r_point(self, point: tuple[int, int]) -> tuple[int, int]:
		return point[0] - self._top_left[0], point[1] - self._top_left[1]
	
	def r_value_at(self, point: tuple[int, int]) -> typing.Any:
		return self.value_at(self.r_point(point))
	
	def r_set_point(self, point: tuple[int, int], value: typing.Any) -> None:
		self.set_point(self.r_point(point), value)
		