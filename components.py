from random import randint

class Interactable:
    def __init__(self, blocks_move=False, blocks_sight=False):
        self.parent = None
        self.blocks_move = blocks_move
        self.blocks_sight = blocks_sight
    
    def set_parent(self, parent):
        self.parent = parent

    def bump(self, entity):
        print(f'You see a {self.parent.name} before you.')
        return self.blocks_move

    def interact(self, entity):
        print(f'You attempt to interact with the {self.parent.name}.')
        

class Door(Interactable):
    def __init__(self, open=False):
        super().__init__(blocks_move = not open, blocks_sight = not open)
    
    def bump(self, entity):
        if self.blocks_move == True:
            self.open_door()
        return self.blocks_move

    def interact(self, entity):
        if self.blocks_move == False:
            self.close_door()
        else:
            self.open_door()

    def open_door(self):
        print('You open the door!')
        self.parent.char = ord('/')
        self.blocks_move = False
        self.blocks_sight = False
    
    def close_door(self):
        print('You close the door!')
        self.parent.char = ord('+')
        self.blocks_move = True
        self.blocks_sight = True

class NPC(Interactable):
    def __init__(self):
        super().__init__(blocks_move=True)
    
    def bump(self, entity):
        print(f'The {self.parent.name} growls at you!')
        return self.blocks_move

class Teleport(Interactable):
    def __init__(self, target_x, target_y):
        super().__init__()
        self.target_x = target_x
        self.target_y = target_y
    
    def interact(self, entity):
        print('You are teleported!')
        entity.put(self.target_x, self.target_y)

class RandomTeleport(Interactable):
    def __init__(self, max_x, max_y):
        super().__init__()
        self.max_x = max_x
        self.max_y = max_y

    def interact(self, entity):
        print(f'You are teleported!')
        x = randint(0,self.max_x)
        y = randint(0,self.max_y)
        entity.put(x,y)
