import curses
from curses_controller import CursesController
from cursor import Cursor
from collisions_layer import CollisionsLayer

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
	box = CollisionsLayer(1, 1, (2, 2))
	box.set_all(True)
	
	while True:
		# update visuals
		stdscr.erase()

		pointer.update()
		stdscr.addstr(*pointer.position(), "X")
		stdscr.addstr(0, 0, str(box.collides_point(pointer.position())))
		
		stdscr.refresh()
		
		# take input
		controller.run()
	
	
curses.wrapper(main)
