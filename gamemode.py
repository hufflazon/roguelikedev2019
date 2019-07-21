import tcod
import tcod.event

from enum import Enum, auto

from terrain import TERRAINS
from entity import RenderOrder
from components.interactable import Corpse

class GameState(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()    

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
            if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_k:
                self.player_move(0, -1)
            elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_j:
                self.player_move(0, 1)
            elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_h:
                self.player_move(-1, 0)
            elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_l:
                self.player_move(1, 0)
            elif event.sym == tcod.event.K_y:
                self.player_move(-1, -1)
            elif event.sym == tcod.event.K_u:
                self.player_move(1, -1)
            elif event.sym == tcod.event.K_b:
                self.player_move(-1, 1)
            elif event.sym == tcod.event.K_n:
                self.player_move(1, 1)
            
            # Handle player interact
            elif event.sym == tcod.event.K_f:
                self.player_interact()

            # Handle player look
            elif event.sym == tcod.event.K_v:
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
        entities_in_render_order = sorted(self.map.objects, key=lambda x: x.render_order.value)
        for obj in entities_in_render_order:
                if self.map.visible[obj.x,obj.y]:  
                        con.fg[obj.x,obj.y,] = obj.color
                        con.ch[obj.x,obj.y,] = obj.char
    
    def update(self):
        if self.fov_recompute:
            self.map.compute_fov()
            self.fov_recompute = False
        
        if self.state == GameState.ENEMY_TURN:
            astar = tcod.path.AStar(self.map.walkable)
            for obj in self.map.objects:
                if self.state == GameState.PLAYER_DEAD:
                    break

                if obj.is_actor():
                    actions = obj.act(self.map, astar, self.map.player)
                    self.actor_actions(obj, actions)
            
            else:
                self.state = GameState.PLAYER_TURN
    
    def actor_actions(self, entity, actions):
        for action in actions:
            for key,value in action.items():
                if key == 'message':
                    print(value)
                elif key == 'move_to':
                    entity.move(value[0], value[1])
                elif key == 'dead':
                    if value.name=='player':
                        self.player_kill(value)
                    else:
                        self.monster_kill(value)
                else:
                    print(f'WARNING: Unimplemented actor action {key}: {value}')
                
    def player_actions(self, actions):
        for action in actions:
            for key,value in action.items():
                if key == 'message':
                    print(value)
                elif key == 'move_to':
                    self.map.player.put(value[0], value[1])
                    self.fov_recompute = True
                elif key == 'fight':
                    self.player_actions(self.map.player.fighter.attack(value))
                elif key == 'update_flags':
                    self.map.update_flags()
                elif key == 'recompute_fov':
                    self.fov_recompute = True
                elif key == 'dead':
                    if value.name=='player':
                        self.player_kill(value)
                    else:
                        self.monster_kill(value)
                else:
                    print(f'WARNING: Unimplemented player action {key}: {value}')

    def player_move(self, dx, dy):
        actions = self.map.move_entity(self.map.player, dx, dy)
        self.player_actions(actions)
        self.fov_recompute = True
        self.state = GameState.ENEMY_TURN
    
    def player_interact(self):
        actions = []

        for obj in self.map.get_objects_at(self.map.player.x, self.map.player.y):
            if obj.name == 'player':
                continue

            actions.extend(obj.interact())
        
        if not actions:
            print('Nothing here to interact with.')
        else:
            self.player_actions(actions)
            self.state = GameState.ENEMY_TURN

    def player_look(self):
        print(self.map.get_terrain_str(self.map.player.x, self.map.player.y))
        for obj in self.map.get_objects_at(self.map.player.x, self.map.player.y):
            print(obj.name)

    def player_kill(self, player):
        player.char = ord('%')
        player.color = tcod.dark_red
        print("You died!")
        self.state = GameState.PLAYER_DEAD
    
    def monster_kill(self, entity):
        print(f'{entity.name} is dead!')
        entity.char = ord('%')
        entity.color = tcod.dark_red
        entity.interactable = Corpse(entity)
        entity.fighter = None
        entity.actor = None
        entity.render_order = RenderOrder.CORPSE
        entity.name = 'remains of ' + entity.name

