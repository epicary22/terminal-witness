import curses
from curses_controller import CursesController
from transform_vector_2 import TransformVector2
from bitmap_layer import BitmapLayer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
import terminal_witness

curses.initscr()


def main(stdscr: curses.window):
	curses.cbreak()
	curses.curs_set(0)
	
	bitmaps = terminal_witness.bitmaps
	player_pos = terminal_witness.player_pos
	
	controller = CursesController(
		stdscr.getkey,
		{
			"h": player_pos.left,
			"j": player_pos.down,
			"k": player_pos.up,
			"l": player_pos.right
		}
	)
	
	binder = CollisionBinder(bitmaps)
	
	binder.bind("player_hitbox", "bounds", player_pos.cancel_transform)
	binder.bind("player_hitbox", "rect", player_pos.zero_axes)
	
	curses.init_pair(255, 15, 255)
	
	while True:
		# update visuals
		stdscr.erase()

		stdscr.addstr(str(binder.bindings))
		player_pos.update()
		bitmaps.get("player_hitbox").set_top_left(player_pos.position())
		stdscr.addstr(*bitmaps.get("player_hitbox").top_left(), "X", curses.color_pair(255))
		
		stdscr.refresh()
		
		# take input
		controller.run()
		
		# temp. make the player hitbox have the future position
		bitmaps.get("player_hitbox").set_top_left(player_pos.next_position())
		##
		
		# check collisions
		binder.tick()
		
	
curses.wrapper(main)
