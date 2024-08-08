import curses
from scene import Scene
from curses_controller import CursesController
from grid.bitmap_layer import BitmapLayer
from collision_binder import CollisionBinder
from renderer import Renderer
import time
import random
from enum import IntEnum


class PyPaint(Scene):
	class Colors(IntEnum):
		BG = 1
		CURSOR = 2
	
	def __init__(self):
		super().__init__()
		
		self.end = False
		
		self.screen_size_check()
		curses.resizeterm(24, 80)
		curses.cbreak()
		curses.curs_set(0)
		self.init_colors()
		
		self.binder = CollisionBinder(1)
		self.renderer = Renderer(self.stdscr, curses.color_pair(1))
		
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
		
		canvas = BitmapLayer(*canvas_size, (1, 2))
		canvas.set_all(False)
		self.renderer.add("canvas", canvas)
		
		cursor = BitmapLayer(1, 1, (canvas_size[0] // 2, canvas_size[1] // 2))
		cursor.set_all(True)
		self.renderer.add("cursor", cursor)
		
		# controller
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": cursor.position.left,
				"j": cursor.position.down,
				"k": cursor.position.up,
				"l": cursor.position.right,
				"f": lambda: canvas.r_set_point(cursor.position.position(), True),
				"d": lambda: canvas.r_set_point(cursor.position.position(), False),
				"c": lambda: canvas.set_all(False),
				":": self.colon_command
			}
		)
		
		# collisions
		self.binder.bind(cursor, menu_border, cursor.position.cancel_transform)
		
	def update(self) -> None:
		self.stdscr.erase()
		self.renderer.render()
		self.stdscr.refresh()
		
		self.controller.run()
		
		self.binder.tick()
		
	def init_colors(self) -> None:
		bg_color = random.randint(9, 15)
		curses.init_pair(self.Colors.BG, bg_color, bg_color)
		curses.init_pair(self.Colors.CURSOR, 15, 0)
	
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
		self.stdscr.attrset(curses.color_pair(self.Colors.BG))
		
		self.stdscr.move(self.stdscr.getmaxyx()[0] - 1, 0)
		self.stdscr.addstr(":")
		self.stdscr.refresh()
		
		user_input = ""
		while not user_input:
			user_input = self.stdscr.getstr()
		
		self.stdscr.hline(self.stdscr.getmaxyx()[0] - 1, 0, " ", 100)
		self.stdscr.refresh()
		
		match user_input:
			case b"q":
				self.end = True
			case b"star":
				star = BitmapLayer(3, 6, (2, 4))
				star.add_rect(3, 2, (0, 2), True)
				star.add_rect(1, 6, (1, 0), True)
				self.renderer.add("star", star)
				
		# back into "game engine" mode
		curses.noecho()
		curses.cbreak()
		self.stdscr.attrset(curses.A_NORMAL)
		