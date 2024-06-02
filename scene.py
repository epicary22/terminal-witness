import curses
import abc


class Scene(abc.ABC):
	@abc.abstractmethod
	def __init__(self, stdscr: curses.window) -> None:
		pass
	
	