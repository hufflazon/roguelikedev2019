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

        # Right half is grass. Left is dirt and stone. 
        for x in range(self.width):
            for y in range(self.height):
                if x > self.width / 2:
                    t = random.randint(0,10)
                    if t == 0:
                        tiles[x][y].terrain = Terrain.BUSH
                    elif t == 10:
                        tiles[x][y].terrain = Terrain.TREE
                    else:
                        tiles[x][y].terrain = Terrain.GRASS

                elif y > self.height / 2:
                    tiles[x][y].terrain = Terrain.STONE

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

        tiles[47][21].terrain = Terrain.DEEP_WATER
        tiles[47][22].terrain = Terrain.DEEP_WATER
        tiles[47][23].terrain = Terrain.DEEP_WATER

        # Make a lava pond
        for x in range(10,15):
            for y in range(30,35):
                tiles[x][y].terrain = Terrain.LAVA

        return tiles
