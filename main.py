import curses
from scenes.test_scene import TestScene
from scenes.pypaint import PyPaint

curses.initscr()


def main(stdscr: curses.window):
	# game = TestScene()
	game = PyPaint()
	while not game.end:
		game.update()
		

curses.wrapper(main)
