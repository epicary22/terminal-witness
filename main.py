import curses
from scenes.test_scene import TestScene
from scenes.pypaint import PyPaint

curses.initscr()


def main(stdscr: curses.window):
	game = PyPaint()
	
	while True:
		game.update()


curses.wrapper(main)
