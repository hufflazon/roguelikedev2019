from enum import Enum, Flag
from random import randint

import tcod
import numpy

from entity import Entity
from components import Door, NPC, Teleport, RandomTeleport
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
    
    def update_flags(self):
        for x in range(self.width):
            for y in range(self.height):
                self.transparent[x][y] = not TERRAINS[self.terrain[x][y]]['flags'] & TerrainFlags.BLOCKS_SIGHT
        
        for obj in self.objects:
            if obj.interactable:
                self.transparent[obj.x][obj.y] = not obj.interactable.blocks_sight

    def place_entity(self, entity, x, y):
        self.objects.append(entity)
        entity.put(x,y)
        
    def remove_entity(self, entity):
        self.objects.remove(entity)

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

    def player_interact(self):
        x = self.player.x
        y = self.player.y
        interacted = False
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                obj.interact(self.player)
                interacted = True
        
        if not interacted:
            print('Nothing here to interact with.')

    def player_look(self):
        x = self.player.x
        y = self.player.y
        terrain = self.terrain[x][y]
        print(TERRAINS[terrain]['look_str'])
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                print(obj.name)

    def player_move(self, dx, dy):
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not self.is_blocked(self.player, nx, ny):
            self.player.put(nx, ny)
        
    def compute_fov(self):
        self.visible = tcod.map.compute_fov(
            transparency=self.transparent,
            pov=(self.player.x, self.player.y),
            radius=10,
            light_walls=True,
            algorithm=0
        )
        self.explored |= self.visible
        
    def make_sample_map(self):
        # Vertial bands of different ground terrains
        for x in range(self.width):
            for y in range(self.height):
                if x < 20:
                    self.terrain[x][y] = Terrain.STONE
                elif x < 40:
                    t = randint(1,50)
                    if t == 1:
                        self.terrain[x][y] = Terrain.BUSH
                    elif t == 50:
                        self.terrain[x][y] = Terrain.MUD
                    else:
                        self.terrain[x][y] = Terrain.DIRT
                elif x < 60:
                    t = randint(1,50)
                    if t == 50:
                        self.terrain[x][y] = Terrain.TREE
                    elif t == 1:
                        self.terrain[x][y] = Terrain.BUSH
                    else:
                        self.terrain[x][y] = Terrain.GRASS
                elif x < 70:
                    self.terrain[x][y] = Terrain.SAND
                elif x < 80:
                    self.terrain[x][y] = Terrain.DEEP_WATER

        # Make a little test room
        for x in range(28,33):
            self.terrain[x][15] = Terrain.STONE_WALL
            self.terrain[x][20] = Terrain.STONE_WALL
        for y in range(16,20):
            self.terrain[28][y] = Terrain.STONE_WALL
            self.terrain[32][y] = Terrain.STONE_WALL
        
        # With a door
            self.terrain[30][20] = Terrain.DIRT

        # Make a pond
        for x in range(45,50):
            for y in range(19,26):
                self.terrain[x][y] = Terrain.WATER

        # Make a lava pond
        for x in range(10,15):
            for y in range(30,35):
                self.terrain[x][y] = Terrain.LAVA
        
        kobold = Entity('kobold', 'k', tcod.yellow)
        kobold.make_interactable(NPC())
        self.place_entity(kobold,35,25)

        door = Entity('door', '+', tcod.sepia)
        door.make_interactable(Door(open=False))
        self.place_entity(door, 30, 20)

        shrine = Entity('shrine', 'X', tcod.yellow)
        shrine.make_interactable(RandomTeleport(self.width-1,self.height-1))
        self.place_entity(shrine, 10, 40)

        portal1 = Entity('strange glowing portal', 'O', tcod.cyan)
        portal1.make_interactable(Teleport(40,40))
        self.place_entity(portal1, 10, 10)

        portal2 = Entity('strange glowing portal', 'O', tcod.cyan)
        portal2.make_interactable(Teleport(10,10))
        self.place_entity(portal2, 40,40)

        self.player.put(40,25)
        self.update_flags()
    
    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.terrain[x][y] = Terrain.STONE
    
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.terrain[x][y] = Terrain.STONE

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.terrain[x][y] = Terrain.STONE

    def make_tutorial_map(self, max_rooms, room_min_size, room_max_size):
        self.terrain = [[Terrain.STONE_WALL for y in range(self.height)] for x in range(self.width)]
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            #check for intersections
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            
            else:
                # no intersections, room is valid
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    self.place_entity(self.player, new_x, new_y)
                
                else:
                    # create a tunnel connecting previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        # over to new x then up/down to new y
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                        pass
                    else:
                        # up/down to new y and then over to new x
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        pass
                    
                rooms.append(new_room)
                num_rooms += 1
    
        self.update_flags()

