import curses
from scenes.test_scene import TestScene

curses.initscr()


def main(stdscr: curses.window):
	game = TestScene()
	
	while True:
		game.update()


curses.wrapper(main)
