from bitmap_layer import BitmapLayer


def noop():
	pass


class CollisionsCollection:
	def __init__(self):
		"""
		Creates a new CollisionsCollection, an object that can store all of your CollisionsLayers and assign them
		z-layers and actions upon collision, among other useful properties.
		"""
		self.collection = {"no_render": {}, "render": {}}
		self._obj_name_counter = 0
		"""Internal value for automatically creating unique names"""
	
	def add(
		self,
		layer: BitmapLayer,
		on_collision: () = noop,
		z_layer: int | None = None,
		name: str | None = None
		) -> None:
		"""
		Adds a layer with the given name and z-layer value (or lack thereof) to the collection of layers.
		Will replace the layer with the same name and layer if there is one.
		:param layer: The layer to be added.
		:param on_collision: The function to run when this object collides with something. If no function is given,
			it will run a no-op (which does nothing).
		:param z_layer: The z-layer value of the layer. Higher number layers get rendered on top of lower number layers.
			If the layer shouldn't be rendered, leave this value as None (default).
		:param name: The name of the layer. If none is provided, a unique name will be generated.
		"""
		collection_to_update: dict
		if z_layer is None:
			collection_to_update = self.collection["no_render"]
		else:
			collection_to_update = self.collection["render"][z_layer]
		
		if name is None:
			name = self._generate_unique_name(collection_to_update)
		collection_to_update.update({name: {"layer": layer, "action": on_collision}})
	
	def _generate_unique_name(self, collection: dict) -> str:
		"""
		This method should only be used internally. Generates a unique name for a layer in a part of the collection.
		:param collection: The part of the collection to generate a unique name for.
		:return: The unique name.
		"""
		name = f"o{self._obj_name_counter}"
		while name in collection.keys():
			self._obj_name_counter += 1
			name = f"o{self._obj_name_counter}"
		return name
