from collisions_layer import CollisionsLayer


class CollisionsCollection:
	def __init__(self):
		"""
		Creates a new CollisionsCollection, an object that can store all of your CollisionsLayers and assign them
		z-layers and actions upon collision, among other useful properties.
		"""
		self.collection = {}
	
	def add(self, layer: CollisionsLayer, name: str, z_layer: int | None = None) -> None:
		"""
		Adds a layer with the given name and z-layer value to the collection of layers.
		Will replace the layer with the same name if there is one.
		:param name: The name of the layer.
		:param z_layer: The z-layer value of the layer; higher number layers get rendered on top of lower number layers.
			If the layer shouldn't be rendered, leave this value as None (default).
		:param layer: The layer to be added.
		"""
		if z_layer is None:
			self.collection.update({"no_render": {name: layer}})
		self.collection.update({"render": {z_layer: {name: layer}}})
		