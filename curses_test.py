import curses
from curses_controller import CursesController
from cursor import Cursor

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
	
	while True:
		# update visuals
		stdscr.erase()

		pointer.update()
		stdscr.addstr(*pointer.position(), "X")
		
		stdscr.refresh()
		
		# take input
		controller.run()
	
	
curses.wrapper(main)
