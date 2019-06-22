class Tile:
    """
    A tile on the map.
    """

    def __init__(self, block_move=False, block_sight=None):
        self.block_move = block_move

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = block_move

        self.block_sight = block_sight

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_move:
            return True
        
        return False
    
    def move_entity(self, entity, dx, dy):
        if not self.is_blocked(entity.x + dx, entity.y + dy):
            entity.move(dx, dy)

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].block_move = True
        tiles[30][22].block_sight = True
        tiles[31][22].block_move = True
        tiles[31][22].block_sight = True
        tiles[32][22].block_move = True
        tiles[32][22].block_sight = True

        return tiles
