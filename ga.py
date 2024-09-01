from population import *

population_size = 20
generations = 600

mutation_probability = 0.05
crossover_probability = 0.8


def average_fitness_for(individuals: list) -> float:
    return sum([individual.fitness for individual in individuals]) / len(individuals)


def crossover(father_chromosome: Chromosome, mother_chromosome: Chromosome):
    mask = to_bits_from(np.random.random())
    mask = Chromosome(mask)

    if np.random.uniform(0, 1) > crossover_probability:
        return father_chromosome, mother_chromosome

    son_chromosome = (father_chromosome & mask) | (mother_chromosome & ~mask)
    daughter_chromosome = (father_chromosome & ~mask) | (mother_chromosome & mask)

    return son_chromosome, daughter_chromosome


def select(individuals) -> Individual:  # Rank selection
    # Sort individuals by fitness (ascending order)
    sorted_individuals = sorted(individuals, key=lambda x: x.fitness)

    # Assign ranks: lowest fitness gets rank 1, highest gets rank N
    ranks = np.arange(1, len(sorted_individuals) + 1)

    # Calculate selection probabilities proportional to rank
    total_rank = np.sum(ranks)
    probabilities = ranks / total_rank

    # Select an individual based on the calculated probabilities
    selected_index = np.random.choice(np.arange(len(individuals)), p=probabilities)
    return sorted_individuals[selected_index]


def mutate(chromosome: Chromosome) -> Chromosome:
    if np.random.random() > mutation_probability:
        return chromosome

    index = np.random.randint(0, len(chromosome.gene))
    integer, fractional = chromosome.gene.split('.')

    # index = len(integer) - 1  # TEST CASE!

    if index < len(integer):
        integer = list(integer)
        integer[index] = '1' if integer[index] == '0' else '0'
    else:
        fractional = list(fractional)
        fractional[index - len(integer) - 1] = '1' if fractional[index - len(integer) - 1] == '0' else '0'

    integer = ''.join(integer)
    fractional = ''.join(fractional)

    return Chromosome(integer + '.' + fractional)

def find_fittest():
    uniform_population = uniform_population_by(population_size)
    parents = gather_individuals_by(uniform_population)

    people = dict()
    people[0] = parents

    for generation in range(1, generations):
        newborns = list()

        while len(newborns) < len(parents):
            mother, father = select(parents), select(parents)

            son_chromosome, daughter_chromosome = crossover(father.chromosome, mother.chromosome)

            son_chromosome = mutate(son_chromosome)
            daughter_chromosome = mutate(daughter_chromosome)

            son = Individual(son_chromosome, generation)
            daughter = Individual(daughter_chromosome, generation)

            newborns.append(son)
            newborns.append(daughter)

        people[generation] = newborns
        parents = newborns.copy()

    return people
