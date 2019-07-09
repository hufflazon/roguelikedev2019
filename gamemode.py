import tcod
import tcod.event

from enum import Enum, auto

from terrain import TERRAINS

class GameState(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()

class GameMode(tcod.event.EventDispatch):
    def __init__(self):
        pass
    
    def ev_quit(self, event):
        raise SystemExit()
    
    def ev_keydown(self, event):
        # Handle Exit on ESC
        if event.sym == tcod.event.K_ESCAPE:
            raise SystemExit()

        # Alt+Enter to toggle fullscreen mode
        elif event.sym == tcod.event.K_RETURN and (event.mod & tcod.event.KMOD_ALT):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    def render(self, console):
        pass
    
    def update(self):
        pass

class Playing(GameMode):
    def __init__(self, map):
        self.map = map
        self.fov_recompute = True
        self.state = GameState.PLAYER_TURN
        
    def ev_keydown(self, event):
        if self.state == GameState.PLAYER_TURN:
            # Handle Player Movement
            if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w:
                self.player_move(0, -1)
            elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s:
                self.player_move(0, 1)
            elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_a:
                self.player_move(-1, 0)
            elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_d:
                self.player_move(1, 0)
            
            # Handle player interact
            elif event.sym == tcod.event.K_f:
                self.player_interact()

            # Handle player look
            elif event.sym == tcod.event.K_l:
                self.player_look()
        
            else:
                super().ev_keydown(event)
    
    def render(self, con):
        # Draw all the tiles in the game map
        for y in range(self.map.height):
                for x in range(self.map.width):
                        visible = self.map.visible[x,y]
                        terrain = TERRAINS[self.map.terrain[x][y]]
                        if visible:
                                con.fg[x,y,] = terrain['color']
                                con.ch[x,y,] = terrain['char']

                        elif self.map.explored[x][y]:
                                con.fg[x,y,] = terrain['dark']
                                con.ch[x,y,] = terrain['char']

        # Draw entities onto the map
        for obj in self.map.objects:
                if self.map.visible[obj.x,obj.y]:  
                        con.fg[obj.x,obj.y,] = obj.color
                        con.ch[obj.x,obj.y,] = obj.char
    
        con.fg[self.map.player.x,self.map.player.y,] = self.map.player.color
        con.ch[self.map.player.x,self.map.player.y,] = self.map.player.char
    
    def update(self):
        if self.fov_recompute:
            self.map.compute_fov()
            self.fov_recompute = False
        
        if self.state == GameState.ENEMY_TURN:
            for obj in self.map.objects:
                if obj.is_actor():
                    obj.act()
            self.state = GameState.PLAYER_TURN
    
    def player_move(self, dx, dy):
        self.map.move_entity(self.map.player, dx, dy)
        self.fov_recompute = True
        self.state = GameState.ENEMY_TURN
    
    def player_interact(self):
        interacted = False
        for obj in self.map.get_objects_at(self.map.player.x, self.map.player.y):
            obj.interact(self.map.player)
            interacted = True
        
        if not interacted:
            print('Nothing here to interact with.')
        else:
            self.map.update_flags()
            self.fov_recompute = True
            self.state = GameState.ENEMY_TURN

    def player_look(self):
        print(self.map.get_terrain_str(self.map.player.x, self.map.player.y))
        for obj in self.map.get_objects_at(self.map.player.x, self.map.player.y):
            print(obj.name)

