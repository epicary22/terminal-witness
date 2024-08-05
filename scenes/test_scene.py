import curses
from grid.bitmap_layer import BitmapLayer
from grid.layer import Layer
from renderer import Renderer
from collision_binder import CollisionBinder
from curses_controller import CursesController
from scene import Scene
from random import randint

def crash(info):
	raise Exception(info)


class TestScene(Scene):
	def __init__(self):
		super().__init__()
		
		curses.cbreak()
		curses.curs_set(0)
		
		curses.init_pair(1, randint(0, 255), randint(0, 255))
		curses.init_pair(2, randint(0, 255), randint(0, 255))
		
		self.binder = CollisionBinder(3)
		self.renderer = Renderer(self.stdscr, curses.color_pair(1))
		
		bounds = BitmapLayer(curses.LINES + 2, curses.COLS + 2, (-1, -1))
		bounds.set_all(True)
		bounds.add_rect(curses.LINES, curses.COLS, (1, 1), False)
		bounds.add_rect(1, 1, (curses.LINES, curses.COLS), True)
		bounds.lock()
		self.renderer.add("bounds", bounds, 999)
		
		cursor = BitmapLayer(1, 1, (15, 30))
		cursor.set_all(True)
		self.renderer.add("cursor", cursor)
		
		berry_boy = BitmapLayer(8, 15, (10, 10))
		berry_boy.add_rect(1, 6, (0, 0), True)
		berry_boy.add_rect(1, 5, (0, 9), True)
		berry_boy.set_point((1, 0), True)
		berry_boy.add_rect(1, 2, (1, 2), True)
		berry_boy.set_point((1, 6), True)
		berry_boy.set_point((1, 8), True)
		berry_boy.add_rect(1, 2, (1, 10), True)
		berry_boy.set_point((1, 13), True)
		berry_boy.set_point((3, 0), True)
		berry_boy.set_point((3, 7), True)
		berry_boy.set_point((4, 2), True)
		berry_boy.add_rect(1, 3, (4, 6), True)
		berry_boy.set_point((4, 13), True)
		berry_boy.add_rect(1, 4, (5, 3), True)
		berry_boy.add_rect(1, 5, (5, 8), True)
		berry_boy.set_point((7, 7), True)
		self.renderer.add("berry_boy", berry_boy)
		
		needle = BitmapLayer(4, 10, (10, 40))
		needle.set_all(True)
		needle.lock()
		self.renderer.add("needle", needle)
		
		# player_hitbox = BitmapLayer(1, 1, (0, 0))
		# player_hitbox.set_all(True)
		# self.bitmaps.add(player_hitbox, "player_hitbox")
		# self.renderer.add(player_hitbox, "player_hitbox", "X", attrs=curses.A_NORMAL, color_pair=1)
		
		rect = BitmapLayer(3, 5, (1, 1))
		rect.set_all(True)
		rect.lock()
		self.renderer.add("rect", rect)
		
		self.binder.bind(berry_boy, bounds, lambda: crash("hit the bounds"))
		self.binder.bind(berry_boy, rect, berry_boy.position.cancel_transform)
		self.binder.bind(berry_boy, needle, berry_boy.position.cancel_transform)
		
		self.controller = CursesController(
			self.stdscr.getkey,
			{
				"h": berry_boy.position.left,
				"j": berry_boy.position.down,
				"k": berry_boy.position.up,
				"l": berry_boy.position.right
			}
		)
		#
		# # layer_map = Layer(int, 2, 3, (0, 10))
		# # layer_map.set_point((0, 1), 8)
		# # layer_map.lock()
		# # layer_map.set_point((0, 1), 100)
		# # raise Exception(str(layer_map.grid))
		# bl = grid.bitmap_layer.BitmapLayer(2, 3, (0, 0))
		# bl.set_all(True)
		# bl2 = grid.bitmap_layer.BitmapLayer(5, 5, (1, 1))
		# bl2.set_point((1, 1), True)
		# bl.position.add_transform((2, 1))
		# intersection = bl2.intersect(bl, 0.5)
		# rect = grid.bitmap_layer.BitmapLayer(4, 6, (0, 5))
		# rect.position.add_transform((1, 1))
		# rect.r_add_rect(4, 6, (0, 5), True, 0.5)
		# # rect.add_rect(2, 4, (1, 1), True)
		# # rect.add_rect(1, 2, (2, 2), False)
		# raise Exception(rect.grid)
		# # raise Exception(bl.collides(bl2, 0.5), intersection.position.position(), intersection.grid)

	def update(self) -> None:
		# update visuals
		self.stdscr.erase()
		
		self.renderer.render()
		
		self.stdscr.refresh()
		
		# take input
		self.controller.run()

		# check collisions
		self.binder.tick()
		
