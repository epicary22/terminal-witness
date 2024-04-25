class CursesController:
	def __init__(self, key_supplier: (), bindings: dict[str, ()] = ()) -> None:
		"""
		Initializes a new Curses Controller.
		:param key_supplier: A function that supplies which keys are being pressed. (usually `stdscr.getkey()`)
		:param bindings: The list of bindings to bind at initialization. Each binding is contained in a tuple, with
			each item being the arguments to pass to `CursesController.bind()`.
			(ex. ``{"j": go_down_func, "^C": exit_func}``)
		"""
		self.key_supplier = key_supplier
		self.bindings: dict = {}
		for key, binding in bindings.items():
			self.bind(key, binding)
		
	def bind(self, binding_key: str, binding_action: ()) -> None:
		"""
		Binds a single key to a single action, running that action when they key is pressed.
		If a bound action already exists for that key, it replaces the old binding.
		:param binding_key: Any key name, in curses string form. (ex. j -> "j", ctrl-C -> "^C")
		:param binding_action: The action to run when the key is pressed.
		"""
		self.bindings.update({binding_key: binding_action})

	# def key_is_down(self):
	# 	"""
	# 	Returns true if a key is currently down.
	# 	:return: Whether a key is currently down.
	# 	"""
	# 	return bool(self.key_supplier())
	
	def run(self) -> bool:
		"""
		Runs the Curses Controller, checking for input then running the bound action, if any.
		:return: Whether a bound action was run.
		"""
		current_key = self.key_supplier()
		bound_action = self.bindings.get(current_key)
		if bound_action:
			bound_action()
			return True
		else:
			return False
		