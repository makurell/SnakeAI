import neuroga as ng
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
    return max(field.eaten*300, 2*field.eaten**3) - avg_eat_timing*50 + i**2

def fitf5(net):
    field = snake.Field()
    live_time = 200
    i = 0

    while live_time > 0:
        if field.game_over: break
        output = net.forward(field.get_senses())
        field.snake_dir = output.argmax()
        if field.step():
            live_time += 100
        live_time -= 1
        i += 1

    # avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    if field.eaten < 10:
        return i*i * 2**field.eaten
    else:
        return i*i * 2**10 * (field.eaten-9)

def fitf6(net):
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
    return max(100*field.eaten, 2**field.eaten) - avg_eat_timing*50 + max(200*i,i**2)

genetic = ng.Genetic([24,16,4],
                     400,
                     fitf5,
                     save='models/p/',
                     save_interval=5,
                     save_hist=True,
                     selection_args={
                         'top':5,
                     },
                     cross_args={
                       # 'cross_biases':False
                     },
                     mutate_args={
                         # 'sel':0.9,
                         # 'rate':0.6,
                      },
                     opt_max=True,
                     activf=ng.sigmoid
                     )

while True:
    genetic.step()
