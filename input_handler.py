import tcod
import tcod.event

class InputHandler(tcod.event.EventDispatch):
    def __init__(self, map, player):
        self.player = player
        self.map = map

    def ev_quit(self, event):
        raise SystemExit()
    
    def ev_keydown(self, event):
        # Handle Player Movement
        if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w:
            self.map.move_entity(self.player, 0, -1)
        elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s:
            self.map.move_entity(self.player, 0, 1)
        elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_a:
            self.map.move_entity(self.player, -1, 0)
        elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_d:
            self.map.move_entity(self.player, 1, 0)
        
        # Handle Exit on ESC
        elif event.sym == tcod.event.K_ESCAPE:
            raise SystemExit()

        # Alt+Enter to toggle fullscreen mode
        elif event.sym == tcod.event.K_RETURN and (event.mod & tcod.event.KMOD_ALT):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())