import math
from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class Entity:
    """
    An entity on the map (player, enemy, item, etc)
    """

    def __init__(self, name, char, color):
        self.x = 0
        self.y = 0
        self.name = name
        self.char = ord(char)
        self.color = color
        self.interactable = None
        self.actor = None
        self.fighter = None
        self.render_order = RenderOrder.ITEM

    def put(self, x, y):
        self.x = x
        self.y = y    

    def is_interactable(self):
        return self.interactable is not None
    
    def bump(self):           
        if self.is_interactable(): 
            return self.interactable.bump()
        
        return False, []

    def interact(self):
        if self.is_interactable():
            return self.interactable.interact()
        
        return []
    
    def is_actor(self):
        return self.actor is not None
    
    def act(self, map, path, target):
        if self.is_actor():
            return self.actor.act(map, path, target)

    def is_fighter(self):
        return self.fighter is not None

    def distance_to(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        return math.sqrt(dx ** 2 + dy ** 2)