import curses
from curses_controller import CursesController
from cursor import Cursor

curses.initscr()


def main(stdscr: curses.window):
	curses.cbreak()
	
	controller = CursesController(
		stdscr.getkey,
		{
			"h": lambda: stdscr.addstr("left"),
			"j": lambda: stdscr.addstr("down"),
			"k": lambda: stdscr.addstr("up"),
			"l": lambda: stdscr.addstr("right")
		}
	)
	pointer = Cursor()
	
	stdscr.clear()
	stdscr.refresh()
	
	while True:
		controller.run()
		stdscr.refresh()
	
	
curses.wrapper(main)
