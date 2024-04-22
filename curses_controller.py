import curses
import sys


class CursesController:
	def __init__(self, stdscr: curses.window, bindings: list[tuple[str, ()]] = ()):
		"""
		Initializes a new Curses Controller, which should be attached to the standard screen (stdscr).
		:param stdscr: The standard window, from `curses.wrapper()` or `curses.initscr()`.
		:param bindings: The list of bindings to bind at initialization. Each binding is contained in a tuple, with each
		item being the arguments to pass to `CursesController.bind()`. (ex. [("j", go_down), ("^C", exit_func)])
		"""
		pass
		
	def bind(self, binding_key: str, binding_action: ()):
		"""
		Binds a single key to a single action, running that action when they key is pressed.
		:param binding_key: Any key name, in curses string form. (ex. ctrl-C -> "^C")
		:param binding_action: The action to run when the key is pressed.
		:return:
		"""
		
		