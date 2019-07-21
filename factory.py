from components.actor import HuntingMobile
from components.interactable import NPC
from components.fighter import Fighter

from entity import Entity, RenderOrder

def create_monster(name, symbol, color, hp=10, power=1, defense=1):
    mob = Entity(name,symbol,color)
    mob.actor = HuntingMobile(mob)
    mob.interactable = NPC(mob)
    mob.fighter = Fighter(mob, hp, defense, power)
    mob.render_order = RenderOrder.ACTOR
    return mob


        
