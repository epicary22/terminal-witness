import curses
from bitmap_layer import BitmapLayer


class Renderer:
	def __init__(self, window: curses.window) -> None:
		self.window = window
		self.render_objs = {}
	
	def add(self, bitmap: BitmapLayer, name: str, char: str, color_pair: int = -1, attrs: int = 0):
		self.render_objs.update({name: {"bitmap": bitmap, "char": char, "color_pair": color_pair, "attrs": attrs}})
		