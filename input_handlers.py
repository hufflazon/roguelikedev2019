import tcod as libtcod

def handle_keys(key):
    # Player Movement

    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter to toggle fullscreen mode
        return {'fullscreen': True}
    
    elif key.vk == libtcod.KEY_ESCAPE:
        # Escape to exit game
        return {'exit': True}
    
    return {}