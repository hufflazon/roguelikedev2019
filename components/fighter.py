from .component import Component

class Fighter(Component):
    def __init__(self, entity, hp, defense, power):
        super().__init__(entity)
        self.hp = hp
        self.max_hp = hp
        self.defense = defense
        self.power = power
    
    def take_damage(self, amount):
        actions = []

        self.hp -= amount

        if self.hp <= 0:
            actions.append({'dead': self.entity })
        
        return actions
    
    def attack(self, target):
        actions = []

        print(self.entity.name+" "+str(self.power))
        damage = self.power - target.fighter.defense

        if damage > 0:
            actions.append({'message': f'{self.entity.name.capitalize()} attacks {target.name} for {damage}'})
            actions.extend(target.fighter.take_damage(damage))
        else:
            actions.append({'message': f'{self.entity.name.capitalize()} attacks {target.name} but does no damage.'})
        
        return actions
