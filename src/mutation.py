import random

def multFlipBit(individual, prob):
    for i in range(len(individual)):
        if random.random() < prob:
            individual[i] = 1 - individual[i]
    return individual,