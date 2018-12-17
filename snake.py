import copy
import math
import random
import time
import numpy as np

def cart_to_pol(x, y):
    rho = np.hypot(x,y)
    phi = np.arctan2(y, x)
    return (rho, phi)

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
            print('EAT')
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

    def get_senses(self):
        head = self.snake_arr[-1]

        dirs_no = 8
        full = 2*np.pi
        sec = full/float(dirs_no)
        half_sec = sec/2.0

        dir_names = '↖↑↗→↘↓↙←'

        food_dist, food_angle = cart_to_pol(head.x-self.food_pos.x,head.y-self.food_pos.y)
        for i in range(1,dirs_no+1): # start w/ 1 up to and including dirs_no
            if sec*i-half_sec <= food_angle%full < sec*i or (sec*i)%full <= food_angle%full < (sec*i+half_sec)%full:
                print(dir_names[i-1])


        print(food_dist,food_angle*57.2958)

    # def get_senses(self):
    #     """
    #     Neural network input
    #     """
    #     # thing ID: nothing, body, food
    #
    #     inf = math.ceil((self.width**2+self.height**2)**(1/2))
    #     thing_ids=[0,0,0,0,0,0,0,0] # 8 directions # 2 bits each
    #     thing_dists=[inf,inf,inf,inf,inf,inf,inf,inf] # 9 bits each
    #     # thing_ids=[0,0,0,0] # 9 directions
    #     # thing_dists=[inf,inf,inf,inf]
    #
    #     ret = []
    #
    #     incrs = [
    #         (1,0),
    #         (1,1),
    #         (0,1),
    #         (-1,1),
    #         (-1,0),
    #         (-1,-1),
    #         (0,-1),
    #         (1,-1)
    #     ]
    #
    #     for diri, incr in enumerate(incrs):
    #         # search this dir
    #         cur = copy.deepcopy(self.snake_arr[-1]) # head of snake
    #         curdist = 0
    #         while self.width > cur.x > 0 and self.height > cur.y > 0:
    #             cur.y+=incr[0]
    #             cur.x+=incr[1]
    #
    #             if cur in self.snake_arr:
    #                 thing_dists[diri]=curdist
    #                 thing_ids[diri]=1
    #                 break
    #             elif cur == self.food_pos:
    #                 thing_dists[diri] = curdist
    #                 thing_ids[diri]=2
    #                 break
    #
    #             curdist+=1
    #
    #
    #         # append data for this dir to buffer
    #         ret.extend([float(x) for x in format(thing_ids[diri],'02b')])
    #         # ret.extend([float(x) for x in format(thing_dists[diri],'09b')]) # if want to do binary way
    #         ret.append(1-(thing_dists[diri]/inf)) # reduces node num from 88 to 24
    #
    #     # print(thing_dists)
    #     return ret