from enum import Enum, Flag, auto

import tcod

class TerrainFlags(Flag):
    NONE = 0
    BLOCKS_MOVE = auto()
    BLOCKS_SIGHT = auto()

class Terrain(Enum):
    DIRT = auto()
    GRASS = auto()
    SAND = auto()
    STONE = auto()
    DEEP_WATER = auto()
    LAVA = auto()
    MUD = auto()
    WATER = auto()
    BUSH = auto()
    TREE = auto()
    STONE_WALL = auto()

TERRAINS = {
    # Ground Types
    Terrain.DIRT: { 
        'char': 250, 
        'color': tcod.sepia,
        'flags': TerrainFlags.NONE,
    },
    Terrain.GRASS: { 
        'char': 250, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.NONE
    },
    Terrain.SAND: {
        'char': 250,
        'color': tcod.dark_yellow,
        'flags': TerrainFlags.NONE
    },
    Terrain.STONE: { 
        'char': 250,
        'color': tcod.gray,
        'flags': TerrainFlags.NONE
    },
    # Liquid Types
    Terrain.DEEP_WATER: { 
        'char': 247, 
        'color': tcod.blue,
        'flags': TerrainFlags.BLOCKS_MOVE 
    },
    Terrain.LAVA: { 
        'char': 247, 
        'color': tcod.orange,
        'flags': TerrainFlags.BLOCKS_MOVE
    },
    Terrain.MUD: {
        'char': 247,
        'color': tcod.sepia,
        'flags': TerrainFlags.NONE
    },
    Terrain.WATER: { 
        'char': 247,
        'color': tcod.cyan,
        'flags': TerrainFlags.NONE
    },
    # Above Ground
    Terrain.BUSH: { 
        'char': 15, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.NONE
    },
    Terrain.TREE: { 
        'char': 6, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.BLOCKS_MOVE    
    },
    # Walls
    Terrain.STONE_WALL: { 
        'char': ord('#'), 
        'color': tcod.lighter_gray,
        'flags': TerrainFlags.BLOCKS_MOVE | TerrainFlags.BLOCKS_SIGHT
    }
}