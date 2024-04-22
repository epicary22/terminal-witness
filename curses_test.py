import curses
from curses_controller import CursesController

curses.initscr()


def main(stdscr: curses.window):
	controller = CursesController(stdscr)
	stdscr.clear()
	stdscr.refresh()
	curses.cbreak()
	
	while True:
		stdscr.getkey()
	
	
curses.wrapper(main)
