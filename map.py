from enum import Enum, Flag
from random import randint

import tcod
import numpy

from entity import Entity
from components import Door, NPC, Teleport, RandomTeleport, Actor
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
        self.objects = []
    
    def load(self, map_data):
        self.terrain = map_data['tiles']
        self.objects = map_data['objects']
        self.player.put(map_data['player'][0], map_data['player'][1])
        self.update_flags()

    def update_flags(self):
        for x in range(self.width):
            for y in range(self.height):
                self.transparent[x][y] = not TERRAINS[self.terrain[x][y]]['flags'] & TerrainFlags.BLOCKS_SIGHT
        
        for obj in self.objects:
            if obj.interactable:
                self.transparent[obj.x][obj.y] = not obj.interactable.blocks_sight

    def is_blocked(self, entity, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        
        terrain = TERRAINS[self.terrain[x][y]]
        if terrain['flags'] & TerrainFlags.BLOCKS_MOVE:
            if entity.name == 'player':
                print(terrain['block_str'])
            return True
        
        blocked = False
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                blocked = blocked or obj.bump(entity)
        return blocked
    
    def move_entity(self, entity, dx, dy):
        nx = entity.x + dx
        ny = entity.y + dy
        if not self.is_blocked(entity, nx, ny):
            entity.put(nx, ny)
    
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
            algorithm=0
        )
        self.explored |= self.visible

