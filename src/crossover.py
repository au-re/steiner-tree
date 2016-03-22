import random

def onePointCrossover(parent1, parent2):
    size = len(parent1)
    point = random.randint(0, size - 1)
    parent1[point:], parent2[point:] = parent2[point:], parent1[point:]
    return parent1, parent2

def twoPointsCrossover(parent1, parent2):
    size = len(parent1)
    point1 = random.randint(0, size)
    point2 = random.randint(0, size - 1)
    if point2 >= point1:
        point2 += 1
    else:
        point1, point2 = point2, point1
    parent1[point1:point2], parent2[point1:point2] \
        = parent2[point1:point2], parent1[point1:point2]
    return parent1, parent2

def probabilityCrossover(parent1, parent2):
    prob = 0
    size = len(parent1) 
    for i in range(size):
        if random.random() < prob:
            parent1[i], parent2[i] = parent2[i], parent1[i]
    return parent1, parent2