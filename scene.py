import curses
import abc


class Scene(abc.ABC):
	"""
	Abstract base class for all scenes based on the curses stdscr.
	"""
	@abc.abstractmethod
	def __init__(self) -> None:
		"""
		Initializes the scene
		"""
		self.stdscr = curses.initscr()
	
	@abc.abstractmethod
	def update(self) -> None:
		pass
	
	
	