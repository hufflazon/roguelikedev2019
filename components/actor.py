from .component import Component

class Actor(Component):
    def __init__(self, entity):
        super().__init__(entity)
    
    def act(self, map, target):
        return [{
            'message': f'The {self.entity.name} ponders the meaning of its existence.'
        }]

class HuntingMobile(Actor):
    def act(self, map, path, target):
        actions = []

        if map.visible[self.entity.x, self.entity.y]:
            if self.entity.distance_to(target) >= 2:
                moves = path.get_path(self.entity.x, self.entity.y, target.x, target.y)
                length = len(moves)
                if length > 0 and length < 25:
                    self.entity.x = moves[0][0]
                    self.entity.y = moves[0][1]
                else:
                    map.move_entity_towards(self.entity, target)
            elif target.fighter.hp > 0:
                actions.extend(self.entity.fighter.attack(target))
        
        return actions
