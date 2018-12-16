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
    steps_limit = 200

    i=0
    for i in range(steps_limit):
        if field.game_over: break
        output = net.forward(field.get_senses())
        # print(output)
        field.snake_dir = output.argmax()
        field.step()

    return field.eaten*100+i


genetic = neuroga.Genetic([24,4,4],
                          20,
                          fitf3,
                          save='models/f/',
                          save_interval=50,
                          save_hist=True,
                          sel_top=0.4,
                          sel_rand=0.3,
                          sel_mut=0.9,
                          prob_cross=0.7,
                          prob_mut=0.9,
                          mut_range=(-20,20),
                          opt_max=True,
                          activf=neuroga.sigmoid
                          )
no=0
while True:
    genetic.step()
    no+=1