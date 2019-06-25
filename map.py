from enum import Enum, Flag

import tcod
import random

from terrain import TERRAINS, Terrain, TerrainFlags

class Tile:
    """
    A tile on the map.
    """

    def __init__(self, terrain=Terrain.DIRT):
        self.terrain = terrain

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def is_blocked(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        
        if TERRAINS[self.tiles[x][y].terrain]['flags'] & TerrainFlags.BLOCKS_MOVE:
            return True
        
        
        return False
    
    def move_entity(self, entity, dx, dy):
        if not self.is_blocked(entity.x + dx, entity.y + dy):
            entity.move(dx, dy)

    def initialize_tiles(self):
        """
            Test terrain features. 
        """
        tiles = [[Tile() for y in range(self.height)] for x in range(self.width)]

        # Vertial bands of different ground terrains
        for x in range(self.width):
            for y in range(self.height):
                if x < 20:
                    tiles[x][y].terrain = Terrain.STONE
                elif x < 40:
                    t = random.randint(1,50)
                    if t == 1:
                        tiles[x][y].terrain = Terrain.BUSH
                    elif t == 50:
                        tiles[x][y].terrain = Terrain.MUD
                    else:
                        tiles[x][y].terrain = Terrain.DIRT
                elif x < 60:
                    t = random.randint(1,50)
                    if t == 50:
                        tiles[x][y].terrain = Terrain.TREE
                    elif t == 1:
                        tiles[x][y].terrain = Terrain.BUSH
                    else:
                        tiles[x][y].terrain = Terrain.GRASS
                elif x < 70:
                    tiles[x][y].terrain = Terrain.SAND
                elif x < 80:
                    tiles[x][y].terrain = Terrain.DEEP_WATER

        # Make a little test room
        for x in range(28,33):
            tiles[x][15].terrain = Terrain.STONE_WALL
            tiles[x][20].terrain = Terrain.STONE_WALL
        for y in range(16,20):
            tiles[28][y].terrain = Terrain.STONE_WALL
            tiles[32][y].terrain = Terrain.STONE_WALL
        
        # With a entrance
            tiles[30][20].terrain = Terrain.DIRT

        # Make a pond
        for x in range(45,50):
            for y in range(19,26):
                tiles[x][y].terrain = Terrain.WATER

        # Make a lava pond
        for x in range(10,15):
            for y in range(30,35):
                tiles[x][y].terrain = Terrain.LAVA

        return tiles
