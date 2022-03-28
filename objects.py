import engine
import keyboard
import math

class Shooter:

    def shoot(self):
        
        pass

        #if self.cooldown_timer > 1:
        #    self.cooldown_timer -= 1
        #else:
        #    bullet = Bullet("sprites/bullet.txt", self.scene, x, y, self)
        #    bullet.set_x(x_vector)
        #    bullet.set_y(y_vector)
        #    self.cooldown_timer = self.cooldown

class Player(engine.PhysicsObject, Shooter):

    def __init__(self, sprite, scene, x, y):

        super().__init__(sprite, scene, x, y)
        self.health = 100
        self.i_frames = 0.5 * scene.fps
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 20 / scene.fps # Per second, fps-independent
        self.sunk = False
        self.sink_cooldown = 0.1 * scene.fps
        self.sink_timer = 0.1 * scene.fps # This one ticks down
                
    def up(self):

        self.x -= self.speed

    def down(self):

        self.x += self.speed

    def left(self):

        self.y -= self.speed

    def right (self):

        self.y += self.speed

    def sink(self): # Reverses sunk state

        if self.sink_timer > 1:
            self.sink_timer -= 1
        else:
            if self.sunk == False:
                self.sunk = True
                with open('sprites/player_sunk.txt', 'r') as file: # Opens the file containing the sprite information
                    self.sprite = file.read().splitlines() # Basically readlines() without \n
            else:
                self.sunk = False
                with open('sprites/player.txt', 'r') as file: # Opens the file containing the sprite information
                    self.sprite = file.read().splitlines() # Basically readlines() without \n
            self.sink_timer = self.sink_cooldown

    def player_input(self, renderer):

        if keyboard.is_pressed('w') and self.x > 0:
            self.up()
        if keyboard.is_pressed('s') and self.x + self.size[0] < renderer.x_res:
            self.down()
        if keyboard.is_pressed('a') and self.y > 0:
            self.left()
        if keyboard.is_pressed('d') and self.y + self.size[1] < renderer.y_res:
            self.right()
        if keyboard.is_pressed('space'):
            self.sink()

    def collision(self):

        hitbox = self.get_location() # Creates a list of cells the player occupies

        for object in engine.ScreenObject.instances:
            if object is not self and not (isinstance(object, Bullet) and object.friendly):
                for point in object.get_location():
                    if point in hitbox:
                        if isinstance(object, Bullet):
                            self.scene.destroy(object)
                        return True
        else:
            return False


    def damage(self, renderer):

        if self.i_frames > 0:
            self.i_frames -= 1
        elif self.collision():
            self.health -= 1
            self.i_frames == 0.5 * self.scene.fps
            if self.health == 0:
                self.scene.destroy(self)
                self.scene.active = False

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            bullet = Bullet("sprites/bullet.txt", self.scene, self.x - 1, self.y + 1, self)
            bullet.set_x(-20 / self.scene.fps)
            bullet.set_y(0)
            self.cooldown_timer = self.cooldown

class Bullet(engine.PhysicsObject):

    def __init__(self, sprite, scene, x, y, shooter):

        super().__init__(sprite, scene, x, y)
        self.friendly = None

        if isinstance(shooter, Player): # Disables friendly fire
            self.friendly = True
        else:
            self.friendly = False

class Enemy(engine.PhysicsObject, Shooter):

    def __init__(self, sprite, scene, x, y):

        super().__init__(sprite, scene, x, y)
        self.health = 10
        self.i_frames = 0
        self.cooldown = 1
        self.speed = 10 / scene.fps

    def state(self): # Rudimentary state machine to be overridden by subclasses

        return None

    def collision(self):

        hitbox = self.get_location() # Creates a list of cells the enemy occupies

        for object in engine.ScreenObject.instances:
            if object is not self and not (isinstance(object, Bullet) and not object.friendly):
                for point in object.get_location():
                    if point in hitbox and not (isinstance(object, Player) and not object.sunk): # Proper hit detection for player
                        if isinstance(object, Bullet):
                            self.scene.destroy(object)
                        return True
        else:
            return False

    def damage(self, renderer):

        if self.i_frames > 0:
            self.i_frames -= 1
        elif self.collision():
            self.health -= 1
            self.i_frames == 0.5 * self.scene.fps
            if self.health == 0:
                self.scene.destroy(self)

