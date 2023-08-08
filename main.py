import string
import random


class Individual:
    def __init__(self, chromosome_size):
        # generate random chromosome of given length
        self.chromosome = [random.choice(StringEvolution.all_genes) for _ in range(chromosome_size)]
        self.chromosome_size = chromosome_size


class StringEvolution:
    # valid genes
    all_genes = string.ascii_letters + string.digits + string.punctuation + " "

    def __init__(self, population_size, goal):
        # validate user input
        if not set(goal) <= set(self.all_genes):
            raise ValueError("Goal contains forbidden characters")

        self.goal = goal
        self.generation = 0
        self.population = []
        self.chromosome_size = len(goal)
        self.population_size = population_size

    # fitness equals to number of common characters of chromosome and goal string
    def __fitness(self, individual):
        fitness = 0
        for cnt in range(self.chromosome_size):
            if self.goal[cnt] == individual.chromosome[cnt]:
                fitness += 1
        return fitness

    # bit flip mutation
    def __mutate(self, individual):
        for i in range(self.chromosome_size):
            rand = random.random()
            if rand < 0.1:
                individual.chromosome[i] = random.choice(StringEvolution.all_genes)

    def __uniform_crossover(self, i1, i2):
        offspring = Individual(self.chromosome_size)
        for i in range(self.chromosome_size):
            rand = random.random()
            offspring.chromosome[i] = i1.chromosome[i] if rand <= 0.5 else i2.chromosome[i]
        return offspring

    def __mate(self):
        selected = self.__roulette_wheel_selection()
        offsprings = []

        for individual in selected:
            # mates with a randomly chosen individual
            off = self.__uniform_crossover(individual, random.choice(selected))
            # mutation can occur
            self.__mutate(off)
            offsprings.append(off)
            if len(offsprings) == self.population_size:
                break

        return offsprings

    # selection is directly proportional to fitness
    def __roulette_wheel_selection(self):
        selected = []
        for individual in self.population:
            probability = self.__fitness(individual) / self.chromosome_size
            rand = random.random()
            if rand <= probability:
                selected.append(individual)
        return selected

    # replace some of the old generation with new offsprings
    def __replacement(self, offsprings):
        for i in range(self.population_size - len(offsprings)):
            offsprings.append(self.population[i])
        self.population = offsprings
        self.population.sort(key=self.__fitness, reverse=True)

    # create a new population of individuals with randomized chromosomes
    def __init_population(self):
        for _ in range(self.population_size):
            self.population.append(Individual(self.chromosome_size))

    # print info of the current generation
    def __print_round(self, line_end):
        chromosome = "".join(self.population[0].chromosome)
        fitness    = self.__fitness(self.population[0])
        data       = (self.generation, chromosome, fitness)
        print('Generation: %s     Choromosome: %s     Best fitness: %s' % data, end=line_end)
    
    def __print_goal(self):
        print(f'-' * (self.chromosome_size + 24))
        print(f'| Goal: {self.goal} | Fitness: {self.chromosome_size} |')
        print(f'-' * (self.chromosome_size + 24))

    # start evolving
    def start(self):
        self.__init_population()
        self.population.sort(key=self.__fitness, reverse=True)
        self.__print_goal()

        while not self.__fitness(self.population[0]) == self.chromosome_size:
            offsprings = self.__mate()
            self.__replacement(offsprings)
            self.generation += 1
            self.__print_round('\r')
        self.__print_round('\n')


# driver program
if __name__ == '__main__':
    StringEvolution(1000, "Artificial intelligence is very intelligent.").start()
