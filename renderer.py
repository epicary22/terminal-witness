import curses
from bitmap_layer import BitmapLayer


class Renderer:
	def __init__(self, window: curses.window) -> None:
		self.window = window
		self.z_layers = {}
	
	def add(
		self, bitmap: BitmapLayer,
		name: str, char: str, z_layer: int = 0, color_pair: int = 1, attrs: int = curses.A_NORMAL
		) -> None:
		# register z-layer if it doesn't exist yet
		if z_layer not in self.z_layers.keys():
			self.z_layers.update({z_layer: {}})
		
		self.z_layers[z_layer].update({
			name: {
				"bitmap": bitmap,
				"char": char,
				"color_pair": color_pair,
				"attrs": attrs
			}
		})
		
		# sort the z-layers
		self.z_layers = dict(sorted(self.z_layers.items(), key=lambda item: item[0]))
	
	def render(self) -> None:
		for z_layer in self.z_layers.values():
			for render_obj in z_layer.values():
				self._render_obj(render_obj)
	
	def _render_obj(self, render_obj: dict) -> None:
		bitmap: BitmapLayer = render_obj["bitmap"]
		top_y = bitmap.top_y
		bottom_y = bitmap.top_y + bitmap.y_size
		left_x = bitmap.left_x
		right_x = bitmap.left_x + bitmap.x_size
		attributes = render_obj["attrs"] | curses.color_pair(render_obj["color_pair"])
		
		for y_coord in range(top_y, bottom_y):
			for x_coord in range(left_x, right_x):
				lookup_point = bitmap.relative_yx(y_coord, x_coord)
				if bitmap.bit_at_point(*lookup_point):
					try:
						self.window.addch(y_coord, x_coord, render_obj["char"], attributes)
					except curses.error:
						pass  # just let things be rendered off-screen
		