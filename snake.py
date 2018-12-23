import copy
import random
import numpy as np

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return str(self.x)+', '+str(self.y)

    def dist(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**(1/2)

def cart_to_pol(x, y):
    rho = np.hypot(x,y)
    phi = np.arctan2(y, x)
    return rho, phi

def get_dir(ref: Pos, other: Pos, dirs_no=8):
    """
    Classify the relative position of `other` to `ref` in terms of distance and direction class.
    Returns `None` if NA
    :return: (distance, dir index)
    """
    full = 2 * np.pi
    sec = full / float(dirs_no)
    half_sec = sec / 2.0

    rho, phi = cart_to_pol(ref.x - other.x, ref.y - other.y)
    for i in range(1, dirs_no + 1):  # start w/ 1 up to and including dirs_no
        if sec * i - half_sec <= phi % full < sec * i or (sec * i) % full <= phi % full < (sec * i + half_sec) % full:
            return rho, i - 1

    return None

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
        # random.seed(0)
        self.eat_timings = [0] # no steps taken to eat (for each eat)

        self.game_over = False
        self.eaten = 0
        self.food_pos = None

        self.snake_arr = []
        self.snake_dir = 2 # up, down, right, left
        self.prev_snake_dir = 0

        # init snake_arr
        snake_dir = random.choice([
            (0,1),
            (1,0),
            (0,-1),
            (-1,0)
        ])
        cur_pos = Pos(random.randint(0,self.width-1),random.randint(0,self.height-1))
        for i in range(3):
            self.snake_arr.append(cur_pos)
            cur_pos.x=(cur_pos.x+snake_dir[0])%self.width
            cur_pos.y=(cur_pos.y+snake_dir[1])%self.height

        self.__spawn_food()

    def __spawn_food(self):
        while True:
            self.food_pos = Pos(random.randint(0,self.width-1),
                                random.randint(0,self.height-1))
            if self.food_pos not in self.snake_arr:
                return

    def __step_snake(self):
        ate = False
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
        # newpos = Pos(newpos.x%self.width, newpos.y%self.height)
        if newpos.x>=self.width or newpos.x<0:
            # border kill
            self.game_over = True
            return False
        if newpos.y>=self.height or newpos.y<0:
            # border kill
            self.game_over = True
            return False

        if newpos == self.snake_arr[-2]:
            # trying to go backwards in on yourself
            self.snake_dir=self.prev_snake_dir # override move dir to a last valid one
            return self.__step_snake() # re-step
        if newpos in self.snake_arr:
            # went into self
            self.game_over = True
            return False

        self.snake_arr.append(newpos)
        if not newpos == self.food_pos:
            del self.snake_arr[0]
            self.eat_timings[-1]+=1
        else:
            # print('EAT')
            self.eaten+=1
            self.__spawn_food()
            self.eat_timings.append(0)
            ate = True

        self.prev_snake_dir = self.snake_dir
        return ate

    def step(self):
        return self.__step_snake()

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

    def get_senses(self):
        head = self.snake_arr[-1]
        data = []

        dirs = [
            (-1,1),
            (0,1),
            (1,1),
            (1,0),
            (1,-1),
            (0,-1),
            (-1,-1),
            (-1,0)
        ]

        for dir_vec in dirs:
            curpos = copy.deepcopy(head)

            found_food, found_tail = False, False

            curpos.x+=dir_vec[0]
            curpos.y+=dir_vec[1]
            dist = 1

            dir_data = [0,0,0]

            while 0<=curpos.x<self.width and 0<=curpos.y<self.height:
                if not found_food and self.food_pos == curpos:
                    dir_data[0] = 1
                    found_food = True

                if not found_tail and curpos in self.snake_arr:
                    dir_data[1] = 1/float(dist)
                    found_tail = True

                curpos.x += dir_vec[0]
                curpos.y += dir_vec[1]
                dist+=1

            dir_data[2] = 1/float(dist)
            data.extend(dir_data)

        # print(data)
        return data
