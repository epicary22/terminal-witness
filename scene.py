import curses
import abc


class Scene(abc.ABC):
	"""
	Abstract base class for all scenes based on the curses stdscr.
	"""
	@abc.abstractmethod
	def __init__(self) -> None:
		"""
		Initializes the Scene.
		Put your code to be called before the Scene starts here.
		"""
		self.stdscr = curses.initscr()
	
	@abc.abstractmethod
	def update(self) -> None:
		"""
		Updates the scene. Put your code to be called every frame here.
		"""
		pass
	
	
	