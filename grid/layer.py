from grid.grid import Grid
from transform_vector_2 import TransformVector2
import typing
import types


class Layer(Grid):
	_next_uid = 0
	
	def __init__(self, t: type | types.GenericAlias | types.UnionType, height: int, width: int, top_left: tuple[int, int]) -> None:
		super().__init__(t, height, width)
		self.position = TransformVector2(top_left)
		self._top_left = self.position.position()
		self.uid = self._generate_uid()
		
	def r_point(self, point: tuple[int, int]) -> tuple[int, int]:
		top_left = self.position.position()
		return point[0] - top_left[0], point[1] - top_left[1]
	
	def r_value_at(self, point: tuple[int, int]) -> typing.Any:
		return self.value_at(self.r_point(point))
	
	def r_set_point(self, point: tuple[int, int], value: typing.Any) -> None:
		self.set_point(self.r_point(point), value)
		
	def r_add_rect(self, height: int, width: int, top_left: tuple[int, int], value: typing.Any) -> None:
		self.add_rect(height, width, self.r_point(top_left), value)
	
	def r_add_grid(self, other: "Layer") -> None:
		self.add_grid(other, self.r_point(other.position.position()))
		
	@staticmethod
	def _generate_uid():
		uid = Layer._next_uid
		Layer._next_uid += 1
		return uid
	
	def get_uid(self):
		return self.uid
	