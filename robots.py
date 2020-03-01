import sys
import json


# Clear the log file 

open('log.txt', 'w').close()


log = []



class Processor:
    def __init__(self, instructions_ref, mode):

        self.instructions_ref = instructions_ref
        self.mode = mode

    def process_instructions(self):

        with open(instructions_ref) as file:
            data = file.read()

        instructions = data.split('\n')

        robot_count = -1
        robots = []

        for row in instructions:
            
            # error handling in case there is an empty string
            # in the instructions etc
            try:
                row = json.loads(row)
            except:
                row = {'type': 'finished'}
                

            if row.get('type') == 'asteroid':
                ast_x = row.get('size').get('x')
                ast_y = row.get('size').get('y')
                ast_mode = 'default'
                asteroid = Asteroid(ast_x, ast_y, ast_mode)
                log.append(
                    f'setting asteroid x dimension to {row.get("size").get("x")}')
                log.append(
                    f'setting asteroid y dimension to {row.get("size").get("y")}')

            if row.get('type') == 'new-robot':
                robot_count += 1
                log.append(f'creating new robot, number {robot_count}')
                x = row.get('position').get('x')
                y = row.get('position').get('y')
                bearing = row.get('bearing')

                robots.append(Robot(x, y, bearing))

            if row.get('type') == 'move':
                log.append(
                    f'sending movement instruction to robot number {robot_count} ')
                robots[robot_count].store_move(row.get('movement'))

        log.append('now calling the robots methods to get their output')

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

        ast_x = ast_size[0]
        ast_y = ast_size[1]
        ast_mode = ast_size[2]
        x = self.x
        y = self.y

        if ast_mode == '3d':
            if self.x >= ast_x:
                x = self.x - ast_x
            if self.y >= ast_y:
                y = self.y - ast_y
            if self.x <= 0:
                x = self.x + ast_x
            if self.y <= 0:
                y = self.y + ast_y

        return {"type": "robot", "position": {"x": x, "y": y}, "bearing": self.bearing}


instructions_ref = sys.argv[1]

mode_ref = sys.argv[2] if len(sys.argv) == 3 else 'default'

processor = Processor(instructions_ref, mode_ref)

processor.process_instructions()


with open('log.txt', 'w') as f:
    for row in log:
        f.write("%s\n" % row)



