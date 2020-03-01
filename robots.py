instructions = [{"type": "asteroid", "size": {"x": 5, "y": 5}},
{"type": "new-robot", "position": {"x": 1, "y": 2}, "bearing": "north"},
{"type": "move", "movement": "turn-left"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-left"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-left"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-left"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "move-forward"},
{"type": "new-robot", "position": {"x": 3, "y": 3}, "bearing": "east"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-right"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-right"},
{"type": "move", "movement": "move-forward"},
{"type": "move", "movement": "turn-right"},
{"type": "move", "movement": "turn-right"},
{"type": "move", "movement": "move-forward"}]


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
      print(f'calling self.bearing = {self.bearing}')
      return

    if self.bearing == 'west':
      self.bearing = 'south'
      print(f'calling self.bearing = {self.bearing}')
      return

    if self.bearing == 'south':
      self.bearing = 'east'
      print(f'calling self.bearing = {self.bearing}')
      return

    if self.bearing == 'east':
      self.bearing = 'north'
      print(f'calling self.bearing = {self.bearing}')
      return


  
  

  def turn_right(self):
    if self.bearing == 'north':
      self.bearing = 'east'
      print(f'calling self.bearing = {self.bearing}')
      return
    if self.bearing == 'east':
      self.bearing = 'south'
      print(f'calling self.bearing = {self.bearing}')
      return
    if self.bearing == 'south':
      self.bearing = 'west'
      print(f'calling self.bearing = {self.bearing}')
      return
    if self.bearing == 'west':
      self.bearing = 'north'
      print(f'calling self.bearing = {self.bearing}')
      return


  def move_forward(self):

    if self.bearing == 'north':
      self.y += 1
      print(f'calling self.y = {self.y}')
    if self.bearing == 'east':
      self.x += 1
      print(f'calling self.x = {self.x}')
    if self.bearing == 'south':
      self.y -= 1
      print(f'calling self.y = {self.y}')
    if self.bearing == 'west':
      self.x -= 1
      print(f'calling self.x = {self.x}')
    

  def calculate_location(self, ast_size):


    for move in self.moves_list:

      if move == 'turn-left':
        self.turn_left()
        print(f'calling turn left, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')
      if move == 'turn-right':
        self.turn_right()
        print(f'calling turn right, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')
      if move == 'move-forward':
        self.move_forward()
        print(f'calling move forward, bearing = {self.bearing}  self.x = {self.x}, self.y = {self.y}')

    ast_x = ast_size[0]
    ast_y = ast_size[1]
    ast_mode = ast_size[2]
    x= self.x
    y= self.y

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




def processor(instructions):
  robot_count = -1
  robots = []

  for row in instructions:

    if row.get('type') == 'asteroid':
      ast_x = row.get('size').get('x')
      ast_y = row.get('size').get('y')
      ast_mode = 'default'
      asteroid = Asteroid(ast_x, ast_y, ast_mode)
      print(f'setting asteroid dimensions to x: {row.get("size").get("x")}')
      print(f'setting asteroid dimensions to y: {row.get("size").get("y")}')


    if row.get('type') == 'new-robot':
      robot_count+=1
      print(f'creating new robot, number {robot_count}')
      x = row.get('position').get('x')
      y = row.get('position').get('y')
      bearing = row.get('bearing')

      robots.append(Robot(x, y, bearing))

    if row.get('type') == 'move':
      print(f'sending movement instruction to robot number {robot_count} ')
      robots[robot_count].store_move(row.get('movement'))

  print('now calling the robots methods to get their output')

  for row in robots:
    print(row.calculate_location(asteroid.share_size()))


processor(instructions)