import tcod

from map import TERRAINS

def render_all(con, game_map):
    draw_map(con, game_map)
    
def draw_map(con, game_map):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            terrain = TERRAINS[game_map.tiles[x][y].terrain]
            con.fg[x,y,] = terrain['color']
            con.ch[x,y,] = terrain['char']

    # Draw entities onto the map
    for obj in game_map.objects:
            con.fg[obj.x,obj.y,] = obj.color
            con.ch[obj.x,obj.y,] = obj.char
    
    con.fg[game_map.player.x,game_map.player.y,] = game_map.player.color
    con.ch[game_map.player.x,game_map.player.y,] = game_map.player.char


