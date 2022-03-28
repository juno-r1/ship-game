import engine
import objects
import random
import keyboard

x_res = 40 # IMPORTANT: X GOES DOWN
y_res = 40 # IMPORTANT: Y GOES ACROSS
level_time = 60 # Time of each level in seconds

render = engine.Renderer(x_res, y_res) # Creates a renderer with a resolution of x_res * y_res

render.cutscene('You are the pilot of an experimental navy ship! Use WASD to move and Space to sink underwater, allowing you to pierce enemy hulls with your spike.\nPress Enter to continue...')

level1 = engine.Scene('level1', fps = 60) # Creates a scene running at ~x fps, or as fast as its legs can manage
player = objects.Player('sprites/player.txt', level1, x_res / 2, y_res / 2)
level1.active = True

while level1.active: # level1 loop

    for spawn in level1.spawns:
        if (level1.frame != 0) and ((level1.frame / level1.fps) % int(spawn[0]) == 0):
            x = eval('objects.{0}({1}, {2}, {3}, {4}, {5})'.format(spawn[1], spawn[2], spawn[3], '0', str(int(random.random() * render.y_res)), spawn[6]))

    for object in level1.objects:
        if object is player:
            level1.queue(player.player_input, render) # Checks for player input
            if not player.sunk:
                level1.queue(player.shoot) # Do not change these variables
                level1.queue(player.damage, render) # Checks if the player is damaged
            if player.health <= 0:
                render.cutscene('GAME OVER')
                input()
                quit()
        elif isinstance(object, objects.Enemy): # Never reference an enemy by name, otherwise it won't get garbage collected properly
            if isinstance(object, objects.Shooter):
                level1.queue(object.shoot)
            level1.queue(object.state) # Invokes the object's state machine
            level1.queue(object.damage, render) # Checks if the object is damaged

    if level1.frame / level1.fps == level_time:
        level1.active = False

    level1.loop(render) # Has to go last, otherwise instructions get missed out

level1.objects = []
render.cutscene('Level 1 complete! Press Enter to continue...')

level2 = engine.Scene('level2', fps = 60) # Creates a scene running at ~x fps, or as fast as its legs can manage
player = objects.Player('sprites/player.txt', level2, x_res / 2, y_res / 2)
level2.active = True

while level2.active: # level2 loop

    for spawn in level2.spawns:
        if (level2.frame != 0) and ((level2.frame / level2.fps) % int(spawn[0]) == 0):
            x = eval('objects.{0}({1}, {2}, {3}, {4}, {5})'.format(spawn[1], spawn[2], spawn[3], '0', str(int(random.random() * render.y_res)), spawn[6]))

    for object in level2.objects:
        if object is player:
            level2.queue(player.player_input, render) # Checks for player input
            if not player.sunk:
                level2.queue(player.shoot) # Do not change these variables
                level2.queue(player.damage, render) # Checks if the player is damaged
            if player.health <= 0:
                render.cutscene('GAME OVER')
                input()
                quit()
        elif isinstance(object, objects.Enemy): # Never reference an enemy by name, otherwise it won't get garbage collected properly
            if isinstance(object, objects.Shooter):
                level2.queue(object.shoot)
            level2.queue(object.state) # Invokes the object's state machine
            level2.queue(object.damage, render) # Checks if the object is damaged

    if level2.frame / level2.fps == level_time:
        level2.active = False

    level2.loop(render) # Has to go last, otherwise instructions get missed out

level2.objects = []
render.cutscene('WARNING: HMS Ornstein and HMS Smough inbound! Their reinforced hulls cannot be pierced by your spike! Press Enter to continue...')

boss1 = engine.Scene('boss1', fps = 60) # Creates a scene running at ~x fps, or as fast as its legs can manage
player = objects.Player('sprites/player.txt', boss1, x_res / 2, y_res / 2)
ornstein = objects.Ornstein('sprites/ornstein.txt', boss1, 10, y_res / 2, 'pursue', player)
smough = objects.Smough('sprites/smough.txt', boss1, 1, 5, 'pursue', player)
boss1.active = True

