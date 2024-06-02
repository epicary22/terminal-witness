import curses
import abc


class Scene(abc.ABC):
	"""
	Abstract base class for all scenes based on the curses stdscr.
	"""
	@abc.abstractmethod
	def __init__(self, stdscr: curses.window) -> None:
		"""
		Initializes the scene
		:param stdscr:
		"""
		self.stdscr = curses.initscr()
	
	@abc.abstractmethod
	def update(self) -> None:
		pass
	
	
	