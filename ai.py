import copy
import random

import numpy as np


def sigmoid(x):
    return 1/(1+np.exp(-x))


class Network:
    def __init__(self,
                 shape,
                 activation=sigmoid):

        if len(shape)<2:
            raise ValueError

        self.shape = shape
        self.activf = activation

        # init
        self.weights = [np.random.randn(j, i) for i, j in zip(
            self.shape[:-1], self.shape[1:])]
        self.biases = [np.random.randn(i, 1) for i in self.shape[1:]]

    def forward(self, data):
        """
        run input through network and get output
        """
        result = (np.array([data]).T if isinstance(data, list) else data)

        for w, b in zip(self.weights, self.biases):
            result = np.dot(w,result)
            result = result + b
            result = self.activf(result)

        return result.flatten()

class Agent:
    def __init__(self, net):
        self.net:Network = net
        self.fitness = 0

    def fitf(self):
        """
        fitness function
        """
        # return self.net.forward()
        # MSQ from XOR
        ret = (0-self.net.forward([0,0])[0])**2+\
              (1-self.net.forward([0,1])[0])**2+\
              (1-self.net.forward([1,0])[0])**2+\
              (0-self.net.forward([1,1])[0])**2
        ret = ret/4.0
        self.fitness=ret
        return ret

class Genetic:
    def __init__(self):
        self.population = []

        for i in range(20):
            self.population.append(Agent(Network([2,2,1])))

    def next_pop(self):
        next_pop = []
        for i in range(10):
            next_pop.append(copy.deepcopy(self.population[i]))
        for i in range(5):
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

        for a in range(10):
            mutant = random.choice(self.population)
            for i, biases in enumerate(mutant.net.biases):
                for j, bias in enumerate(mutant.net.biases[i]):
                    if random.random() < 0.5:
                        mutant.net.biases[i][j]+=random.uniform(-1,1)


g = Genetic()
for b in range(10000):
    g.step()
    if g.population[0].fitness<1e-100:
        print('wow')
# n = Network([2,2,1])
# print(n.biases)
# print(n.weights)
# print(n.forward([1,0,1]))
# print(np.argmax(n.forward([0,0.5]), axis=0))
