import curses
from curses_controller import CursesController
from cursor import Cursor
from bitmap_layer import BitmapLayer
from collisions_collection import CollisionsCollection

curses.initscr()


def main(stdscr: curses.window):
	curses.cbreak()
	curses.curs_set(0)
	
	pointer = Cursor()
	controller = CursesController(
		stdscr.getkey,
		{
			"h": pointer.left,
			"j": pointer.down,
			"k": pointer.up,
			"l": pointer.right
		}
	)
	
	bounds = BitmapLayer(curses.LINES + 2, curses.COLS + 2, (-1, -1))
	bounds.set_all(True)
	bounds.add_rect(False, curses.LINES, curses.COLS, (1, 1))
	bounds.add_rect(True, 1, 1, (curses.LINES, curses.COLS))
	bounds.lock()
	
	collection = CollisionsCollection()
	collection.add(bounds, "bounds")
	
	while True:
		# update visuals
		stdscr.erase()

		pointer.update()
		stdscr.addstr(*pointer.position(), "X")
		
		stdscr.refresh()
		
		# take input
		controller.run()
		
		# check collisions
		if bounds.collides_point(pointer.next_position()):
			pointer.cancel_transform()
		
	
curses.wrapper(main)
