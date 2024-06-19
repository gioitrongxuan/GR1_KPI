import random
from deap import base, creator, tools, algorithms

# Giả sử chúng ta có 5 dự án và 3 nhân viên
NUM_PROJECTS = 5
NUM_EMPLOYEES = 3

# Thời gian và chi phí cho mỗi dự án
project_times = [10, 20, 30, 40, 50]
project_costs = [100, 200, 300, 400, 500]

# Năng suất làm việc của mỗi nhân viên (hệ số giảm thời gian hoàn thành dự án)
employee_productivity = [0.9, 0.8, 0.85]

# Tạo kiểu cá thể (individual) và quần thể (population)
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def evaluate(individual):
    """Hàm đánh giá cá thể."""
    total_time = 0
    total_cost = 0
    for i, employee in enumerate(individual):
        total_time += project_times[i] * employee_productivity[employee]
        total_cost += project_costs[i]
    return total_time, total_cost

def mutate(individual, indpb):
    """Hàm đột biến cá thể."""
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.randint(0, NUM_EMPLOYEES - 1)
    return individual,

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, NUM_EMPLOYEES - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=NUM_PROJECTS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", mutate, indpb=0.1)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evaluate)

def main():
    random.seed(42)
    population = toolbox.population(n=100)
    ngen = 50  # Số thế hệ
    cxpb = 0.7  # Xác suất lai ghép
    mutpb = 0.2  # Xác suất đột biến

    # Khởi tạo quần thể
    fits = list(map(toolbox.evaluate, population))
    for fit, ind in zip(fits, population):
        ind.fitness.values = fit

    # Lặp qua các thế hệ
    for gen in range(ngen):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Áp dụng lai ghép và đột biến
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Đánh giá lại các cá thể đã thay đổi
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fits = map(toolbox.evaluate, invalid_ind)
        for fit, ind in zip(fits, invalid_ind):
            ind.fitness.values = fit

        # Tạo quần thể mới
        population = toolbox.select(population + offspring, len(population))

    return population

if __name__ == "__main__":
    pop = main()
    # Trích xuất các giải pháp Pareto tối ưu
    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    for ind in pareto_front:
        print(f"Solution: {ind}, Fitness: {ind.fitness.values}")
