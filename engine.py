import time
import colorama
import keyboard

class Renderer: # Contains information about the rendered screen

    def __init__(self, x_res, y_res): # Takes a resolution as an argument

        self.x_res = x_res # IMPORTANT: X GOES DOWN
        self.y_res = y_res # IMPORTANT: Y GOES ACROSS
        self.grid = [] # 2D list that contains every character on the rendered screen
        self.screen = '' # Newline-separated string that contains the entire output
        self.empty = ' ' # Filler character for empty cells

        colorama.init() # Allows interpretation of ANSI escape characters, necessary for self.display()
        
    def refresh(self): # Resets grid and screen

        self.grid = []
        self.screen = ''

        for x in range(self.x_res): # Grid is constructed as a list of strings for space and time efficiency; works like scanlines
            self.grid.append('')
            for y in range(self.y_res):
                self.grid[x] += self.empty

    def display(self): # Renders the screen

        for x, row in enumerate(self.grid): # Converts the information in self.grid into a printable string and renders the screen
            for y, cell in enumerate(row):
                if cell == self.empty:
                    self.screen += self.empty
                else:
                    self.screen += cell
            else:
                self.screen += '\n'

        print('\033[H\033[3J') # ANSI escape characters that move the cursor and clear both the terminal and the buffer
        print(self.screen, flush = True) # Flush prevents buffer and forces immediate execution

    def update(self, object): # Updates the screen with a screen object sprite if the space is empty

        for x, row in enumerate(object.sprite): # For each line of the sprite:
            if self.in_bounds(int(object.x) + x, int(object.y)):
                line = list(self.grid[int(object.x) + x])
                for y, cell in enumerate(row):
                    if self.in_bounds(int(object.x) + x, int(object.y) + y) and self.grid[int(object.x) + x][int(object.y) + y] == self.empty:
                        line[int(object.y) + y] = cell
                else:
                    self.grid[int(object.x) + x] = line

    def cutscene(self, text):

        self.refresh()
        self.screen = text
        self.display()
        keyboard.wait('enter')
        self.refresh()
        self.screen = ''
        self.display()

    def in_bounds(self, x, y):

        if x >= 0 and x < self.x_res and y >= 0 and y < self.y_res:
            return True
        else:
            return False

    def on_screen(self, object):

        if (object.x + object.size[0] <= 0 or object.x >= self.x_res) or (object.y + object.size[1] <= 0 or object.y >= self.y_res):
            return False
        else:
            return True

class Scene: # Contains information about the main event loop

    def __init__(self, name, fps):
                
        self.fps = fps # There's probably an upper limit to this defined by the time it takes to render, but I don't know what it is
        self.active = True # Indicates whether this scene is currently active
        self.frame = 0 # fps-dependent
        self.instructions = [] # List of instructions to be performed in the current frame
        self.objects = [] # List of objects in the current scene

        with open('levels/{0}.txt'.format(name), 'r') as file:
            buffer = file.read().splitlines()
            self.spawns = [line.split(' ') for line in buffer]

    def queue(self, task, *args): # Syntactic sugar for queueing a function and its parameters

        self.instructions.append([task, *args])

    def include(self, object): # Syntactic sugar for including an object in the current scene

        self.objects.append(object)

    def destroy(self, object): # Allows destroy method to be called anywhere; use carefully

        try: # Sometimes this doesn't work for some reason; just patch it over and move on
            self.objects.remove(object) # Remove references for cleaner deletion
            ScreenObject.instances.remove(object)
            PhysicsObject.instances.remove(object)
            del object # YEET
        except ValueError:
            del object # SUPER YEET
            
    def loop(self, renderer): # Queues and executes all instructions for a single frame of the event loop

        start_time = time.time() # Logs the start time of the frame
        current_time = 0 # Logs the current time

        def wrapper(task, args):
            task(*args) # Allows parameters to be passed as list

        self.queue(renderer.refresh) # Resets the grid and the screen

        if len(self.objects) > 0: # Only activates if there any objects created
            for object in self.objects: # For every object:
                if object in PhysicsObject.instances: # If physics object:
                    self.queue(object.move) # Update movement
                    self.queue(renderer.update, object) # Render the object

        self.queue(renderer.display)

        for task in self.instructions:
            if len(task) > 1: # If function with parameters:
                wrapper(task[0], task[1:]) # Use wrapper to execute function with queued parameters
            else: # If procedure without parameters:
                task[0]() # Execute without wrapper
        self.instructions = [] # Clears buffer so the next frame of instructions can be performed

        if len(self.objects) > 0: # Manual garbage collection; make sure not to reference objects after deletion
            for object in self.objects: # For every object:
                if not renderer.on_screen(object): # If it's off-screen, yeet it
                    self.destroy(object)

        while current_time < start_time + (1 / self.fps): # Hangs the program until the end of the current frame
            current_time = time.time() # Implementation of frame timing without asyncio, because I enjoy pain
        else:
            self.frame += 1

        return True # Just in case any other method needs to know when the frame ends

class ScreenObject: # Base class for a game object

    instances = []
    
    def __init__(self, sprite, scene, x, y):

        with open(sprite, 'r') as file: # Opens the file containing the sprite information
            self.sprite = file.read().splitlines() # Basically readlines() without \n

        self.x = x # Initial x for top-left of sprite
        self.y = y # Initial y for top-left of sprite
        self.size = (len(self.sprite), len(self.sprite[0])) # Rectangular size of the sprite
        self.adjacent = (len(self.sprite) + 2, len(self.sprite[0]) + 2) # 1 larger than self.size to handle collision
        self.scene = scene # Object must be initialised into a specific scene

        scene.include(self) # Automatically includes self in the specified scene
        self.instances.append(self)

    def get_location(self):

        location = []

        for x in range(int(self.x), int(self.x + self.size[0])):
            for y in range(int(self.y), int(self.y + self.size[1])):
                location.append((x, y))

        return location

class PhysicsObject(ScreenObject):

    instances = []

    def __init__(self, scene, sprite, x, y):

        super().__init__(scene, sprite, x, y)
        self.x_vector = 0
        self.y_vector = 0
        super().instances.append(self)
        self.instances.append(self)

    def move(self): # Per-frame movement by movement vector

        self.x += self.x_vector
        self.y += self.y_vector

    def set_x(self, x): # Set x movement vector

        self.x_vector = x

    def set_y(self, y): # Set y movement vector

        self.y_vector = y