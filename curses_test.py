import curses
from curses_controller import CursesController
from cursor import Cursor

curses.initscr()


def main(stdscr: curses.window):
	curses.cbreak()
	
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
	
	stdscr.clear()
	stdscr.refresh()
	
	while True:
		# stdscr.clear()
		
		controller.run()
		pointer.update()
		stdscr.addstr(*pointer.position(), "X")
		# stdscr.addstr(2, 2, str(pointer.position()))
		
		stdscr.refresh()
	
	
curses.wrapper(main)
