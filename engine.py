import tcod
import tcod.event

from input_handler import InputHandler
from entity import Entity
from render_functions import render_all
from map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

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
        game_map.make_sample_map()
        handler = InputHandler(game_map)

        while True:
            con.clear(fg=(255,255,255))
            render_all(con, game_map)
            con.blit(root_console, 0, 0, 0, 0, screen_width, screen_height)
            tcod.console_flush()
            for event in tcod.event.wait():
                handler.dispatch(event)

if __name__ == '__main__':
    main()