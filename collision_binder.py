from grid.bitmap_layer import BitmapLayer


class CollisionBinder:
	def __init__(self, collision_check_frequency: int) -> None:
		self.bindings: dict = {}
		self._bitmaps: dict = {}
		self._registered_ids = []
		if collision_check_frequency < 1:
			self.collision_check_frequency = 1
		else:
			self.collision_check_frequency = collision_check_frequency
		
	def bind(self, from_bitmap: BitmapLayer, to_bitmap: BitmapLayer, func: (), _id=-1) -> None:
		if _id < 0 or _id in self._registered_ids:
			_id = self._next_free_id()
		self._register_id(_id)
		
		from_uid = from_bitmap.get_uid()
		to_uid = to_bitmap.get_uid()
		self._bitmaps.update({from_uid: from_bitmap, to_uid: to_bitmap})
		if from_uid not in self.bindings.keys():
			self.bindings[from_uid] = {}
		self.bindings[from_uid][to_uid] = {"func": func, "id": _id}
	
	def _next_free_id(self) -> int:
		if not self._registered_ids:
			return 0
		registered_ids = sorted(self._registered_ids)
		for i in range(len(registered_ids)):
			if registered_ids[i] != i:
				return i
		return len(registered_ids)
	
	def _register_id(self, _id: int) -> None:
		self._registered_ids.append(_id)
	
	def tick(self) -> None:
		for from_bitmap_uid, to_bitmaps in self.bindings.items():
			for to_bitmap_uid, collision_properties in to_bitmaps.items():
				from_bitmap = self._bitmaps[from_bitmap_uid]
				to_bitmap = self._bitmaps[to_bitmap_uid]
				for collision_check_num in range(self.collision_check_frequency + 1):
					lerp_percent = collision_check_num / self.collision_check_frequency
					if from_bitmap.collides(to_bitmap, lerp_percent):
						collision_properties["func"]()
						break
		for bitmap in self._bitmaps.values():
			bitmap.position.update()
		