from random import randint

import numpy
import tcod

from map import GameMap
from entity import Entity
from components import Door, NPC, Teleport, RandomTeleport, Actor
from terrain import TERRAINS, Terrain, TerrainFlags

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)
    
    def intersect(self, other):
        #returns true if this rectangle intersects another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and 
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(tiles, room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            tiles[x][y] = Terrain.STONE
    
def create_h_tunnel(tiles, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles[x][y] = Terrain.STONE

def create_v_tunnel(tiles, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
           tiles[x][y] = Terrain.STONE

def create_mobs(room, entities, max_mobs_per_room):
    number_of_mobs = randint(0, max_mobs_per_room)

    for i in range(number_of_mobs):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            if randint(0, 100) < 80:
                mob = Entity('harpy', 'h', tcod.desaturated_amber)
            else:
                mob = Entity('minotaur', 'M', tcod.dark_chartreuse)
            
            mob.make_interactable(NPC())
            mob.make_actor(Actor())
            mob.put(x, y)
            entities.append(mob)

def make_sample_map(width, height):
    tiles = numpy.zeros((width, height), dtype=Terrain, order='F')

    # Vertial bands of different ground terrains
    for x in range(width):
        for y in range(height):
            if x < 20:
                tiles[x][y] = Terrain.STONE
            elif x < 40:
                t = randint(1,50)
                if t == 1:
                    tiles[x][y] = Terrain.BUSH
                elif t == 50:
                    tiles[x][y] = Terrain.MUD
                else:
                    tiles[x][y] = Terrain.DIRT
            elif x < 60:
                t = randint(1,50)
                if t == 50:
                    tiles[x][y] = Terrain.TREE
                elif t == 1:
                    tiles[x][y] = Terrain.BUSH
                else:
                    tiles[x][y] = Terrain.GRASS
            elif x < 70:
                tiles[x][y] = Terrain.SAND
            elif x < 80:
                tiles[x][y] = Terrain.DEEP_WATER

    # Make a little test room
    for x in range(28,33):
        tiles[x][15] = Terrain.STONE_WALL
        tiles[x][20] = Terrain.STONE_WALL
    for y in range(16,20):
        tiles[28][y] = Terrain.STONE_WALL
        tiles[32][y] = Terrain.STONE_WALL
    
    # With a door
        tiles[30][20] = Terrain.DIRT

    # Make a pond
    for x in range(45,50):
        for y in range(19,26):
            tiles[x][y] = Terrain.WATER

    # Make a lava pond
    for x in range(10,15):
        for y in range(30,35):
            tiles[x][y] = Terrain.LAVA
    
    objects = []
    kobold = Entity('kobold', 'k', tcod.yellow)
    kobold.make_interactable(NPC())
    kobold.make_actor(Actor())
    kobold.put(35,25)
    objects.append(kobold)

    door = Entity('door', '+', tcod.sepia)
    door.make_interactable(Door(open=False))
    door.put(30, 20)
    objects.append(door)

    shrine = Entity('shrine', 'X', tcod.yellow)
    shrine.make_interactable(RandomTeleport(width-1,height-1))
    shrine.put(10, 40)
    objects.append(shrine)

    portal1 = Entity('strange glowing portal', 'O', tcod.cyan)
    portal1.make_interactable(Teleport(40,40))
    portal1.put(10, 10)
    objects.append(portal1)

    portal2 = Entity('strange glowing portal', 'O', tcod.cyan)
    portal2.make_interactable(Teleport(10,10))
    portal2.put(40,40)
    objects.append(portal2)

    return {
        'tiles': tiles,
        'objects': objects,
        'player': (40,25)
    }
    
def make_tutorial_map(width, height, max_rooms, room_min_size, room_max_size):
    tiles = [[Terrain.STONE_WALL for y in range(height)] for x in range(width)]
    rooms = []
    entities = []
    num_rooms = 0

    for r in range(max_rooms):
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        x = randint(0, width - w - 1)
        y = randint(0, height - h - 1)

        new_room = Rect(x, y, w, h)

        #check for intersections
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        
        else:
            # no intersections, room is valid
            create_room(tiles, new_room)

            if num_rooms > 0:
                # create a tunnel connecting previous room
                (new_x, new_y) = new_room.center()
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                if randint(0, 1) == 1:
                    # over to new x then up/down to new y
                    create_h_tunnel(tiles, prev_x, new_x, prev_y)
                    create_v_tunnel(tiles, prev_y, new_y, new_x)
                else:
                    # up/down to new y and then over to new x
                    create_v_tunnel(tiles, prev_y, new_y, prev_x)
                    create_h_tunnel(tiles, prev_x, new_x, new_y)
            
            create_mobs(new_room, entities, 3)
            rooms.append(new_room)
            num_rooms += 1
    
    return {
        'tiles': tiles,
        'objects': entities,
        'player': (rooms[0].center())
    }