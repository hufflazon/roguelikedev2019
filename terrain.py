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
        'look_str': 'The ground here is hard packed dirt.'
    },
    Terrain.GRASS: { 
        'char': 250, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.NONE,
        'look_str': 'The ground here is covered in lush grass.'
    },
    Terrain.SAND: {
        'char': 250,
        'color': tcod.dark_yellow,
        'flags': TerrainFlags.NONE,
        'look_str': 'The ground here is fine sand.'
    },
    Terrain.STONE: { 
        'char': 250,
        'color': tcod.gray,
        'flags': TerrainFlags.NONE,
        'look_str': 'The ground here is solid stone.'
    },
    # Liquid Types
    Terrain.DEEP_WATER: { 
        'char': 247, 
        'color': tcod.blue,
        'flags': TerrainFlags.BLOCKS_MOVE,
        'block_str': 'The water is too deep!',
        'look_str': 'This water is well over your head.'
    },
    Terrain.LAVA: { 
        'char': 247, 
        'color': tcod.orange,
        'flags': TerrainFlags.BLOCKS_MOVE,
        'block_str': 'You cannot enter lava!',
        'look_str': 'Molten lava bubbles up from somewhere below.'
    },
    Terrain.MUD: {
        'char': 247,
        'color': tcod.sepia,
        'flags': TerrainFlags.NONE,
        'look_str': 'The ground here is muddy.'
    },
    Terrain.WATER: { 
        'char': 247,
        'color': tcod.cyan,
        'flags': TerrainFlags.NONE,
        'look_str': 'This water is shallow enough to wade in.'
    },
    # Above Ground
    Terrain.BUSH: { 
        'char': 15, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.NONE,
        'look_str': 'A shrubbery large enough to conceal a person.'
    },
    Terrain.TREE: { 
        'char': 6, 
        'color': tcod.dark_green,
        'flags': TerrainFlags.BLOCKS_MOVE,
        'block_str': 'A large tree blocks your way.',
        'look_str': 'A towering tree soars far overhead.'   
    },
    # Walls
    Terrain.STONE_WALL: { 
        'char': ord('#'), 
        'color': tcod.lighter_gray,
        'flags': TerrainFlags.BLOCKS_MOVE | TerrainFlags.BLOCKS_SIGHT,
        'block_str': 'A stone wall blocks your way.',
        'look_str': 'This wall looks solid. You\'ll have to go around.'
    }
}