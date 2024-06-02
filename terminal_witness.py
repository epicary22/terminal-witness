import curses
from bitmap_layer import BitmapLayer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
from curses_controller import CursesController
from transform_vector_2 import TransformVector2
from scene import Scene


class TerminalWitness(Scene):
	def __init__(self, stdscr: curses.window):
		super().__init__(stdscr)
		
		self.bitmaps = BitmapCollection()
		
		bounds = BitmapLayer(curses.LINES + 2, curses.COLS + 2, (-1, -1))
		bounds.set_all(True)
		bounds.add_rect(False, curses.LINES, curses.COLS, (1, 1))
		bounds.add_rect(True, 1, 1, (curses.LINES, curses.COLS))
		bounds.lock()
		self.bitmaps.add(bounds, "bounds")
		
		rect = BitmapLayer(3, 5, (1, 1))
		rect.set_all(True)
		rect.lock()
		self.bitmaps.add(rect, "rect")
		
		self.player_pos = TransformVector2()
		player_hitbox = BitmapLayer(1, 1, self.player_pos.position())
		player_hitbox.set_all(True)
		self.bitmaps.add(player_hitbox, "player_hitbox")
		
		self.binder = CollisionBinder(self.bitmaps)
		
		self.binder.bind("player_hitbox", "bounds", self.player_pos.cancel_transform)
		self.binder.bind("player_hitbox", "rect", self.player_pos.zero_axes)
		
		self.controller = CursesController(
			stdscr.getkey,
			{
				"h": self.player_pos.left,
				"j": self.player_pos.down,
				"k": self.player_pos.up,
				"l": self.player_pos.right
			}
		)

	def update(self) -> None:
		# update visuals
		self.stdscr.erase()
		
		try:
			self.stdscr.addstr(*self.bitmaps.get("player_hitbox").top_left(), "X")
			self.stdscr.addstr(*self.bitmaps.get("rect").top_left(), "r")
		except curses.error:
			pass
		
		self.stdscr.refresh()
		
		# take input
		self.controller.run()
		
		# test if the new hitbox collisions don't collide
		self.bitmaps.get("player_hitbox").set_top_left(self.player_pos.next_position())
		
		# check collisions
		self.binder.tick()
		
		# update the hitbox accordingly
		self.player_pos.update()
		self.bitmaps.get("player_hitbox").set_top_left(self.player_pos.position())
		