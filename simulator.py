import random
import numpy as np
import sim, world
import matplotlib.pyplot as plt

def simulate(generations = 10, individuals = 20, timelimit = 1000, size = 800):
    n = 0
    best = []
    pop = sim.generate(n = individuals)
    gamemap = world.world(size= size)
    gamemap.generate_food()
    gamemap.generate_cloth()
    alive = 1
    while n < generations:
        print("geração:", n)
        while gamemap.time < timelimit:
            for ind in pop:
                if ind.state == "DEAD":
                    pass
                else:
                    ind.action(gamemap) 
            gamemap.time += 1

        gamemap = world.world(size= size)
        gamemap.time = 0
        gamemap.generate_food()
        gamemap.generate_cloth()
        pop,x = sim.evolve(population=pop)
        
        print("utlidade máxima:", x.utility)
        best.append(x)

        n += 1

    print("ACABOU!!!!")
    temp1  = []
    for i in best:
        temp1.append(i.utility)
    
    y = np.arange(0, len(temp1))
    print(len(temp1), len(y))
    plt.plot(y, temp1)

###
    n = 0
    best = []
    pop = sim.generate(n = individuals)
    gamemap = world.world(size= size)
    gamemap.generate_food()
    gamemap.generate_cloth()
    alive = 1
    while n < generations:
        print("geração:", n)
        while gamemap.time < timelimit:
            for ind in pop:
                if ind.state == "DEAD":
                    pass
                else:
                    ind.action(gamemap, tax = True) 
            gamemap.time += 1

        gamemap = world.world(size= size)
        gamemap.time = 0
        gamemap.generate_food()
        gamemap.generate_cloth()
        pop,x = sim.evolve(population=pop)
        
        print("utlidade máxima:", x.utility)
        best.append(x)

        n += 1

    print("ACABOU!!!!")
    temp2  = []
    for i in best:
        temp2.append(i.utility)
    
    razao = temp1[-1]/temp2[-1]
    print(razao)

    t = np.arange(0, len(temp2))
    print(len(temp2), len(y))
    plt.plot(t, temp2)


    plt.show()

    import pdb
    pdb.set_trace()


def logAction():
    pass


simulate(size = 20, individuals= 10)

