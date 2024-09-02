from numeric import to_float_from
import numpy as np

from numeric import to_bits_from

x_min, x_max = 0, np.pi


class Chromosome:
    gene: str

    def __init__(self, gene):
        self.gene = gene
        self.integer, self.fractional = gene.split('.') if '.' in gene else (gene, '0')

    def __repr__(self):
        return self.gene

    def __and__(self, other):
        integer, fractional = self.gene.split('.')

        integer = bin(int(integer, 2) & int(other.integer, 2))[2:]
        fractional = bin(int(fractional, 2) & int(other.fractional, 2))[2:]

        return Chromosome(integer + '.' + fractional)

    def __or__(self, other):
        integer, fractional = self.gene.split('.')

        integer = bin(int(integer, 2) | int(other.integer, 2))[2:]
        fractional = bin(int(fractional, 2) | int(other.fractional, 2))[2:]

        return Chromosome(integer + '.' + fractional)

    def __invert__(self):
        integer, fractional = self.gene.split('.')

        integer = ['1' if bit == '0' else '0'  for bit in integer]
        integer = ''.join(integer)

        fractional = ['1' if bit == '0' else '0' for bit in fractional]
        fractional = ''.join(fractional)

        return Chromosome(integer + '.' + fractional)


class Individual:

    def __init__(self, chromosome, generation=0):
        self.x = to_float_from(chromosome.gene)
        self.fitness = fitness_by(self.x)
        self.chromosome = chromosome
        self.generation = generation


def fitness_by(x):
    return x + abs(np.sin(32*x))


def uniform_population_by(size):
    return np.random.uniform(x_min, x_max, size)


def gather_individuals_by(uniform_population):
    individuals = list()

    for value in uniform_population:
        chromosome = Chromosome(to_bits_from(value))
        individual = Individual(chromosome)
        individuals.append(individual)

    return individuals


if __name__ == '__main__':
    pi = 3.14
    result = to_bits_from(pi)

    print(Chromosome(result))
    print(~Chromosome(result))