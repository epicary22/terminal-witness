import curses
from bitmap_layer import BitmapLayer
from renderer import Renderer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
from curses_controller import CursesController
from transform_vector_2 import TransformVector2
from scene import Scene
from random import randint


class TestScene(Scene):
	def __init__(self):
		super().__init__()
		
		curses.cbreak()
		curses.curs_set(0)
		
		self.bitmaps = BitmapCollection()
		self.renderer = Renderer(self.stdscr)
		
		curses.init_pair(1, randint(0, 255), randint(0, 255))
		curses.init_pair(2, randint(0, 255), randint(0, 255))
		
		bounds = BitmapLayer(curses.LINES + 2, curses.COLS + 2, (-1, -1))
		bounds.set_all(True)
		bounds.add_rect(False, curses.LINES, curses.COLS, (1, 1))
		bounds.add_rect(True, 1, 1, (curses.LINES, curses.COLS))
		bounds.lock()
		self.bitmaps.add(bounds, "bounds")
		
		player_hitbox = BitmapLayer(1, 1, (0, 0))
		player_hitbox.set_all(True)
		self.bitmaps.add(player_hitbox, "player_hitbox")
		self.renderer.add(player_hitbox, "player_hitbox", "X", attrs=curses.A_NORMAL, color_pair=1)
		
		rect = BitmapLayer(3, 5, (1, 1))
		rect.set_all(True)
		rect.lock()
		self.bitmaps.add(rect, "rect")
		self.renderer.add(rect, "rect", "r", attrs=curses.A_REVERSE, color_pair=2)
		
		self.binder = CollisionBinder(self.bitmaps)
		
		self.binder.bind("player_hitbox", "bounds", player_hitbox.vector.cancel_transform)
		self.binder.bind("player_hitbox", "rect", player_hitbox.vector.cancel_transform)
		
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": player_hitbox.vector.left,
				"j": player_hitbox.vector.down,
				"k": player_hitbox.vector.up,
				"l": player_hitbox.vector.right
			}
		)

	def update(self) -> None:
		# update visuals
		self.stdscr.erase()
		
		self.renderer.render()
		
		self.stdscr.refresh()
		
		# take input
		self.controller.run()

		# check collisions
		self.binder.tick()
		