import curses
import typing
from grid.layer import Layer
from grid.bitmap_layer import BitmapLayer
from grid.display_layer import DisplayLayer


class Renderer:
	
	def __init__(self, window: curses.window, default_attributes: int) -> None:
		self.window = window
		self.default_attributes = default_attributes
		self.z_layers = {}
	
	def add(self, name: str, layer: Layer, z_layer: int = 0) -> None:
		# register z-layer if it doesn't exist yet
		if z_layer not in self.z_layers.keys():
			self.z_layers.update({z_layer: {}})
		
		self.z_layers[z_layer][name] = layer
		
		# sort the z-layers
		self.z_layers = dict(sorted(self.z_layers.items(), key=lambda item: item[0]))
	
	def render(self) -> None:
		for z_layer in self.z_layers.values():
			for layer in z_layer.values():
				self.render_layer(layer)
	
	def render_layer(self, layer: Layer) -> None:
		layer_type = type(layer)
		top_y, left_x = layer.position.position()
		bottom_y = top_y + layer.height - 1
		right_x = left_x + layer.width - 1
		
		for y in range(top_y, bottom_y + 1):
			for x in range(left_x, right_x + 1):
				point_contents = layer.r_value_at((y, x))
				if point_contents:
					try:
						self.window.addstr(y, x, *self._generate_cell_graphic(layer_type, point_contents))
					except curses.error:
						pass  # just let things be rendered off-screen
				
	def _generate_cell_graphic(self, layer_type: type, point_contents: typing.Any) -> tuple[str, int]:
		if layer_type is BitmapLayer:
			return "#", self.default_attributes
		elif layer_type is DisplayLayer:
			return point_contents[0][0], curses.color_pair(point_contents[1])
		elif layer_type is Layer:
			return (str(point_contents) + " ")[0], self.default_attributes
		