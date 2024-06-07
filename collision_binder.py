from bitmap_collection import BitmapCollection


class CollisionBinder:
	def __init__(self, bitmaps: BitmapCollection) -> None:
		"""
		Creates a new CollisionBinder. This can be used to bind the collision of two bitmaps to a function.
		:param bitmaps: The bitmaps to bind.
		"""
		self.bitmaps = bitmaps
		self.bindings: dict = {}
		
	def bind(self, bitmap_1: str, bitmap_2: str, function: ()) -> None:
		"""
		Binds the collision of two bitmaps to a function.
		:param bitmap_1: The name of the first bitmap in the provided collection.
		:param bitmap_2: The name of the second bitmap in the provided collection.
		:param function: The function to run when these two bitmaps collide.
		"""
		bitmap_tuple = (self.bitmaps.get(bitmap_1), self.bitmaps.get(bitmap_2))
		self.bindings.update({bitmap_tuple: function})
	
	def tick(self) -> None:
		"""
		Ticks the collision checker, running bound functions if objects collide.
		"""
		for bitmap_tuple, function in self.bindings.items():
			bitmap_1, bitmap_2 = bitmap_tuple
			if bitmap_1.collides(bitmap_2):
				function()
		