# My Plan Right Now
<hr>

I want three BitmapCollections:
* A physics one that is fed to a PhysicsHandler to handle physics every update
* A collisions one that is fed to a CollisionsHandler to run actions upon/during collisions with objects (ex. standing on a switch)
* A rendering one that is fed to a Renderer, which does about what it says it would do

These three could all take the same objects.

<br><br><br><br><br><br><br><br><br><br><br><br><br><br>
<code style="text-align:center">/////////////// warning! thoughts below ///////////////</code>  

Okay hear me out: what if we had object take a list of tags that they'd use to figure out what their purposes are. So like ProcessingTag.RENDER, ProcessingTag.COLLIDE, ProcessingTag.PHYSICS, etc. These would be used to direct the layers to the right processors, and you could tell what processing a layer will get just by looking at the layer. At that point, each layer would also require an attribute that its processer requires of it... so the ProcessingTag thing would be directly connected to the requirements of the Processor. Okay okay okay so that means I need to Processors before I make the ProcessingTags, before I can make the BitmapObjects use these tags. Or maybe I can make stand-ins for now. Stub methods. The like.

SO ANYWAYS, the processors would require:
* Physics: a PhysicsMaterial attribute
* Collision: on_collision, during_collision, and out_collision methods
* Render: color and character attributes

So how would I hand it its requirements? I would make each GameObject have a list of RequirementPlugins that would tell it which requirements it needs. Though it would be nice to hand these in at the init... I want to somehow make the requirements branch out of the processors themselves. Is there any simpler way of doing this? I'm sure there is. This is just too abstracted, and I'm going to drive myself crazy like this. The thing is I want the objects to be able to reference each other and themselves, at that becomes seemingly impossible if I don't abstract it to this length. Maybe I still apply the processing tags at the GameObject level, but I don't actually say how they interact with each other until they reach the Collection level.

What I want to happen is that when I (player) touch a button, it sends out a signal to turn another object yellow. So that's like 
```py
def on_collision(self_object, other_object):
    obj_to_turn_yellow.color = Color.YELLOW
```
But I also want it to be static for the Witness. Aaaaaaaaaaaaaa this is why you use a prebuilt game engine. NO. I want to make my own engine once and for all!!!!!! I think I will have to define unique behaviors in script files that I attach to each object. That's the only feasible way it seems. But that's for another day. I need a starting point, and making the Witness seems to be a good one.









So, I want to make a working physics engine for what requires physics. This will be processed on one CollisionsCollection, with members possibly joint with another rendering CollisionsCollection. 

List of what I want:
* Physics CollisionsCollection, where all the members have CollisionsMaterials
* Non-physics CollisionsCollection, where everything has an action upon collision but doesn't have rigidbody physics
* Rendering CollisionsCollection, where the sole purpose of the bitmaps is to render

How this will work:
* For the physics collection, I want a PhysicsHandler that can take the collection and run all the physics on it.
* For collidable collections (like buttons or touchable walls), I want something that can call the actions of the colliding objects based on their properties. This would be called the CollisionsHandler.
* For all collections, I want a Renderer that can render everything with certain colors and characters.

Or maybe I want a physics collection, a collidable collection, and a rendering collection that all have their own object handlers. You can have the same object in multiple collections, so that seems alright.