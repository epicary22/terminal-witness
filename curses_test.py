import curses
import terminal_witness

curses.initscr()


def main(stdscr: curses.window):
	curses.cbreak()
	curses.curs_set(0)
	
	game = terminal_witness.TerminalWitness(stdscr)
	
	while True:
		game.update()
		
	
curses.wrapper(main)
