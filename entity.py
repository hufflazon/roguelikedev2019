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

    def put(self, x, y):
        self.x = x
        self.y = y    

    def make_interactable(self, interactable):
        self.interactable = interactable
        interactable.set_parent(self)
    
    def is_interactable(self):
        return self.interactable is not None
    
    def bump(self, entity):           
        if self.is_interactable(): 
            return self.interactable.bump(entity)
        
        return False

    def interact(self, entity):
        if self.is_interactable():
            return self.interactable.interact(entity)
        
        return False
    
    def make_actor(self, actor):
        self.actor = actor
        actor.set_parent(self)
    
    def is_actor(self):
        return self.actor is not None
    
    def act(self):
        if self.is_actor():
            return self.actor.act()
