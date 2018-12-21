import neuroga
import snake


def fitf1(net:neuroga.Network):
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

def fitf2(net:neuroga.Network):
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


# model d is corrupted past a 2050
genetic = neuroga.Genetic([24,16,4],
                          200,
                          fitf3,
                          save='models/w/',
                          save_interval=5,
                          save_hist=True,
                          sel_top=0.1,
                          sel_rand=0.1,
                          sel_mut=0.8,
                          prob_cross=0.5,
                          prob_mut=0.8,
                          mut_range=(-10,10),
                          opt_max=True, # do NOt change
                          activf=neuroga.sigmoid)
no=0
while True:
    genetic.step()
    no+=1