import tcod
import tcod.event

from input_handler import InputHandler
from state import player

def main():
    screen_width = 80
    screen_height = 50

    player.x = int(screen_width / 2)
    player.y = int(screen_height / 2)

    tcod.console_set_custom_font(
        'arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
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
        handler = InputHandler()

        while True:
            con.clear()
            con.put_char(player.x, player.y, ord('@'))
            con.blit(root_console, 0, 0, 0, 0, screen_width, screen_height)
            tcod.console_flush()
            for event in tcod.event.wait():
                handler.dispatch(event)

if __name__ == '__main__':
    main()