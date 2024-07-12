import curses
from scene import Scene
from curses_controller import CursesController
from bitmap_layer import BitmapLayer
from bitmap_collection import BitmapCollection
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
		
		self.screen_size_check()
		curses.resizeterm(24, 80)
		curses.cbreak()
		curses.curs_set(0)
		self.init_colors()
		
		self.end = False
		
		self.bitmaps = BitmapCollection()
		self.collisions = CollisionBinder(self.bitmaps)
		self.renderer = Renderer(self.stdscr)
		
		# menu
		canvas_size = (16, 56)
		screen_size = self.stdscr.getmaxyx()
		
		menu_border = BitmapLayer(*screen_size, (0, 0))
		menu_border.set_all(True)
		# (canvas space)
		menu_border.add_rect(False, *canvas_size, (1, 2))
		# (lower menu space)
		menu_border.add_rect(
			False,
			screen_size[0] - canvas_size[0] - 3,
			canvas_size[1],
			(canvas_size[0] + 2, 2)
		)
		# (rgb flipper space)
		menu_border.add_rect(
			False,
			screen_size[0] - canvas_size[0],
			screen_size[1] - canvas_size[1] - 6,
			(canvas_size[0] - 1, canvas_size[1] + 4)
		)
		menu_border.lock()
		self.bitmaps.add(menu_border, "menu_border")
		self.renderer.add(menu_border, "menu_border", " ", attrs=curses.A_REVERSE, color_pair=self.Colors.BG)
		
		canvas = BitmapLayer(*canvas_size, (1, 2))
		self.bitmaps.add(canvas, "canvas")
		self.renderer.add(canvas, "canvas", " ", z_layer=-1, attrs=curses.A_REVERSE, color_pair=self.Colors.CURSOR)
		
		cursor = BitmapLayer(1, 1, (canvas_size[0] // 2, canvas_size[1] // 2))
		cursor.set_all(True)
		self.bitmaps.add(cursor, "cursor")
		self.renderer.add(cursor, "cursor", "X", attrs=curses.A_NORMAL, color_pair=self.Colors.CURSOR)
		
		# controler
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": cursor.pos_vector.left,
				"j": cursor.pos_vector.down,
				"k": cursor.pos_vector.up,
				"l": cursor.pos_vector.right,
				"f": lambda: canvas.set_point(True, *canvas.relative_yx(*cursor.top_left())),
				"d": lambda: canvas.set_point(False, *canvas.relative_yx(*cursor.top_left())),
				"c": lambda: canvas.set_all(False),
				":": self.colon_command
			}
		)
		
		# collisions
		self.collisions.bind("cursor", "menu_border", cursor.pos_vector.cancel_transform)
		
	def update(self) -> None:
		self.stdscr.erase()
		self.renderer.render()
		self.stdscr.refresh()
		
		self.controller.run()
		
		self.collisions.tick()
		
	def init_colors(self) -> None:
		curses.init_pair(self.Colors.BG, random.randint(9, 15), 0)
		curses.init_pair(self.Colors.CURSOR, 15, 0)
	
	def screen_size_check(self):
		max_y, max_x = self.stdscr.getmaxyx()
		if max_y < 24 or max_x < 80:
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
		self.stdscr.attrset(curses.color_pair(self.Colors.BG) | curses.A_REVERSE)
		
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
				star.add_rect(True, 3, 2, (0, 2))
				star.add_rect(True, 1, 6, (1, 0))
				self.renderer.add(
					star,
					"star",
					" ",
					attrs=curses.A_REVERSE,
					color_pair=self.Colors.BG
				)
				
		# back into "game engine" mode
		curses.noecho()
		curses.cbreak()
		self.stdscr.attrset(curses.A_NORMAL)
		