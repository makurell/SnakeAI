import copy
import random
import time


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return str(self.x)+', '+str(self.y)

class Field:
    """
    Coordinate system: Origin is top-left
    """

    def __init__(self,
                 width=20,
                 height=20):
        # params
        self.width = width
        self.height = height

        # init
        random.seed(0)
        self.eat_timings = [0] # no steps taken to eat (for each eat)

        self.game_over = False
        self.eaten = 0
        self.food_pos = None

        self.snake_arr = []
        self.snake_dir = 2 # up, down, right, left
        self.prev_snake_dir = 0

        # init snake_arr
        for i in range(3):
            self.snake_arr.append(Pos(i,0))

        self.__spawn_food()

    def __spawn_food(self):
        while True:
            self.food_pos = Pos(random.randint(0,self.width-1),
                                random.randint(0,self.height-1))
            if self.food_pos not in self.snake_arr:
                return

    def __step_snake(self):
        newpos = copy.deepcopy(self.snake_arr[-1])
        if self.snake_dir == 0:
            newpos.y-=1
        elif self.snake_dir == 1:
            newpos.y+=1
        elif self.snake_dir == 2:
            newpos.x+=1
        elif self.snake_dir == 3:
            newpos.x-=1

        # position wrap around
        newpos = Pos(newpos.x%self.width, newpos.y%self.height)

        if newpos == self.snake_arr[-2]:
            # trying to go backwards in on yourself
            self.snake_dir=self.prev_snake_dir # override move dir to a last valid one
            return self.__step_snake() # re-step
        if newpos in self.snake_arr:
            # went into self
            self.game_over = True
            return

        self.snake_arr.append(newpos)
        if not newpos == self.food_pos:
            del self.snake_arr[0]
            self.eat_timings[-1]+=1
        else:
            self.eaten+=1
            self.__spawn_food()
            self.eat_timings.append(0)

        self.prev_snake_dir = self.snake_dir

    def step(self):
        self.__step_snake()

    def str_render(self):
        buffer = []
        for row in range(self.height):
            buf = ''
            for col in range(self.width):
                cur = Pos(col,row)
                if cur in self.snake_arr:
                    buf+= '#'
                elif cur == self.food_pos:
                    buf+= 'o'
                else:
                    buf+= '.'
            buffer.append(buf)
        return '\n'.join(buffer)