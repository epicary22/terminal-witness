from bitmap_layer import BitmapLayer


class CollisionsLayer:
	def __init__(
		self,
		collisions: BitmapLayer,
		on_collision: () = lambda: {},
		during_collision: () = lambda: {}
	):
		"""
		Creates a new collisions layer, which can be used for making colliding objects.
		:param collisions: The bitmap of collisions.
		:param on_collision: The function to call upon collision with another object. Must take two CollisionsLayers
			as parameters, and must return ``None``.
		:param during_collision: The function to call while an object is colliding with this layer. Must take two
			CollisionsLayers as parameters, and must return ``None``.
		"""
		self.collisions = collisions
		self.on_collision = on_collision
		self.during_collision = during_collision
		