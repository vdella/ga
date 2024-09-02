from population import *

population_size = 20
generations = 600

mutation_probability = 0.2
crossover_probability = 0.8


def average_fitness_for(individuals: list) -> float:
    return sum([individual.fitness for individual in individuals]) / len(individuals)


def crossover(father_chromosome: Chromosome, mother_chromosome: Chromosome):
    # Randomly decide a crossover point within the gene string.
    crossover_point = np.random.randint(1, len(father_chromosome.gene) - 1)

    # Combine the parents' genes at the crossover point.
    son_gene = father_chromosome.gene[:crossover_point] + mother_chromosome.gene[crossover_point:]
    daughter_gene = mother_chromosome.gene[:crossover_point] + father_chromosome.gene[crossover_point:]

    # We might get '..' while crossing over, so we need to replace it with '.'.
    son_gene = son_gene.replace('..', '.')
    daughter_gene = daughter_gene.replace('..', '.')

    print(son_gene, daughter_gene)

    son_chromosome = Chromosome(son_gene)
    daughter_chromosome = Chromosome(daughter_gene)

    son_value = to_float_from(son_chromosome.gene)
    daughter_value = to_float_from(daughter_chromosome.gene)

    # Ensure the offspring values are within the valid range [x_min, x_max]
    if not (x_min <= son_value <= x_max):
        son_value = np.clip(son_value, x_min, x_max)
        son_chromosome = Chromosome(to_bits_from(son_value))

    if not (x_min <= daughter_value <= x_max):
        daughter_value = np.clip(daughter_value, x_min, x_max)
        daughter_chromosome = Chromosome(to_bits_from(daughter_value))

    return son_chromosome, daughter_chromosome


def select(individuals) -> Individual:  # Rank selection
    # Sort individuals by fitness (ascending order)
    sorted_individuals = sorted(individuals, key=lambda i: i.fitness)

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

    if index < len(integer):
        integer = list(integer)
        integer[index] = '1' if integer[index] == '0' else '0'
    else:
        fractional = list(fractional)
        fractional[index - len(integer) - 1] = '1' if fractional[index - len(integer) - 1] == '0' else '0'

    integer = ''.join(integer)
    fractional = ''.join(fractional)

    genes = Chromosome(integer + '.' + fractional)
    float_gene = to_float_from(genes.gene)

    # Ensure the mutated value is within the valid range [x_min, x_max].
    if not (x_min <= float_gene <= x_max):
        son_value = np.clip(float_gene, x_min, x_max)
        genes = Chromosome(to_bits_from(son_value))

    return genes


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


if __name__ == '__main__':
    all_people = find_fittest()

    # for citizens in all_people:
    #     print(f'Generation {citizens}:')
    #     for individual in all_people[citizens]:
    #         print(f'x: {individual.x}, fitness: {individual.fitness}')
    #     print()
