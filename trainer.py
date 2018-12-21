import random
from typing import List

import neuroga as ng
import numpy as np
import snake


def fitf1(net:ng.Network):
    field = snake.Field()

    steps_limit = 5
    bonus = 0

    for i in range(steps_limit):
        if not field.game_over:
            output = net.forward(field.get_senses()).argmax()
            field.snake_dir = output
            field.step()
        else:
            bonus-=(steps_limit-i)
            break

    avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    return len(field.snake_arr)-avg_eat_timing + bonus

def fitf2(net:ng.Network):
    field = snake.Field()

    steps_limit = 800

    sum_dists = 0

    i=0
    for i in range(steps_limit):
        if not field.game_over:
            output = net.forward(field.get_senses())
            field.snake_dir = output.argmax()
            field.step()
            # print(output)


            sum_dists+=field.snake_arr[-1].dist(field.food_pos)
        else:
            break

    avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    return avg_eat_timing + (max(steps_limit-i,0)) - (field.eaten*100) + sum_dists/float(i)

def fitf3(net):
    field = snake.Field()
    steps_limit = 20000

    i=0
    for i in range(steps_limit):
        if field.game_over: break
        output = net.forward(field.get_senses())
        # print(output)
        field.snake_dir = output.argmax()
        field.step()

        if field.eat_timings[-1]>80: # not really going for the food = kill
            break

    avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    return field.eaten*100 - avg_eat_timing*50 + i

def fitf4(net):
    field = snake.Field()
    live_time = 200
    i=0

    while live_time > 0:
        if field.game_over: break
        output = net.forward(field.get_senses())
        field.snake_dir = output.argmax()
        if field.step():
            live_time+=100
        live_time-=1
        i+=1

    avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    return max(field.eaten*300, field.eaten**3) - avg_eat_timing*50 + i**2

def mutate(pop:List[ng.Agent], **kwargs)->List[ng.Agent]:
    for agent in pop:
        for i, weights in enumerate(agent.net.weights):
            for j, weight in enumerate(weights):
                for k, w in enumerate(weight):
                    # print(w)
                    if random.random() < 0.6:
                        # mutate
                        new = w + np.random.normal()/5
                        # print(new)
                        new = max(min(new,1),-1)
                        agent.net.weights[i][j][k] = new

                        # agent.net.weights[i][j] = min(
                        #     agent.net.weights[i][j], 1
                        # )
                        # agent.net.weights[i][j] = max(
                        #     agent.net.weights[i][j], -1
                        # )

        agent.net.biases = [np.zeros((i,1)) for i in agent.net.shape[1:]]
    return pop


genetic = ng.Genetic([24,16,4],
                     400,
                     fitf3,
                     save='models/m/',
                     save_interval=5,
                     save_hist=True,
                     selection_args={
                         'top':5,
                         # 'rand':1,
                     },
                     cross_args={
                       # 'cross_biases':False
                     },
                     mutate_args={
                         # 'sel':0.9,
                         # 'rate':0.6,
                      },
                     opt_max=True, # do NOt change
                     activf=ng.sigmoid
                     )

# genetic.mutate = mutate

no=0
while True:
    genetic.step()
    no+=1