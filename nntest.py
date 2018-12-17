import random

import neuroga

genetic = neuroga.Genetic([24,12,4],
                          20,
                          lambda net:
                          (1-net.forward([random.random() for x in range(24)])[3])**2+
                          (0 - net.forward([random.random() for x in range(24)])[0]) ** 2+
                          (0 - net.forward([random.random() for x in range(24)])[1]) ** 2+
                          (0 - net.forward([random.random() for x in range(24)])[2]) ** 2,
                          save='models/testa/',
                          save_interval=500,
                          save_hist=True,
                          sel_top=0.4,
                          sel_rand=0.3,
                          sel_mut=0.9,
                          prob_cross=0.7,
                          prob_mut=0.9,
                          mut_range=(-20,20),
                          opt_max=False,
                          activf=neuroga.sigmoid
                          )
no=0
while True:
    genetic.step()
    no+=1