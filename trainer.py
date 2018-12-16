import neuroga
import snake


def fitf1(net:neuroga.Network):
    field = snake.Field()

    steps_limit = 1000
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

    steps_limit = 1000

    sum_dists = 0

    i=0
    for i in range(steps_limit):
        if not field.game_over:
            output = net.forward(field.get_senses()).argmax()
            field.snake_dir = output
            field.step()

            sum_dists+=field.snake_arr[-1].dist(field.food_pos)
        else:
            break

    avg_eat_timing = sum(field.eat_timings) / float(len(field.eat_timings))
    return avg_eat_timing + (max(steps_limit-i,0)) - (field.eaten*10) + sum_dists/float(i)



genetic = neuroga.Genetic([24,24,4],
                          100,
                          fitf2,
                          save='models/a/',
                          save_interval=2,
                          save_hist=True,
                          sel_top=0.3,
                          sel_rand=0.5,
                          sel_mut=0.8,
                          prob_cross=0.6,
                          prob_mut=0.6,
                          mut_range=(-5,5),
                          opt_max=False
                          )
while True:
    genetic.step()