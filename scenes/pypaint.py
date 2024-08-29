import curses
import typing

from scene import Scene
from curses_controller import CursesController
from grid.bitmap_layer import BitmapLayer
from grid.display_layer import DisplayLayer
from collision_binder import CollisionBinder
from renderer import Renderer
import time
import random
from enum import IntEnum


class PyPaint(Scene):
	class Colors(IntEnum):
		BG = 1
		CURSOR = 2
		COLON = 3
		PAIR_START = 10
		PAIR_END = 255
	
	def __init__(self):
		super().__init__()
		
		self.end = False
		
		self.screen_size_check()
		curses.resizeterm(24, 80)
		curses.cbreak()
		curses.curs_set(0)
		self.init_colors()
		self.brush_colors_registered = 0
		self.current_brush_color = self.Colors.CURSOR
		
		self.binder = CollisionBinder(1)
		self.renderer = Renderer(self.stdscr, curses.color_pair(self.Colors.BG))
		
		# menu
		canvas_size = (16, 56)
		screen_size = self.stdscr.getmaxyx()
		
		menu_border = BitmapLayer(*screen_size, (0, 0))
		menu_border.set_all(True)
		# (canvas space)
		menu_border.add_rect(*canvas_size, (1, 2), False)
		# (lower menu space)
		menu_border.add_rect(
			screen_size[0] - canvas_size[0] - 3,
			canvas_size[1],
			(canvas_size[0] + 2, 2),
			False
		)
		# (rgb flipper space)
		menu_border.add_rect(
			screen_size[0] - canvas_size[0],
			screen_size[1] - canvas_size[1] - 6,
			(canvas_size[0] - 1, canvas_size[1] + 4),
			False
		)
		menu_border.lock()
		self.renderer.add("menu_border", menu_border)
		
		canvas = DisplayLayer(*canvas_size, (1, 2))
		canvas.set_all(None)
		self.renderer.add("canvas", canvas)
		self.canvas = canvas
		
		brush = BitmapLayer(1, 1, (canvas_size[0] // 2, canvas_size[1] // 2))
		brush.set_all(True)
		self.renderer.add("brush", brush, z_layer=999)
		self.brush = brush
		
		# controller
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": brush.position.left,
				"j": brush.position.down,
				"k": brush.position.up,
				"l": brush.position.right,
				"f": lambda: canvas.r_set_point(brush.position.position(), ("#", self.current_brush_color)),
				"d": lambda: canvas.r_set_point(brush.position.position(), None),
				":": self.colon_command
			}
		)
		
		# collisions
		self.binder.bind(brush, menu_border, brush.position.cancel_transform)
		
	def update(self) -> None:
		self.stdscr.erase()
		self.renderer.render()
		self.stdscr.refresh()
		
		self.controller.run()
		
		self.binder.tick()
		
	def init_colors(self) -> None:
		bg_color = 7
		curses.init_pair(self.Colors.BG, bg_color, bg_color)
		curses.init_pair(self.Colors.CURSOR, 15, 0)
		curses.init_pair(self.Colors.COLON, 0, bg_color)
	
	def screen_size_check(self):
		max_y, max_x = self.stdscr.getmaxyx()
		if max_y < 24 or max_x < 80:
			self.end = True
			self.stdscr.erase()
			self.stdscr.addstr("Please resize the window to at least 80x24! ~Epicary")
			self.stdscr.refresh()
			for i in range(3, 0, -1):
				self.stdscr.addstr(2, 0, f"Crashing in {i}...")
				self.stdscr.refresh()
				time.sleep(1)
		
	def colon_command(self):
		# out of "game engine" mode
		curses.echo()
		curses.nocbreak()
		self.stdscr.attrset(curses.color_pair(self.Colors.COLON))
		
		self.stdscr.move(self.stdscr.getmaxyx()[0] - 1, 0)
		self.stdscr.addstr(":")
		self.stdscr.refresh()
		
		user_input = self.stdscr.getstr().split(b" ")
		command = b""
		args = []
		if len(user_input) > 0:
			command = user_input[0]
		if len(user_input) > 1:
			args = user_input[1:]
		
		self.stdscr.hline(self.stdscr.getmaxyx()[0] - 1, 0, " ", 100)
		self.stdscr.refresh()
		
		match command:
			case b"q":  # Quit
				self.end = True
			case b"t":  # Text
				args = [arg.decode() for arg in args]
				text = " ".join(args)
				start_point = self.brush.position.position()
				self.add_text_at(start_point, text)
			case b"c":  # brush Color
				args = [arg.decode() for arg in args]
				args = [int(arg) for arg in args if arg.isnumeric()]
				pair_number = min(self.Colors.PAIR_START + self.brush_colors_registered, self.Colors.PAIR_END)
				if len(args) == 1:
					curses.init_pair(pair_number, int(args[0]), int(args[0]))
					self.current_brush_color = pair_number
					self.brush_colors_registered += 1
				elif len(args) >= 2:
					curses.init_pair(pair_number, int(args[0]), int(args[1]))
					self.current_brush_color = pair_number
					self.brush_colors_registered += 1
			case b"m":  # Menu color
				args = [arg.decode() for arg in args]
				if len(args) >= 1:
					if args[0].isnumeric():
						curses.init_pair(self.Colors.BG, int(args[0]), int(args[0]))
						if PyPaint.color_is_dark(int(args[0])):
							curses.init_pair(self.Colors.COLON, 15, int(args[0]))
						else:
							curses.init_pair(self.Colors.COLON, 0, int(args[0]))
			case b"clear":
				self.canvas.set_all(None)
		
		# back into "game engine" mode
		curses.noecho()
		curses.cbreak()
		self.stdscr.attrset(curses.A_NORMAL)
		
	def add_text_at(self, point: tuple[int, int], text: str) -> None:
		text_display = DisplayLayer(1, len(text), point)
		for i in range(len(text)):
			text_display.set_point((0, i), (text[i], self.Colors.BG))
		self.renderer.add(f"text_{text}", text_display)
		
	@staticmethod
	def color_is_dark(color_number: int) -> bool:
		if color_number <= 8:
			return True
		if 232 <= color_number <= 244:
			return False
		adjusted_color = color_number - 16
		color_rgb = (adjusted_color // 36, (adjusted_color % 36) // 6, adjusted_color % 6)
		if max(color_rgb) >= 4 and sum(color_rgb) >= 6:
			return False
		return True
		