import random

# Đầu vào
KPIs = ['KPI1', 'KPI2', 'KPI3', 'KPI4']  # Danh sách KPI của công ty
tasks = {
    'KPI1': ['Task1', 'Task2'],
    'KPI2': ['Task3', 'Task4'],
    'KPI3': ['Task5'],
    'KPI4': ['Task6', 'Task7']
}

staff = {
    'Staff1': [0.8, 0.6, 0.7, 0.9],  # Mức độ phù hợp của nhân sự với các KPI
    'Staff2': [0.7, 0.9, 0.8, 0.6]
}

# Hàm mục tiêu
def objective_function(assignment):
    score = 0
    for staff_name, assigned_tasks in assignment.items():
        for task in assigned_tasks:
            kpi = next((k for k, v in tasks.items() if task in v), None)
            if kpi:
                kpi_index = KPIs.index(kpi)
                score += staff[staff_name][kpi_index]
    return score

# Hàm tạo cá thể (phân bổ Task cho nhân sự)
def create_individual():
    available_tasks = list(tasks.keys())
    individual = {}
    for staff_name in staff.keys():
        if not available_tasks:
            break  # Đảm bảo không chọn nhiệm vụ nếu danh sách rỗng
        individual[staff_name] = random.sample(available_tasks, 2)
        available_tasks = list(set(available_tasks) - set(individual[staff_name]))
    return individual

# Hàm lai ghép
def crossover(parent1, parent2):
    child = {}
    for staff_name in staff.keys():
        split_point = random.randint(0, 1)
        if staff_name in parent1 and staff_name in parent2:
            child[staff_name] = parent1[staff_name][:split_point] + parent2[staff_name][split_point:]
        elif staff_name in parent1:
            child[staff_name] = parent1[staff_name]
        elif staff_name in parent2:
            child[staff_name] = parent2[staff_name]
    return child

# Hàm đột biến
def mutate(individual):
    for staff_name in individual.keys():
        if random.random() < 0.2:  # xác suất đột biến
            available_tasks = list(set(tasks.keys()) - set(individual[staff_name]))
            task_to_mutate = random.choice(individual[staff_name])
            new_task = random.choice(available_tasks)
            individual[staff_name][individual[staff_name].index(task_to_mutate)] = new_task
    return individual

# Hàm chạy giải thuật di truyền
def genetic_algorithm(pop_size, generations):
    population = [create_individual() for _ in range(pop_size)]

    for _ in range(generations):
        population = sorted(population, key=lambda x: objective_function(x), reverse=True)

        # Lựa chọn cá thể tốt nhất để duy trì
        new_population = [population[0]]

        # Lựa chọn và lai ghép
        for _ in range(pop_size - 1):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    best_individual = max(population, key=lambda x: objective_function(x))
    return best_individual, objective_function(best_individual)

# Chạy giải thuật di truyền và hiển thị kết quả
best_solution, best_score = genetic_algorithm(pop_size=10, generations=100)
print("Phân bổ Tasks cho nhân sự để tối ưu hóa hoàn thành KPI của công ty:")
for staff_name, assigned_kpis in best_solution.items():
    assigned_tasks = [task for kpi in assigned_kpis for task in tasks[kpi]]
    print(f"{staff_name}: {assigned_tasks}")