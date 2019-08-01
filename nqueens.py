
#best_fit, epoch_num, visualization = solver.solve()
import collections
import random

class Solver_8_queens:
        
    def __init__(self, pop_size = 180, cross_prob=0.9, mut_prob=0.1):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        
  
    def solve(self, min_fitness=0.9, max_epochs=100):
        epoch_count = 0
        population = self.generate_population()
        fit_func_in = self.fit_func(population)

        while min(fit_func_in) != 0 and epoch_count<max_epochs:
            parent_pull = self.reproduction(fit_func_in, population)
            random.shuffle(parent_pull)
            parent_fit_func = self.fit_func(parent_pull)
            crossingover_out = self.crossingover(parent_pull)
            self.mutation(crossingover_out)
            fit_func_cross = self.fit_func(crossingover_out)
            population = self.reduction(parent_pull, crossingover_out, parent_fit_func, fit_func_cross)
            fit_func_in = self.fit_func(population)
            epoch_count += 1
        min_fit = min(fit_func_in)
        sum_fit = sum(fit_func_in)
        out_fit = 1 - min_fit/sum_fit
        out = ""
        for i in range(len(fit_func_in)):
            if fit_func_in[i] == min_fit:
                for index in range(0, len(population[i])):
                    for x in range(0, population[i][index]):
                        out += "+"
                    out += "Q"
                    for x in range(population[i][index], 7):
                        out += "+"
                    out += "\n"
                break

        return (out_fit, epoch_count, out)

    def generate_population(self):
        population = [[0] * 8 for i in range(self.pop_size)]
        for hromosom in population:
            for position in range(len(hromosom)):
                hromosom[position] = random.randrange(0, 8, 1)
        return population
        
    def fit_func(self, population):
        check = [0, 1, 2, 3, 4, 5, 6, 7]
        fit_func_result = [0]*self.pop_size
        for index, hromosom in enumerate(population):
            #Вертикаль
            counter = collections.Counter(hromosom)
            for i in check:
                if(counter[i] != 0):
                    fit_func_result[index] += counter[i] - 1
  
            # Диагонали
            for x in range(0,len(hromosom)):
                for y in range(x + 1, len(hromosom)):
                    if abs(x-y) == abs(hromosom[x]-hromosom[y]):
                        fit_func_result[index] += 1
  
        return fit_func_result


    def reproduction(self, fit_func, population):
        func_p = [0] * self.pop_size
        parent_pull = [[0] * 8 for i in range(self.pop_size)]
        sum_fit = sum(fit_func)
        for i in range(0, len(fit_func)):
            fit_func[i] = 1 - (fit_func[i]/sum_fit)
         
        for index, hromosom in enumerate(fit_func):
            func_p[index] = round(fit_func[index] / sum(fit_func) * 100)
  
        wheel = []
  
        for x in range(0, len(population)):
            for y in range(0, func_p[x]):
                wheel.append(x)
  
        for x in range(0, len(population)):
            parent_pull[x] = population[wheel[random.randrange(0, len(wheel), 1)]]
  
        return parent_pull

    def crossingover(self, parent_pull):
        crossingover_out = [[0] * 8 for i in range(self.pop_size)]
  
        for x in range(0, int(self.pop_size/ 2)):
            if random.randrange(0, 100, 1) < self.cross_prob * 100:
                first_parent = parent_pull[x]
                second_parent = parent_pull[int(self.pop_size/ 2 - 1 + x)]
  
                k_point = random.randrange(1, 8 - 1, 1)

                for index in range(k_point):
                    crossingover_out[x][index] = first_parent[index]
                    crossingover_out[int(self.pop_size/ 2 - 1 + x)][index] = second_parent[index]
                for index in range(k_point, 8):
                    crossingover_out[x][index] = second_parent[index]
                    crossingover_out[int(self.pop_size/ 2 - 1 + x)][index] = first_parent[index]             
  
        return crossingover_out

    
    def mutation(self, crossingover_out):
        rint = random.randrange(0, 8, 1)
        for hromosom in crossingover_out:
            if random.randrange(0, 100, 1) < self.mut_prob * 100:
                hromosom[rint] = random.randrange(0, 7, 1)

    def massivsorting(self, hromosom, key):
        lenkey = len(key)
        for index in range(lenkey):
            minkey = min(key[index:lenkey])
            #print(minkey)
            for i in range(index, lenkey):
                #print("::")
                if (key[i] == minkey):
                    #print(i)
                    remKey = key[i]
                    remH = hromosom[i]
                    key[i] = key[index]
                    hromosom[i] = hromosom[index]
                    key[index] = remKey
                    hromosom[index] = remH
                    break
        return hromosom
       
    def reduction(self, population, crossingover_out, fit_func_in, fit_func_cross):
        union_pop = []
        union_pop += population
        union_pop += crossingover_out
        union_fit = []
        union_fit += fit_func_in
        union_fit += fit_func_cross
        full_hromosoms = self.massivsorting(union_pop, union_fit)
        return full_hromosoms[:len(population)]
        
