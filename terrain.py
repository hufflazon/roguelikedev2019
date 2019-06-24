from enum import Enum, Flag, auto

import tcod

class TerrainFlags(Flag):
    NONE = 0
    BLOCKS_MOVE = auto()
    BLOCKS_SIGHT = auto()

class Terrain(Enum):
    DIRT = auto()
    STONE = auto()
    GRASS = auto()
    STONE_WALL = auto()
    WATER = auto()
    DEEP_WATER = auto()
    LAVA = auto()
    BUSH = auto()
    TREE = auto()

TERRAINS = {
    Terrain.DIRT: { 
        'char': 250, 
        'color': tcod.sepia,
        'flags': TerrainFlags.NONE,
    },
    Terrain.STONE: { 
        'char': 250,
        'color': tcod.gray,
        'flags': TerrainFlags.NONE,
    },
    Terrain.GRASS: { 
        'char': 250, 
        'color': tcod.green,
        'flags': TerrainFlags.NONE
    },
    Terrain.STONE_WALL: { 
        'char': ord('#'), 
        'color': tcod.lighter_gray,
        'flags': TerrainFlags.BLOCKS_MOVE | TerrainFlags.BLOCKS_SIGHT
    },
    Terrain.WATER: { 
        'char': ord('~'),
        'color': tcod.cyan,
        'flags': TerrainFlags.NONE
    },
    Terrain.DEEP_WATER: { 
        'char': ord('~'), 
        'color': tcod.blue,
        'flags': TerrainFlags.BLOCKS_MOVE 
    },
    Terrain.LAVA: { 
        'char': ord('~'), 
        'color': tcod.orange,
        'flags': TerrainFlags.BLOCKS_MOVE
    },
    Terrain.BUSH: { 
        'char': ord('*'), 
        'color': tcod.green,
        'flags': TerrainFlags.NONE
    },
    Terrain.TREE: { 
        'char': 5, 
        'color': tcod.green,
        'flags': TerrainFlags.BLOCKS_MOVE    
    }
}