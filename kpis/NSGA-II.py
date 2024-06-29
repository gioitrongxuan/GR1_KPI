import random
import numpy as np

# Dữ liệu thời gian công việc và độ phức tạp
work_times = [4, 2, 3, 6, 5, 1, 8, 7, 3, 4]
work_complexities = [5, 3, 4, 7, 6, 2, 8, 7, 3, 4]
num_workers = 5

# Năng lực của các nhân viên
worker_capabilities = [6, 5, 8, 7, 4]

# Khởi tạo quần thể
def init_population(pop_size, num_jobs, num_workers):
    return [np.random.randint(0, num_workers, num_jobs).tolist() for _ in range(pop_size)]

# Hàm đánh giá cho từng cá thể
def evaluate(individual):
    workloads = [0] * num_workers
    suitability_score = 0
    for i, worker in enumerate(individual):
        workloads[worker] += work_times[i]
        suitability_score += abs(worker_capabilities[worker] - work_complexities[i])
    
    time_completed = sum(workloads)
    workload_balance = max(workloads) - min(workloads)
    return [time_completed, workload_balance, suitability_score]

# Hàm không trội và khoảng cách đông đúc
def non_dominated_sorting(pop):
    fronts = [[]]
    domination_count = [0] * len(pop)
    dominated_solutions = [[] for _ in range(len(pop))]
    rank = [0] * len(pop)
    
    for p in range(len(pop)):
        for q in range(len(pop)):
            if all(p_f <= q_f for p_f, q_f in zip(pop[p][1], pop[q][1])) and any(p_f < q_f for p_f, q_f in zip(pop[p][1], pop[q][1])):
                dominated_solutions[p].append(q)
            elif all(q_f <= p_f for q_f, p_f in zip(pop[q][1], pop[p][1])) and any(q_f < p_f for q_f, p_f in zip(pop[q][1], pop[p][1])):
                domination_count[p] += 1
        if domination_count[p] == 0:
            rank[p] = 0
            fronts[0].append(p)
    
    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_count[q] -= 1
                if domination_count[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    
    fronts.pop()
    return fronts

def crowding_distance(front, pop):
    distance = [0] * len(front)
    for m in range(3):  # 3 mục tiêu
        front = sorted(front, key=lambda x: pop[x][1][m])
        distance[0] = distance[-1] = float('inf')
        for i in range(1, len(front) - 1):
            distance[i] += (pop[front[i + 1]][1][m] - pop[front[i - 1]][1][m]) / (max(pop[front])[1][m] - min(pop[front])[1][m])
    return distance

# Chọn lọc NSGA-II
def selection(pop, fronts, pop_size):
    new_pop = []
    for front in fronts:
        if len(new_pop) + len(front) > pop_size:
            distance = crowding_distance(front, pop)
            front = sorted(front, key=lambda x: distance[front.index(x)], reverse=True)
            new_pop.extend(front[:pop_size - len(new_pop)])
            break
        new_pop.extend(front)
    return new_pop

# Lai ghép và Đột biến
def crossover_and_mutate(parents, num_jobs, num_workers, crossover_prob=0.7, mutation_prob=0.2):
    offspring = []
    for i in range(0, len(parents), 2):
        parent1, parent2 = parents[i], parents[i + 1]
        if random.random() < crossover_prob:
            point = random.randint(1, num_jobs - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
        else:
            child1, child2 = parent1, parent2
        
        if random.random() < mutation_prob:
            child1[random.randint(0, num_jobs - 1)] = random.randint(0, num_workers - 1)
        if random.random() < mutation_prob:
            child2[random.randint(0, num_jobs - 1)] = random.randint(0, num_workers - 1)
        
        offspring.append(child1)
        offspring.append(child2)
    return offspring

# Khởi tạo thông số
pop_size = 100
num_jobs = len(work_times)
num_generations = 50

# Khởi tạo quần thể ban đầu
population = init_population(pop_size, num_jobs, num_workers)
evaluated_pop = [(ind, evaluate(ind)) for ind in population]

# Vòng lặp tiến hóa
for gen in range(num_generations):
    fronts = non_dominated_sorting(evaluated_pop)
    selected_indices = selection(evaluated_pop, fronts, pop_size)
    parents = [evaluated_pop[i][0] for i in selected_indices]
    offspring = crossover_and_mutate(parents, num_jobs, num_workers)
    evaluated_pop = [(ind, evaluate(ind)) for ind in offspring]

# Kết quả
best_individual = sorted(evaluated_pop, key=lambda x: x[1])[0]
print("Best individual:", best_individual[0])
print("Best individual fitness:", best_individual[1])

# Phân tích kết quả
best_workloads = [0] * num_workers
for i, worker in enumerate(best_individual[0]):
    best_workloads[worker] += work_times[i]

print("\nBest workloads per worker:")
for i in range(num_workers):
    print(f"Worker {i + 1}: {best_workloads[i]} hours")

# In chi tiết phân công công việc cho nhân viên
for i in range(num_workers):
    worker_tasks = [j + 1 for j in range(len(best_individual[0])) if best_individual[0][j] == i]
    print(f"Worker {i + 1} tasks: {worker_tasks}")
