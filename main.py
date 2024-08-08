import curses
from scenes.test_scene import TestScene
from scenes.pypaint import PyPaint

curses.initscr()


def main(stdscr: curses.window):
	game = PyPaint()
	
	while not game.end:
		game.update()
		if game.end:
			raise Exception()


curses.wrapper(main)
