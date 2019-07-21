from enum import Enum, Flag
from random import randint
import math

import tcod
import numpy

from terrain import TERRAINS, Terrain, TerrainFlags

class GameMap:
    def __init__(self, width, height, player):
        self.width = width
        self.height = height
        self.player = player
        self.terrain = numpy.zeros((self.width, self.height), dtype=Terrain, order='F')
        self.explored = numpy.zeros((self.width, self.height), dtype=bool, order='F')
        self.visible = numpy.zeros((self.width, self.height), dtype=bool, order='F')
        self.transparent = numpy.ones((self.width, self.height), dtype=bool, order='F')
        self.walkable = numpy.ones((self.width, self.height), dtype=bool, order='F')
        self.objects = []
    
    def load(self, map_data):
        self.terrain = map_data['tiles']
        self.objects = map_data['objects']
        self.objects.append(self.player)
        self.player.put(map_data['player'][0], map_data['player'][1])
        self.update_flags()

    def update_flags(self):
        for x in range(self.width):
            for y in range(self.height):
                flags = TERRAINS[self.terrain[x][y]]['flags']
                self.transparent[x][y] = not flags & TerrainFlags.BLOCKS_SIGHT
                self.walkable[x][y] = not flags & TerrainFlags.BLOCKS_MOVE
        
        for obj in self.objects:
            if obj.interactable:
                self.transparent[obj.x][obj.y] &= not obj.interactable.blocks_sight
                self.walkable[obj.x][obj.y] &= not obj.interactable.blocks_move

    def is_blocked(self, x, y):
        actions = []
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True, actions
        
        terrain = TERRAINS[self.terrain[x][y]]
        if terrain['flags'] & TerrainFlags.BLOCKS_MOVE:
            actions.extend([{'message': terrain['block_str'] }])
            return True, actions
        
        blocked = False
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                bumped, interactions = obj.bump()
                blocked = blocked or bumped
                actions.extend(interactions)
        return blocked, actions
    
    def move_entity(self, entity, dx, dy):
        nx = entity.x + dx
        ny = entity.y + dy
        blocked, actions = self.is_blocked(nx, ny)
        if not blocked:
            entity.put(nx, ny)
        return actions
    
    def move_entity_towards(self, entity, target):
        dx = target.x - entity.x
        dy = target.y - entity.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        return self.move_entity(entity,dx,dy)
    
    def get_objects_at(self, x, y):
        return [obj for obj in self.objects if obj.x == x and obj.y == y]

    def get_terrain_str(self, x, y):
        terrain = self.terrain[x][y]
        return TERRAINS[terrain]['look_str']
        
    def compute_fov(self):
        self.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=(self.player.x, self.player.y),
            radius=10,
            light_walls=True,
            algorithm=tcod.FOV_BASIC
        )
        self.explored |= self.visible

