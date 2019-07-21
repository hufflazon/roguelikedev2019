from random import randint
from .component import Component

class Interactable(Component):
    def __init__(self, entity, blocks_move=False, blocks_sight=False):
        super().__init__(entity)
        self.blocks_move = blocks_move
        self.blocks_sight = blocks_sight
    
    def bump(self):
        return self.blocks_move, [{
            'message': f'You see a {self.entity.name} before you.'
        }]

    def interact(self):
        return [{
            'message': f'You attempt to interact with the {self.entity.name}.'
        }]
        
class Corpse(Interactable):
    def __init__(self, entity):
        super().__init__(entity)

    def interact(self):
        return [{
            'message': f'You kick the corpse!'
        }]

class Door(Interactable):
    def __init__(self, entity, open=False):
        super().__init__(entity, blocks_move = not open, blocks_sight = not open)
    
    def bump(self):
        actions = []
        if self.blocks_move == True:
            actions.extend(self.open_door())
        return self.blocks_move, actions

    def interact(self):
        if self.blocks_move == False:
            return self.close_door()
        else:
            return self.open_door()

    def open_door(self):
        actions = [{ 'message': 'You open the door!', 'update_flags': True, 'recompute_fov': True }]
        self.entity.char = ord('/')
        self.blocks_move = False
        self.blocks_sight = False
        return actions
    
    def close_door(self):
        actions = [{ 'message': 'You close the door!', 'update_flags': True, 'recompute_fov': True }]
        self.entity.char = ord('+')
        self.blocks_move = True
        self.blocks_sight = True
        return actions

class NPC(Interactable):
    def __init__(self, entity):
        super().__init__(entity, blocks_move=True)
    
    def bump(self):
        return self.blocks_move, [{
            'fight': self.entity
        }]

class Teleport(Interactable):
    def __init__(self, entity, target_x, target_y):
        super().__init__(entity)
        self.target_x = target_x
        self.target_y = target_y
    
    def interact(self):
        return [{
            'move_to': (self.target_x, self.target_y),
            'message': 'You are teleported!'
        }]
        
class RandomTeleport(Interactable):
    def __init__(self, entity, max_x, max_y):
        super().__init__(entity)
        self.max_x = max_x
        self.max_y = max_y

    def interact(self):
        x = randint(0,self.max_x)
        y = randint(0,self.max_y)
        return [{
            'move_to': (x, y),
            'message': 'You are teleported!'
        }]