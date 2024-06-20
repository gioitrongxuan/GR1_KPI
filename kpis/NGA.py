import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Khởi tạo các hàm mục tiêu
def evaluate(individual):
    x = individual[0]
    return x**2, (x-2)**2

# Thiết lập môi trường DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", np.random.uniform, -5, 5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=-5, up=5, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=-5, up=5, eta=20.0, indpb=1.0)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

# Các thông số của giải thuật
population = toolbox.population(n=100)
ngen = 250
cxpb = 0.9
mutpb = 0.1

# Chạy giải thuật NSGA-II
algorithms.eaMuPlusLambda(population, toolbox, mu=100, lambda_=100, cxpb=cxpb, mutpb=mutpb, ngen=ngen,
                          stats=None, halloffame=None, verbose=False)

# Lấy kết quả
fronts = tools.emo.sortNondominated(population, len(population), first_front_only=True)
pareto_front = np.array([ind.fitness.values for ind in fronts[0]])

# Vẽ kết quả
plt.scatter(pareto_front[:, 0], pareto_front[:, 1], c="b")
plt.xlabel('f1(x) = x^2')
plt.ylabel('f2(x) = (x-2)^2')
plt.title('Pareto Front')
plt.show()