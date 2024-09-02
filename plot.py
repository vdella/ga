import matplotlib.pyplot as plt
from ga import find_fittest, average_fitness_for
from population import x_min, x_max
import numpy as np


def plot_fitness():
    fittest: dict = find_fittest()

    generation_avg_fitness: dict = {}

    for generation, individuals in fittest.items():
        generation_avg_fitness[generation] = average_fitness_for(individuals)

    x = list(generation_avg_fitness.keys())
    y = list(generation_avg_fitness.values())

    plt.plot(x, y)
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.title('Genetic Algorithm')
    plt.show()


def plot_chromosomes_from(generation):
    x = np.arange(x_min, x_max, 0.01)
    y = x + abs(np.sin(32 * x))

    plt.plot(x, y)

    chromosomes = np.array([individual.x for individual in generation])
    fitness = chromosomes + abs(np.sin(32 * chromosomes))

    plt.scatter(chromosomes, fitness, color='red')
    plt.xlabel('Chromosomes')
    plt.ylabel('Fitness functional interval')
    plt.title('Genetic Algorithm')
    plt.show()


if __name__ == '__main__':
    a = find_fittest()

    plot_chromosomes_from(a[0])

    plot_chromosomes_from(a[10])

    plot_chromosomes_from(a[599])

