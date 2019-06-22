import tcod

def render_all(con, entities, game_map, colors):
    draw_map(con, game_map, colors)
    
    for entity in entities:
        draw_entity(con, entity)

def draw_entity(con, entity):
    con.default_fg = entity.color
    con.put_char(entity.x, entity.y, ord(entity.char), tcod.BKGND_NONE)

def draw_map(con, game_map, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                con.fg[x,y,]= colors.get('dark_wall')
                con.ch[x,y] = ord('#')
            else:
                con.fg[x,y,] = colors.get('dark_ground')
                con.ch[x,y] = ord('.')
