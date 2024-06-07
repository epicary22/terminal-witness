import curses
from scenes.terminal_witness import TerminalWitness

curses.initscr()


def main(stdscr: curses.window):
	game = TerminalWitness()
	
	while True:
		game.update()


curses.wrapper(main)
