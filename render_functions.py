import tcod

from map import TERRAINS

def render_all(con, entities, game_map):
    draw_map(con, game_map)
    
    for entity in entities:
        draw_entity(con, entity)

def draw_entity(con, entity):
    con.default_fg = entity.color
    con.put_char(entity.x, entity.y, ord(entity.char), tcod.BKGND_NONE)

def draw_map(con, game_map):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            terrain = TERRAINS[game_map.tiles[x][y].terrain]
            con.fg[x,y,] = terrain['color']
            con.ch[x,y,] = terrain['char']