class Corvette(Enemy):

    def __init__(self, sprite, scene, x, y, state):

        super().__init__(sprite, scene, x, y)
        self.health = 1
        self.i_frames = 0
        self.cooldown = 0.25 * scene.fps
        self.cooldown_timer = 0.25 * scene.fps
        self.speed = 10 / scene.fps
        self.instruction = state

    def state(self):

        return eval('self.' + self.instruction + '()')

    def descend(self):

        self.set_x(self.speed)

    def swarm(self):

        self.set_x(self.speed)
        self.set_y(math.sin(self.x))

    def nothing(self):

        pass

class Destroyer(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state):

        super().__init__(sprite, scene, x, y)
        self.health = 5
        self.i_frames = 0
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 5 / scene.fps
        self.instruction = state

    def state(self):

        return eval('self.' + self.instruction + '()')

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            bullet_nw = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y, self)
            bullet_nw.set_x(20 / self.scene.fps)
            bullet_nw.set_y(-20 / self.scene.fps)
            bullet_sw = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y, self)
            bullet_sw.set_x(20 / self.scene.fps)
            bullet_sw.set_y(-20 / self.scene.fps)
            bullet_ne = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y + 2, self)
            bullet_ne.set_x(20 / self.scene.fps)
            bullet_ne.set_y(20 / self.scene.fps)
            bullet_se = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y + 2, self)
            bullet_se.set_x(20 / self.scene.fps)
            bullet_se.set_y(20 / self.scene.fps)
            self.cooldown_timer = self.cooldown

    def descend(self):

        self.set_x(self.speed)

    def swarm(self):

        self.set_x(self.speed)
        self.set_y(math.sin(self.x * 2))

    def nothing(self):

        pass

class Cruiser(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state):

        super().__init__(sprite, scene, x, y)
        self.health = 20
        self.i_frames = 0
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 2 / scene.fps
        self.instruction = state

    def state(self):

        return eval('self.' + self.instruction + '()')

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            bullet_nw = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y, self)
            bullet_nw.set_x(20 / self.scene.fps)
            bullet_nw.set_y(-20 / self.scene.fps)
            bullet_smw = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y, self)
            bullet_smw.set_x(20 / self.scene.fps)
            bullet_smw.set_y(-20 / self.scene.fps)
            bullet_sw = Bullet("sprites/bullet.txt", self.scene, self.x + 5, self.y, self)
            bullet_sw.set_x(20 / self.scene.fps)
            bullet_sw.set_y(-20 / self.scene.fps)
            bullet_ne = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y + 2, self)
            bullet_ne.set_x(20 / self.scene.fps)
            bullet_ne.set_y(20 / self.scene.fps)
            bullet_sme = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y + 2, self)
            bullet_sme.set_x(20 / self.scene.fps)
            bullet_sme.set_y(20 / self.scene.fps)
            bullet_se = Bullet("sprites/bullet.txt", self.scene, self.x + 5, self.y + 2, self)
            bullet_se.set_x(20 / self.scene.fps)
            bullet_se.set_y(20 / self.scene.fps)
            self.cooldown_timer = self.cooldown

    def descend(self):

        self.set_x(self.speed)

    def swarm(self):

        self.set_x(self.speed)
        self.set_y(math.sin(self.x * 2))

    def nothing(self):

        pass

