import random
import numpy as np
from numpy.matrixlib import matrix

class world():

    def __init__(self, grid = [], size = 800):
        self.grid = [[0 for x in range(size)] for y in range(size)]
        self.matrix = np.matrix(self.grid)
        self.time = 0


    def _updateMatrix(self):
        self.matrix = np.matrix(self.grid)


    def vision(self, posX, posY, sight = 5):
        

        tclothes = self.matrix.tolist()
        tfoods = self.matrix.tolist()
        clothes = []
        foods = []


        for j in tclothes:
            for i in j:
                if isinstance(i, cloth):
                    clothes.append(1)
                else:
                    clothes.append(0)


                

        for j in tfoods:
            for i in j:
                if isinstance(i, food):
                    foods.append(1)
                else:
                    foods.append(0)

        return clothes, foods

    def _vision(self, posX, posY, sight = 5):

        # -



        highX = int(posX+sight)
        lowX = int(posX-sight)
        highY = int(posY+sight)
        lowY = int(posY-sight)

        overlX = overlY = 0
        overhX = overhY = 2 * sight

        if highX > 799:
            overhX = highX - 799
            highX = 799
        elif lowX < 0:
            overlX = lowX
            lowX = 0
        if highY > 799:
            overhY = highY - 799
            highY = 799
        elif lowY < 0:  
            overlY = lowY
            lowY = 0

        temp = []
        temp = np.full((sight, sight), -1)
        tempworld = self.matrix[lowX:highX, lowY:highY]
        print("x", posX, "y", posY)
        print("lowX", lowX, overlX, "highX", highX, overhX)
        print("lowY", lowY, overlY, "highY", highY, overhY)
        print("temp", temp)
        print("world", tempworld)
        temp[overlX:overhX, overlY:overhY] = tempworld
        tclothes = tfoods = temp.tolist()
        clothes = foods = []

        for j in tclothes:
            t = []
            for i in j:
                if isinstance(i, cloth):
                    t.append(1)
                else:
                    t.append(0)
                clothes.append(t)
                

        for j in tfoods:
            t = []
            for i in j:
                if isinstance(i, food):
                    t.append(1)
                else:
                    t.append(0)
                clothes.append(t)

        return clothes, foods


    def generate_food(self):
        n = random.randint(1, 3)
        for i in range(n):
            done = False
            while not done:
                tempX = random.randint(0, 19)
                tempY = random.randint(0, 19)
                if self.grid[tempX][tempY] == 0:
                    self.grid[tempX][tempY] = 1
                    done = True
    

    def generate_cloth(self):
        n = random.randint(1, 3)
        for i in range(n):
            done = False
            while not done:
                tempX = random.randint(0, 19)
                tempY = random.randint(0, 19)
                if self.grid[tempX][tempY] == 0:
                    self.grid[tempX][tempY] = 1
                    done = True
                    


class food():

    def __init__(self, posX, posY, size = 20):
        self.posX = posX
        self.posY = posY
        self.size = size


class cloth():
    def __init__(self, posX, posY, size = 20):
        self.posX = posX
        self.posY = posY
        self.size = size