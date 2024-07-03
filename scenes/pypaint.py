import curses
from scene import Scene
from curses_controller import CursesController
from bitmap_layer import BitmapLayer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
from renderer import Renderer
import time


class PyPaint(Scene):
	def __init__(self):
		super().__init__()
		
		self.screen_size_check()
		
		curses.cbreak()
		curses.curs_set(0)
		curses.resizeterm(24, 80)
		
		curses.init_pair(1, 9, 0)
		
		self.bitmaps = BitmapCollection()
		self.collisions = CollisionBinder(self.bitmaps)
		self.renderer = Renderer(self.stdscr)
		
		# bitmap definitions
		canvas_size = (16, 56)
		canvas_border = BitmapLayer(canvas_size[0] + 2, canvas_size[1] + 4, (0, 0))
		canvas_border.set_all(True)
		canvas_border.add_rect(False, canvas_size[0], canvas_size[1], (1, 2))
		canvas_border.lock()
		self.bitmaps.add(canvas_border, "canvas_border")
		self.renderer.add(canvas_border, "canvas_border", " ", attrs=curses.A_REVERSE)
		
		cursor = BitmapLayer(1, 1, (canvas_size[0] // 2, canvas_size[1] // 2))
		cursor.set_all(True)
		self.bitmaps.add(cursor, "cursor")
		self.renderer.add(cursor, "cursor", "X", z_layer=-1, attrs=curses.A_NORMAL)
		
		# controler
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": cursor.pos_vector.left,
				"j": cursor.pos_vector.down,
				"k": cursor.pos_vector.up,
				"l": cursor.pos_vector.right
			}
		)
		
		# collisions
		self.collisions.bind("cursor", "canvas_border", cursor.pos_vector.cancel_transform)
		
	def update(self) -> None:
		self.stdscr.erase()
		
		self.renderer.render()
		
		self.stdscr.addstr(str(self.bitmaps.get("cursor").top_left()))
		
		self.stdscr.refresh()
		
		self.controller.run()
		
		self.collisions.tick()
		
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
		