class Ornstein(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state, player):

        super().__init__(sprite, scene, x, y)
        self.health = 50
        self.i_frames = 0
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 30 / scene.fps
        self.instruction = state
        self.base_x = x
        self.ability = 5 * scene.fps # In seconds, fps-independent
        self.ability_timer = 5 * scene.fps # This one ticks down
        self.ability_active = False

    def state(self, player):

        return eval('self.{0}(player)'.format(self.instruction))

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            bullet_nw = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y, self)
            bullet_nw.set_x(20 / self.scene.fps)
            bullet_nw.set_y(-20 / self.scene.fps)
            bullet_sw = Bullet("sprites/bullet.txt", self.scene, self.x + 5, self.y, self)
            bullet_sw.set_x(20 / self.scene.fps)
            bullet_sw.set_y(-20 / self.scene.fps)
            bullet_ne = Bullet("sprites/bullet.txt", self.scene, self.x + 1, self.y + 2, self)
            bullet_ne.set_x(20 / self.scene.fps)
            bullet_ne.set_y(20 / self.scene.fps)
            bullet_se = Bullet("sprites/bullet.txt", self.scene, self.x + 5, self.y + 2, self)
            bullet_se.set_x(20 / self.scene.fps)
            bullet_se.set_y(20 / self.scene.fps)
            self.cooldown_timer = self.cooldown

    def pursue(self, player):

        if self.ability_timer > 1 and self.ability_active == False:
            self.ability_timer -= 1
            if self.x > self.base_x:
                self.set_x(-0.5 * self.speed)
            else:
                self.set_x(0)
                self.y = player.y
        else:
            self.ability_active = True
            if self.x < player.x:
                self.set_x(self.speed)
            else:
                self.set_x(0)
                self.ability_active = False
                self.ability_timer = self.ability

    def collision(self):

        hitbox = self.get_location() # Creates a list of cells the enemy occupies

        for object in engine.ScreenObject.instances:
            if object is not self and not (isinstance(object, Bullet) and not object.friendly):
                for point in object.get_location():
                    if point in hitbox and not (isinstance(object, Player)): # Proper hit detection for player
                        if isinstance(object, Bullet):
                            self.scene.destroy(object)
                        return True
        else:
            return False

    def damage(self, renderer):

        if self.i_frames > 0:
            self.i_frames -= 1
        elif self.collision():
            self.health -= 1
            self.i_frames == 0.25 * self.scene.fps
            if self.health == 0:
                self.scene.destroy(self)

class Smough(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state, player):

        super().__init__(sprite, scene, x, y)
        self.health = 50
        self.i_frames = 0
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 15 / scene.fps
        self.instruction = state
        self.base_x = x
        self.ability = 5 * scene.fps # In seconds, fps-independent
        self.ability_timer = 5 * scene.fps # This one ticks down
        self.ability_stage = 0

    def state(self, player):

        return eval('self.{0}(player)'.format(self.instruction))

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            bullet_nw = Bullet("sprites/bullet.txt", self.scene, self.x + 2, self.y, self)
            bullet_nw.set_x(20 / self.scene.fps)
            bullet_nw.set_y(-20 / self.scene.fps)
            bullet_smw = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y, self)
            bullet_smw.set_x(20 / self.scene.fps)
            bullet_smw.set_y(-20 / self.scene.fps)
            bullet_sw = Bullet("sprites/bullet.txt", self.scene, self.x + 4, self.y, self)
            bullet_sw.set_x(20 / self.scene.fps)
            bullet_sw.set_y(-20 / self.scene.fps)
            bullet_ne = Bullet("sprites/bullet.txt", self.scene, self.x + 2, self.y + 6, self)
            bullet_ne.set_x(20 / self.scene.fps)
            bullet_ne.set_y(20 / self.scene.fps)
            bullet_sme = Bullet("sprites/bullet.txt", self.scene, self.x + 3, self.y + 6, self)
            bullet_sme.set_x(20 / self.scene.fps)
            bullet_sme.set_y(20 / self.scene.fps)
            bullet_se = Bullet("sprites/bullet.txt", self.scene, self.x + 4, self.y + 6, self)
            bullet_se.set_x(20 / self.scene.fps)
            bullet_se.set_y(20 / self.scene.fps)
            self.cooldown_timer = self.cooldown

    def pursue(self, player):

        if self.ability_timer > 1 and self.ability_stage == 0:
            self.ability_timer -= 1
        else:
            if self.ability_stage == 0:
                self.ability_stage = 1
            elif self.ability_stage == 1:
                if self.x < player.x:
                    self.set_x(self.speed)
                else:
                    self.set_x(0)
                    self.ability_stage = 2
            elif self.ability_stage == 2:
                if self.y < player.y and not self.collision():
                    self.set_y(2 * self.speed)
                elif self.y > player.y and not self.collision():
                    self.set_y(-2 * self.speed)
                else:
                    self.set_y(0)
                    self.ability_stage = 3
            elif self.ability_stage == 3:
                if self.x > self.base_x:
                    self.set_x(-1 * self.speed)
                else:
                    self.set_x(0)
                    self.ability_timer = self.ability
                    self.ability_stage = 0

    def collision(self):

        hitbox = self.get_location() # Creates a list of cells the enemy occupies

        for object in engine.ScreenObject.instances:
            if object is not self and not (isinstance(object, Bullet) and not object.friendly):
                for point in object.get_location():
                    if point in hitbox and not (isinstance(object, Player)): # Proper hit detection for player
                        if isinstance(object, Bullet):
                            self.scene.destroy(object)
                        return True
        else:
            return False

    def damage(self, renderer):

        if self.i_frames > 0:
            self.i_frames -= 1
        elif self.collision():
            self.health -= 1
            self.i_frames == 0.25 * self.scene.fps
            if self.health == 0:
                self.scene.destroy(self)

