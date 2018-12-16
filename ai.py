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

        return result

n = Network([3,2,1])
print(n.forward([1,0,1]))
# print(np.argmax(n.forward([0,0.5]), axis=0))