while boss1.active: # boss1 loop

    for object in boss1.objects:
        if object is player:
            boss1.queue(player.player_input, render) # Checks for player input
            if not player.sunk:
                boss1.queue(player.shoot) # Do not change these variables
                boss1.queue(player.damage, render) # Checks if the player is damaged
            if player.health <= 0:
                render.cutscene('GAME OVER')
                input()
                quit()
        elif isinstance(object, (objects.Ornstein, objects.Smough)): # Never reference an enemy by name, otherwise it won't get garbage collected properly
            boss1.queue(object.shoot)
            boss1.queue(object.state, player) # Invokes the object's state machine
            boss1.queue(object.damage, render) # Checks if the boss is damaged

    print(player.health)

    if ornstein.health <= 0 and smough.health <= 0:
        boss1.active = False

    boss1.loop(render) # Has to go last, otherwise instructions get missed out

boss1.objects = []
render.cutscene('HMS Ornstein and HMS Smough sunk! Press Enter to continue...')

level3 = engine.Scene('level3', fps = 60) # Creates a scene running at ~x fps, or as fast as its legs can manage
player = objects.Player('sprites/player.txt', level3, x_res / 2, y_res / 2)
level3.active = True

while level3.active: # level3 loop

    for spawn in level3.spawns:
        if (level3.frame != 0) and ((level3.frame / level3.fps) % int(spawn[0]) == 0):
            x = eval('objects.{0}({1}, {2}, {3}, {4}, {5})'.format(spawn[1], spawn[2], spawn[3], '0', str(int(random.random() * render.y_res)), spawn[6]))

    for object in level3.objects:
        if object is player:
            level3.queue(player.player_input, render) # Checks for player input
            if not player.sunk:
                level3.queue(player.shoot) # Do not change these variables
                level3.queue(player.damage, render) # Checks if the player is damaged
            if player.health <= 0:
                render.cutscene('GAME OVER')
                input()
                quit()
        elif isinstance(object, objects.Enemy): # Never reference an enemy by name, otherwise it won't get garbage collected properly
            if isinstance(object, objects.Shooter):
                level3.queue(object.shoot)
            level3.queue(object.state) # Invokes the object's state machine
            level3.queue(object.damage, render) # Checks if the object is damaged

    if level3.frame / level3.fps == level_time:
        level3.active = False

    level3.loop(render) # Has to go last, otherwise instructions get missed out

level3.objects = []
render.cutscene("WARNING: Is that... good God! It's HMS Thatcher! Give her all you've got!")

boss2 = engine.Scene('boss2', fps = 60) # Creates a scene running at ~x fps, or as fast as its legs can manage
player = objects.Player('sprites/player.txt', boss2, x_res / 2, y_res / 2)
thatcher_cannon = objects.ThatcherCannon('sprites/thatcher_cannon.txt', boss2, 5, y_res / 2, 'pursue', player)
thatcher = objects.Thatcher('sprites/thatcher.txt', boss2, 0, 0, 'nothing', player)
boss2.active = True

while boss2.active: # boss2 loop

    for object in boss2.objects:
        if object is player:
            boss2.queue(player.player_input, render) # Checks for player input
            if not player.sunk:
                boss2.queue(player.shoot) # Do not change these variables
                boss2.queue(player.damage, render) # Checks if the player is damaged
            if player.health <= 0:
                render.cutscene('GAME OVER')
                input()
                quit()
        elif isinstance(object, (objects.Thatcher, objects.ThatcherCannon)): # Never reference an enemy by name, otherwise it won't get garbage collected properly
            boss2.queue(object.shoot)
            boss2.queue(object.state, player) # Invokes the object's state machine
            boss2.queue(object.damage, render) # Checks if the boss is damaged

    print(player.health)

    if thatcher.health <= 0:
        boss2.active = False

    boss2.loop(render) # Has to go last, otherwise instructions get missed out

boss2.objects = []
render.cutscene('The witch is dead, and we can breath easy. Mission success.')
input()