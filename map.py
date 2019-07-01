from enum import Enum, Flag

import tcod
import random

from entity import Entity
from components import Door, NPC, Teleport, RandomTeleport
from terrain import TERRAINS, Terrain, TerrainFlags

class Tile:
    """
    A tile on the map.
    """

    def __init__(self, terrain=Terrain.DIRT):
        self.terrain = terrain
        self.objects = []

class GameMap:
    def __init__(self, width, height, player):
        self.width = width
        self.height = height
        self.objects = []
        self.tiles = self.initialize_tiles()
        self.player = player
        self.player.put(40,25)
        
        kobold = Entity('kobold', 'k', tcod.yellow)
        kobold.make_interactable(NPC())
        self.place_entity(kobold,35,25)

        door = Entity('door', '+', tcod.sepia)
        door.make_interactable(Door(open=False))
        self.place_entity(door, 30, 20)

        shrine = Entity('shrine', 'X', tcod.yellow)
        shrine.make_interactable(RandomTeleport(width-1,height-1))
        self.place_entity(shrine, 10, 40)

        portal1 = Entity('strange glowing portal', 'O', tcod.cyan)
        portal1.make_interactable(Teleport(40,40))
        self.place_entity(portal1, 10, 10)

        portal2 = Entity('strange glowing portal', 'O', tcod.cyan)
        portal2.make_interactable(Teleport(10,10))
        self.place_entity(portal2, 40,40)

    def place_entity(self, entity, x, y):
        self.tiles[x][y].objects.append(entity)
        self.objects.append(entity)
        entity.put(x,y)
        
    def remove_entity(self, entity):
        self.tiles[entity.x][entity.y].objects.remove(entity)
        self.objects.remove(entity)

    def is_blocked(self, entity, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        
        terrain = TERRAINS[self.tiles[x][y].terrain]
        if terrain['flags'] and TerrainFlags.BLOCKS_MOVE:
            if entity.name == 'player':
                print(terrain['block_str'])
            return True
        
        blocked = False
        for obj in self.tiles[x][y].objects:
            blocked = blocked or obj.bump(entity)
        
        return blocked
    
    def move_entity(self, entity, dx, dy):
        nx = entity.x + dx
        ny = entity.y + dy
        if not self.is_blocked(entity, nx, ny):
            self.tiles[entity.x][entity.y].objects.remove(entity)
            entity.put(nx, ny)
            self.tiles[nx][ny].objects.append(entity)

    def player_interact(self):
        x = self.player.x
        y = self.player.y
        for obj in self.tiles[x][y].objects:
            obj.interact(self.player)
            return True
        print('Nothing here to interact with.')
    
    def player_look(self):
        x = self.player.x
        y = self.player.y
        terrain = self.tiles[x][y].terrain
        print(TERRAINS[terrain]['look_str'])
        for obj in self.tiles[x][y].objects:
            print(obj.name)
    
    def player_move(self, dx, dy):
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not self.is_blocked(self.player, nx, ny):
            self.player.put(nx, ny)
    
    def initialize_tiles(self):
        return [[Tile() for y in range(self.height)] for x in range(self.width)]

    def make_sample_map(self):
        # Vertial bands of different ground terrains
        for x in range(self.width):
            for y in range(self.height):
                if x < 20:
                    self.tiles[x][y].terrain = Terrain.STONE
                elif x < 40:
                    t = random.randint(1,50)
                    if t == 1:
                        self.tiles[x][y].terrain = Terrain.BUSH
                    elif t == 50:
                        self.tiles[x][y].terrain = Terrain.MUD
                    else:
                        self.tiles[x][y].terrain = Terrain.DIRT
                elif x < 60:
                    t = random.randint(1,50)
                    if t == 50:
                        self.tiles[x][y].terrain = Terrain.TREE
                    elif t == 1:
                        self.tiles[x][y].terrain = Terrain.BUSH
                    else:
                        self.tiles[x][y].terrain = Terrain.GRASS
                elif x < 70:
                    self.tiles[x][y].terrain = Terrain.SAND
                elif x < 80:
                    self.tiles[x][y].terrain = Terrain.DEEP_WATER

        # Make a little test room
        for x in range(28,33):
            self.tiles[x][15].terrain = Terrain.STONE_WALL
            self.tiles[x][20].terrain = Terrain.STONE_WALL
        for y in range(16,20):
            self.tiles[28][y].terrain = Terrain.STONE_WALL
            self.tiles[32][y].terrain = Terrain.STONE_WALL
        
        # With a door
            self.tiles[30][20].terrain = Terrain.DIRT

        # Make a pond
        for x in range(45,50):
            for y in range(19,26):
                self.tiles[x][y].terrain = Terrain.WATER

        # Make a lava pond
        for x in range(10,15):
            for y in range(30,35):
                self.tiles[x][y].terrain = Terrain.LAVA