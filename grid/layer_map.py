from grid.grid import Grid


class LayerMap(Grid):
	def __init__(self, t: type, height: int, width: int, top_left: tuple[int, int]) -> None:
		super().__init__(t, height, width)
		self._top_left = top_left
		