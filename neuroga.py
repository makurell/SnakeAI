import copy
import math
import random
import numpy as np


def sigmoid(x):
    return 1/(1+np.exp(-x))


class Network:
    def __init__(self, shape, activation=sigmoid):
        """
        :param shape: list of num neurons in each layer
        :param activation: activation function
        """

        if len(shape)<2:
            raise ValueError

        self.shape = shape
        self.activf = activation

        # init (random inital weights/biases)
        self.weights = [np.random.randn(j, i) for i, j in zip(
            self.shape[:-1], self.shape[1:])] # matrix for each layer-gap
        self.biases = [np.random.randn(i, 1) for i in self.shape[1:]] # single column matrix for each layer-gap

    def forward(self, data):
        """
        run input through network and get output
        :param data: list of inputs
        :return: list of outputs
        """
        result = (np.array([data]).T if isinstance(data, list) else data)

        for w, b in zip(self.weights, self.biases):
            result = self.activf(np.dot(w,result) + b)

        return result.flatten()

class Agent:
    """
    A member of a `Genetic` class' population
    """
    def __init__(self, net:Network, fitf):
        """
        :param net: underlying Neural Network
        :param fitf: fitness function. Network will be passed as parameter.
        """
        self.net:Network = net
        self.__fitf = fitf
        self.fitness = 0

    def evaluate(self):
        """
        update fitness by executing fitness function
        """
        fitness = self.__fitf(self.net)
        self.fitness = fitness
        return fitness

class Genetic:
    def __init__(self,
                 shape,
                 pop_size,
                 fitf,
                 sel_top=0.5,
                 sel_rand=0.25,
                 sel_mut=0.5,
                 prob_cross=0.5,
                 prob_mut=0.5,
                 mut_range=(-1,1),
                 activf=sigmoid,
                 opt_max=True,
                 parallelise=True):
        """
        Evolve Neural Networks to optimise a given function ('fitness function')
        :param shape: shape of Neural Networks (list of num neurons in each layer)
        :param pop_size: number of NNs in population
        :param fitf: fitness function. Corresponding NN will be passed as parameter. Should output fitness.
        :param sel_top: Num top agents to be selected for the next generation per step. Fraction of pop_size.
        :param sel_rand: Num agents to be randomly selected for the next generation per step. Fraction of pop_size
        :param sel_mut: Num agents to be mutated per step. Fraction of pop_size
        :param prob_cross: During crossing, prob for a given gene to be crossed. 0-1 (Cross frequency)
        :param prob_mut: During mutation, prob for a given gene to be mutated. 0-1 (Mutation frequency)
        :param mut_range: (Tuple) Mutation range (Mutation amount)
        :param activf: activation function for underlying NNs (default: sigmoid)
        :param opt_max: whether to maximise fitf or to minimise it
        :param parallelise: whether to parallelise (multithread) evaluation of NNs (execution of fitfs)
        """
        # todo saving to file

        self.shape = shape
        self.pop_size = pop_size
        self.fitf = fitf
        self.sel_top = sel_top
        self.sel_rand = sel_rand
        self.sel_mut = sel_mut
        self.prob_cross = prob_cross
        self.prob_mut = prob_mut
        self.mut_range = mut_range
        self.activf = activf
        self.opt_max = opt_max
        self.parallelise = parallelise

        self.population = []

        # init population
        for i in range(self.pop_size):
            self.population.append(Agent(
                Network(self.shape,self.activf),
                self.fitf))

    def next_pop(self):
        """
        select agents to survive to next generation
        :return:
        """
        next_pop = []

        # select specified no of top agents
        for i in range(math.floor(self.pop_size*self.sel_top)):
            next_pop.append(copy.deepcopy(self.population[i]))

        # randomly select specified no of agents
        for i in range(math.floor(self.pop_size*self.sel_rand)):
            next_pop.append(copy.deepcopy(random.choice(self.population)))

        return next_pop

    def cross(self, parent1, parent2):
        # create merged
        merged = copy.deepcopy(parent1)

        for i, weights in enumerate(parent2.net.weights):
            for j, weight in enumerate(parent2.net.weights[i]):
                if random.random() < 0.3:
                    merged.net.weights[i][j] = weight
        return merged

    def step(self):
        self.population.sort(key=lambda x: x.fitf(), reverse=False)
        print('Top fit: '+str(self.population[0].fitness))

        self.population=self.next_pop()

        for a in range(5):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population) # fixme may choose same twice
            self.population.insert(0,self.cross(parent1,parent2))

        for a in range(10):
            mutant = random.choice(self.population)
            for i, weights in enumerate(mutant.net.weights):
                for j, weight in enumerate(mutant.net.weights[i]):
                    if random.random() < 0.5:
                        mutant.net.weights[i][j]+=random.uniform(-1,1)

        # for a in range(10):
        #     mutant = random.choice(self.population)
        #     for i, biases in enumerate(mutant.net.biases):
        #         for j, bias in enumerate(mutant.net.biases[i]):
        #             if random.random() < 0.5:
        #                 mutant.net.biases[i][j]+=random.uniform(-1,1)


g = Genetic()
for b in range(10000):
    g.step()
    # if g.population[0].fitness<1e-100:
    #     # print('wow')
    #     inpts = [[0, 0], [0, 1], [1, 0], [1, 1]]
    #     for inpt in inpts:
    #         outpt = g.population[0].net.forward(inpt)[0]
    #         print(str(inpt) + '--> ' + str(outpt))
    #     exit()
# n = Network([2,2,1])
# print(n.biases)
# print(n.weights)
# print(n.forward([1,0,1]))
# print(np.argmax(n.forward([0,0.5]), axis=0))
