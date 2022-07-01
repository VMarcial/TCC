# Referencias: 
#   - https://towardsdatascience.com/evolving-neural-networks-b24517bb3701
#   - https://towardsdatascience.com/reinforcement-learning-fda8ff535bb6


import random

from numpy.core.fromnumeric import clip
import world as w
import utils
import numpy as np
from numpy.random import choice


def generate(n = 1, center = [0,0]):
    temp = []
    for i in range(n):
        temp.append(ind(i, center[0], center[1], [60, 60, 60]))
    return temp


def evolve(population):
    rank = sorted(population, key= lambda X: X.utility, reverse=True)
    temp = []
    for i in rank:
        temp.append(i.utility)
    print(temp)
    limit = int((len(rank)/2))
    survivors = rank[0:limit]
    nextGen = survivors
    while len(nextGen) < len(rank):
        t = choice(survivors)
        t.mutate()
        nextGen.append(t)
    return nextGen, survivors[0]
        

class ind():
    def __init__(self, cpf, posX, posY, dimensions, name = None, age = 0, velocity = 10, productivity = 10, utilfun = None, cloth = 0 , food = 25, state = "ALIVE", output = "softmax"):
        
        # Caracteristicas de estado do indivíduo
        self.state = state
        self.cpf = cpf
        self.name = name
        self.age = age
        self.velocity = velocity
        self.productivity = productivity
        self.utilfun = utilfun
        self.utility = 0
        self.posX = posX
        self.posY = posY
        self.food = food
        self.cloth = cloth
        self.range = 5
        self.output = self._activate(output)
        self.vision = []
        self.layers = []
        self.biases = []
        self.dimensions = [803] + dimensions + [7] #dimensões da rede neural, primeira e ultima são definidas pelo tipo do problema
        # inputs são comida, cloth, visão(matrix 5x5), utilidade atual ou seja 28
        # outputs são movimentar para cima[0], baixo[1], direita[2], esquerda[3], consumir comida[4], consumir cloth[5], trocar[6] ou seja 7


        if name == None:
            self.name = self.randomName()
        
        else:
            self.name = name
        
        if utilfun == None:
            self.utilfun = self.randomUtilfun()
        
        else:
            self.utilfun = utilfun

        #Criando a Rede neural do indivíduo

        for i in range(len(self.dimensions) - 1):
            shape = (self.dimensions[i], self.dimensions[i+1])
            std = np.sqrt(2/sum(shape))
            layer = np.random.normal(0, std, shape)
            bias = np.random.normal(0, std, (1, self.dimensions[i+1]))
            self.layers.append(layer)
            self.biases.append(bias)



    def randomName(self):
        firstName = ["Vinicius", "Victor", "Marcelo"]
        lastName = ["Pudim", "Doce de Leite", "Leite Ninho"]

        rFirst = firstName[random.randint(0, len(firstName) - 1 )]
        rLast = lastName[random.randint(0, len(lastName) - 1)]

        return rFirst + " " + rLast


    def randomUtilfun(self, thetaSelection = "limited", thetas = None):
        #TODO tipos puras: log, CES, Cobb Douglas, Substitutos Perfeitos
        #return lambda X: 1*X[0] + 2*X[1]
        #return lambda X: X[0]**1/2 + X[1]**1/2
        return lambda X: np.log(X[0]) + np.log(X[1])

    
    def _activate(self, output:str):
        if output == "softmax":
            return lambda X : np.exp(X) / np.sum(np.exp(X), axis=1).reshape(-1, 1)
        elif output == 'sigmoid':
            return lambda X : (1 / (1 + np.exp(-X)))
        elif output == 'linear':
            return lambda X : X
    

    def predict(self, X):
        for index, (layer, bias) in enumerate(zip(self.layers, self.biases)):
            X = X @ layer + np.ones((X.shape[0],1)) @ bias
            if index == len(self.layers) -1:
                X = self.output(X)
            else:
                X = np.clip(X, 0, np.inf)
        return X
    

    def predict_choice(self, X):
        output = self.predict(X)[0].tolist()
        decisions = []
        for i in output:
            if i > 0.5:
                decisions.append((1,i))
            else:
                decisions.append((0,i))
        return decisions


    def updateVision(self, world):
        self.vision = world.vision(self.posX, self.posY)
    

    def getX(self):
        temp = [self.food, self.cloth, self.utility]
        for i in self.vision:
            for j in i:
                temp.append(j)
        temp = np.array(temp)
        return temp


    def action(self, world, tax = False):
        self.updateVision(world)
        X = self.getX()
        choices = self.predict_choice(X)
        self.movement(choices = choices)
        self.collect(world)
        self.consume(choices = choices, tax = tax)
        
        
    def mutate(self, stdrate = 0.3):
        for i in range(len(self.layers)):
            self.layers[i] += np.random.normal(0, stdrate, self.layers[i].shape)
            self.biases[i] += np.random.normal(0, stdrate, self.biases[i].shape)


    def movement(self, randomize = True, choices = []):
        if randomize:
            tempX = self.posX + random.randint(-1,1)
            tempY = self.posY + random.randint(-1,1)
        else:
            temp = choices
            tempX, tempY = temp[0][0] - temp[1][0], temp[2][0] - temp[3][0]

        if tempX > 0 and tempX < 20:
            self.posX = tempX
        if tempY > 0 and tempY < 20:
            self.posY = tempY


    def consume(self, choices, punish = False, tax = False):
        if not tax:
            foodConsumado = 0
            clothConsumado = 0

            if self.food >= choices[4][1]:
                self.food -= choices[4][1]
                foodConsumado = choices[4][1]

            elif self.food > 0:
                self.food -= 1
                foodConsumado = 1
                if punish:#TODO colocar alguma punição proporcional
                    pass
            else:
                self.state = "DEAD"
            if choices[5][0]:
                if self.cloth >= choices[4][1]:
                    self.cloth -= choices[4][1]
                    clothConsumado = choices[4][1]

                elif self.cloth > 0:
                    self.cloth -= 1
                    clothConsumado = 1
                    if punish:#TODO colocar alguma punição proporcional
                        pass

                elif punish:
                    pass #TODO colocar alguma punição proporcional

        else:
            foodConsumado = 0
            clothConsumado = 0

            if self.food >= choices[4][1]:
                self.food -= choices[4][1]
                foodConsumado = choices[4][1]

            elif self.food > 0:
                self.food -= 1
                foodConsumado = 1 * 0.9
                if punish:#TODO colocar alguma punição proporcional
                    pass
            else:
                self.state = "DEAD"
            if choices[5][0]:
                if self.cloth >= choices[4][1]:
                    self.cloth -= choices[4][1]
                    clothConsumado = choices[4][1]

                elif self.cloth > 0:
                    self.cloth -= 1
                    clothConsumado = 1 * 0.9
                    if punish:#TODO colocar alguma punição proporcional
                        pass

                elif punish:
                    pass #TODO colocar alguma punição proporcional
        final = [foodConsumado, clothConsumado]
        self.utility += self.utilfun(final)

    def collect(self, world):
        target = world.grid[self.posX][self.posY]
        if isinstance(target, w.food):
            self.food += self.productivity
        elif isinstance(target, w.cloth):
            self.cloth += self.productivity


    def inRange(self):
        # TODO Mudar isso
        if self.target == None:
            return False
        elif self.range < utils.norm([self.posX, self.posY], self.target):
            return True
        else:
            return False 

