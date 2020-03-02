import sys
import json


# Clear the log file from previous runs

open('log.txt', 'w').close()

log = []


class Processor:
    def __init__(self, instructions_ref, mode):

        self.instructions_ref = instructions_ref
        self.mode = mode

    def process_instructions(self):

        with open(instructions_ref) as file:
            data = file.read()

        # Split data into rows for iteration
        instructions = data.split('\n')

        # Avoid off by one error later
        # as we will use the robot's number to find its index
        # in the list of robots when we send it instructions
        robot_count = -1
        robots = []

        for row in instructions:

            # Error handling in case there is an empty string
            # in the instructions etc
            try:
                row = json.loads(row)
            except:
                # Avoid .get throwing an error by making
                # replacing blank row with a dictionary 
                # even though it won't be used
                row = {'type': 'finished'}

            if row.get('type') == 'asteroid':
                ast_x = row.get('size').get('x')
                ast_y = row.get('size').get('y')
                ast_mode = self.mode
                asteroid = Asteroid(ast_x, ast_y, ast_mode)
                log.append(
                    f'setting asteroid x dimension to {row.get("size").get("x")}')
                log.append(
                    f'setting asteroid y dimension to {row.get("size").get("y")}')

            
            # if new-robot, create a new robot and add it to the robots list
            if row.get('type') == 'new-robot':
                robot_count += 1
                log.append(f'creating new robot, number {robot_count +1}')
                x = row.get('position').get('x')
                y = row.get('position').get('y')
                bearing = row.get('bearing')

                robots.append(Robot(x, y, bearing))

            # new-robot is always followed by instructions for that robot
            # so send the instuctions to the right robot!
            if row.get('type') == 'move':
                log.append(
                    f'sending movement instruction to robot number {robot_count +1} ')
                robots[robot_count].store_move(row.get('movement'))

        log.append('now calling the robots methods to get their output')

        # Now all objects have been set up, call the robots to
        # calculate their loction then output it to the console
        for row in robots:
            print(row.calculate_location(asteroid.share_size()))


class Asteroid:
    def __init__(self, x, y, mode):
        self.x = x
        self.y = y
        self.mode = mode

    def share_size(self):
        return self.x, self.y, self.mode


class Robot:
    def __init__(self, x, y, bearing):
        self.x = x
        self.y = y
        self.bearing = bearing
        self.moves_list = []

    def store_move(self, move):
        self.moves_list.append(move)

    def turn_left(self):

        if self.bearing == 'north':
            self.bearing = 'west'
            return

        if self.bearing == 'west':
            self.bearing = 'south'
            return

        if self.bearing == 'south':
            self.bearing = 'east'
            return

        if self.bearing == 'east':
            self.bearing = 'north'
            return

    def turn_right(self):
        if self.bearing == 'north':
            self.bearing = 'east'
            return
        if self.bearing == 'east':
            self.bearing = 'south'
            return
        if self.bearing == 'south':
            self.bearing = 'west'
            return
        if self.bearing == 'west':
            self.bearing = 'north'
            return

    def move_forward(self):

        if self.bearing == 'north':
            self.y += 1
        if self.bearing == 'east':
            self.x += 1
        if self.bearing == 'south':
            self.y -= 1
        if self.bearing == 'west':
            self.x -= 1

    def calculate_location(self, ast_size):

        for move in self.moves_list:

            if move == 'turn-left':
                self.turn_left()
                log.append(
                    f'calling turn left, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')
            if move == 'turn-right':
                self.turn_right()
                log.append(
                    f'calling turn right, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')
            if move == 'move-forward':
                self.move_forward()
                log.append(
                    f'calling move forward, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')

        
        # Code below only relevant if mode is set to 3d
        ast_x = ast_size[0]
        ast_y = ast_size[1]
        ast_mode = ast_size[2]
        x = self.x
        y = self.y

        # if mode is 3d, the robot can't go past x4 or y4 on a 5x5 asteroid
        # therefor it will go all around and back to 0
        log.append(f'Mode is {ast_mode}')
        if ast_mode == '3d':
            if self.x >= ast_x:
                x = self.x - ast_x
            if self.y >= ast_y:
                y = self.y - ast_y
            if self.x <= 0:
                x = self.x + ast_x
            if self.y <= 0:
                y = self.y + ast_y

        # Finally, output final location of robot!
        return {"type": "robot", "position": {"x": x, "y": y}, "bearing": self.bearing}


# Execution logic:

# Make sure we have some instructions, if not load the example instructions

try:
    instructions_ref = sys.argv[1]
except:
    instructions_ref = 'instructions.txt'
    print('No instructions given in command line, \
results using example instructions:')

mode_ref = sys.argv[2] if len(sys.argv) == 3 else 'default'

log.append(f'Mode from command line is {mode_ref}')

# Instantiate the processor and process the instructions

processor = Processor(instructions_ref, mode_ref)

processor.process_instructions()


with open('log.txt', 'w') as f:
    for row in log:
        f.write("%s\n" % row)
