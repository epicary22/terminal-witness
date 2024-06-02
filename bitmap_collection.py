from bitmap_layer import BitmapLayer


def noop():
	pass


class BitmapCollection:
	def __init__(self):
		"""
		Creates a new BitmapCollection, an object that can store all of your BitmapLayers to be used by external
		processors.
		"""
		self.collection: dict = {}
		self._obj_name_counter = 0
		"""Internal value for automatically creating unique names"""
	
	def add(
		self,
		layer: BitmapLayer,
		name: str | None = None
		) -> None:
		"""
		Adds a layer with the given name to the collection of layers.
		Will replace the layer with the same name and layer if there is one.
		:param layer: The layer to be added.
		:param name: The name of the layer. If none is provided, a unique name will be generated.
		"""
		
		if name is None:
			name = self._generate_unique_name()
		self.collection.update({name: layer})
		
	def get(self, name: str) -> BitmapLayer:
		"""
		Returns the BitmapLayer in this collection with the given name.
		:param name: The name of the BitmapLayer to get.
		:return: The BitmapLayer with the given name.
		"""
		return self.collection.get(name)
	
	def _generate_unique_name(self) -> str:
		"""
		Generates a unique name for a bitmap in the collection.
		
		This method should only be used internally.
		:return: The unique name.
		"""
		name = f"o{self._obj_name_counter}"
		while name in self.collection.keys():
			self._obj_name_counter += 1
			name = f"o{self._obj_name_counter}"
		return name