class Thatcher(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state, player):

        super().__init__(sprite, scene, x, y)
        self.health = 500
        self.i_frames = 0
        self.cooldown = 0.50 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.50 * scene.fps # This one ticks down
        self.instruction = state

    def state(self, player):

        return eval('self.{0}(player)'.format(self.instruction))

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            if self.scene.frame % 3 == 0:
                for y in range(1, 40, 4):
                    bullet = Bullet("sprites/bullet.txt", self.scene, self.size[0], self.y + y, self)
                    bullet.set_x(20 / self.scene.fps)
                else:
                    self.cooldown_timer = self.cooldown
            else:
                for y in range(2, 40, 4):
                    bullet = Bullet("sprites/bullet.txt", self.scene, self.size[0], self.y + y, self)
                    bullet.set_x(20 / self.scene.fps)
                else:
                    self.cooldown_timer = self.cooldown

    def nothing(self, player):

        pass

    def collision(self):

        hitbox = self.get_location() # Creates a list of cells the enemy occupies

        for object in engine.ScreenObject.instances:
            if object is not self and not (isinstance(object, Bullet) and not object.friendly):
                for point in object.get_location():
                    if point in hitbox and not (isinstance(object, (Player, ThatcherCannon))): # Proper hit detection for player
                        if isinstance(object, Bullet):
                            self.scene.destroy(object)
                        return True
        else:
            return False

    def damage(self, renderer):

        if self.i_frames > 0:
            self.i_frames -= 1
        elif self.collision():
            self.health -= 1
            self.i_frames == 0.25 * self.scene.fps
            if self.health == 0:
                self.scene.destroy(self)

class ThatcherCannon(Enemy, Shooter):

    def __init__(self, sprite, scene, x, y, state, player):

        super().__init__(sprite, scene, x, y)
        self.cooldown = 0.25 * scene.fps # In seconds, fps-independent
        self.cooldown_timer = 0.25 * scene.fps # This one ticks down
        self.speed = 30 / scene.fps
        self.instruction = state
        self.base_x = x
        self.ability = 10 * scene.fps # In seconds, fps-independent
        self.ability_timer = 10 * scene.fps # This one ticks down
        self.ability_active = False

    def state(self, player):

        return eval('self.{0}(player)'.format(self.instruction))

    def shoot(self):
               
        if self.cooldown_timer > 1:
            self.cooldown_timer -= 1
        else:
            for y in range(1, 5):
                bullet = Bullet("sprites/bullet.txt", self.scene, self.x, self.y + y, self)
                bullet.set_x(50 / self.scene.fps)
            else:
                self.cooldown_timer = self.cooldown
            
    def pursue(self, player):

        if self.ability_timer > 1 and self.ability_active == False:
            self.ability_timer -= 1
            if self.x > self.base_x:
                self.set_x(-0.5 * self.speed)
            else:
                self.set_x(0)
                self.y = player.y
        else:
            self.ability_active = True
            if self.ability_timer < self.ability:
                self.shoot()
                self.ability_timer += 5 
            else:
                self.ability_active = False