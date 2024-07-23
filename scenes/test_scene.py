import curses
from bitmap_layer import BitmapLayer
from renderer import Renderer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
from curses_controller import CursesController
from transform_vector_2 import TransformVector2
from scene import Scene
from random import randint

# from grid.layer import Layer
import grid.bitmap_layer


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
		
		berry_boy = BitmapLayer(8, 15, (10, 10))
		berry_boy.add_rect(True, 1, 6, (0, 0))
		berry_boy.add_rect(True, 1, 5, (0, 9))
		berry_boy.set_point(True, *(1, 0))
		berry_boy.add_rect(True, 1, 2, (1, 2))
		berry_boy.set_point(True, *(1, 6))
		berry_boy.set_point(True, *(1, 8))
		berry_boy.add_rect(True, 1, 2, (1, 10))
		berry_boy.set_point(True, *(1, 13))
		berry_boy.set_point(True, *(3, 0))
		berry_boy.set_point(True, *(3, 7))
		berry_boy.set_point(True, *(4, 2))
		berry_boy.add_rect(True, 1, 3, (4, 6))
		berry_boy.set_point(True, *(4, 13))
		berry_boy.add_rect(True, 1, 4, (5, 3))
		berry_boy.add_rect(True, 1, 5, (5, 8))
		berry_boy.set_point(True, *(7, 7))
		self.bitmaps.add(berry_boy, "berry_boy")
		self.renderer.add(berry_boy, "berry_boy", " ", attrs=curses.A_REVERSE, color_pair=1)
		
		needle = BitmapLayer(1, 10, (10, 40))
		needle.set_all(True)
		needle.lock()
		self.bitmaps.add(needle, "needle")
		self.renderer.add(needle, "needle", "<", attrs=curses.A_NORMAL, color_pair=2)
		
		# player_hitbox = BitmapLayer(1, 1, (0, 0))
		# player_hitbox.set_all(True)
		# self.bitmaps.add(player_hitbox, "player_hitbox")
		# self.renderer.add(player_hitbox, "player_hitbox", "X", attrs=curses.A_NORMAL, color_pair=1)
		
		rect = BitmapLayer(3, 5, (1, 1))
		rect.set_all(True)
		rect.lock()
		self.bitmaps.add(rect, "rect")
		self.renderer.add(rect, "rect", "r", attrs=curses.A_REVERSE, color_pair=2)
		
		self.binder = CollisionBinder(self.bitmaps)
		
		self.binder.bind("berry_boy", "bounds", berry_boy.pos_vector.cancel_transform)
		self.binder.bind("berry_boy", "rect", berry_boy.pos_vector.cancel_transform)
		self.binder.bind("berry_boy", "needle", berry_boy.pos_vector.cancel_transform)
		
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": berry_boy.pos_vector.left,
				"j": berry_boy.pos_vector.down,
				"k": berry_boy.pos_vector.up,
				"l": berry_boy.pos_vector.right
			}
		)
		
		# layer_map = Layer(int, 2, 3, (0, 10))
		# layer_map.set_point((0, 1), 8)
		# layer_map.lock()
		# layer_map.set_point((0, 1), 100)
		# raise Exception(str(layer_map.grid))
		bl = grid.bitmap_layer.BitmapLayer(2, 3, (0, 0))
		bl.set_all(True)
		bl2 = grid.bitmap_layer.BitmapLayer(5, 5, (1, 1))
		bl2.set_point((1, 1), True)
		bl.position.add_transform((2, 1))
		intersection = bl2.intersect(bl, 0.5)
		raise Exception(bl.collides(bl2, 0.5), intersection.position.position(), intersection.grid)

	def update(self) -> None:
		# update visuals
		self.stdscr.erase()
		
		self.renderer.render()
		
		self.stdscr.refresh()
		
		# take input
		self.controller.run()

		# check collisions
		self.binder.tick()
		