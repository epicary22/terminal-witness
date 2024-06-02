import curses
from bitmap_layer import BitmapLayer
from bitmap_collection import BitmapCollection
from collision_binder import CollisionBinder
from curses_controller import CursesController
from transform_vector_2 import TransformVector2


bitmaps = BitmapCollection()

bounds = BitmapLayer(24 + 2, 80 + 2, (-1, -1))
bounds.set_all(True)
bounds.add_rect(False, 24, 80, (1, 1))
bounds.add_rect(True, 1, 1, (24, 80))
bounds.lock()
bitmaps.add(bounds, "bounds")

rect = BitmapLayer(3, 5, (1, 1))
rect.set_all(True)
rect.lock()
bitmaps.add(rect, "rect")

player_pos = TransformVector2()
player_hitbox = BitmapLayer(1, 1, player_pos.position())
player_hitbox.set_all(True)
bitmaps.add(player_hitbox, "player_hitbox")
