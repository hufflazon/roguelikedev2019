import tcod
import tcod.event

from gamemode import Playing
from entity import Entity
from map import GameMap
from mapgen import make_sample_map, make_tutorial_map

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = Entity('player', '@', tcod.white)

    tcod.console_set_custom_font(
        'terminal12x12_gs_ro.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
    )
    
    with tcod.console_init_root(
        screen_width,
        screen_height,
        'Roguelikedev2019', 
        order='F', 
        renderer=tcod.RENDERER_SDL2,
        vsync=True
    ) as root_console:

        con = tcod.console.Console(screen_width, screen_height, order='F')
        game_map = GameMap(map_width, map_height, player)
        #game_map.load(make_sample_map(map_width, map_height))
        game_map.load(make_tutorial_map(map_width, map_height, max_rooms, room_min_size, room_max_size))

        handler = Playing(game_map)

        while True:
            con.clear(fg=(255,255,255))
            handler.update()
            handler.render(con)
            con.blit(root_console, 0, 0, 0, 0, screen_width, screen_height)
            tcod.console_flush()
            for event in tcod.event.wait():
                handler.dispatch(event)

if __name__ == '__main__':
    main()