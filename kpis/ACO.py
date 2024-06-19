import random
import numpy as np

num_ants = 100  
num_iterations = 100  
alpha = 1 
beta = 1 
rho = 0.1  
pheromone_max = 10  
pheromone_min = 0.1 

tasks = {
    "A": {
        "weights": [0.2, 0.3, 0.5],
        "resources": [1, 1, 1],
        "scores": [[0.8, 0.3, 0.4], [0.4, 0.4, 0.5], [0.7, 0.9, 0.0]],
    },
    "B": {
        "weights": [0.2, 0.1, 0.4, 0.2, 0.1],
        "resources": [1, 1, 1, 1, 1],
        "scores": [[0.6, 0.5, 0.6], [0.3, 0.3, 0.3], [0.9, 0.7, 0.8], [0.5, 0.5, 0.5], [0.6, 0.6, 0.4]],
    },
    "C": {
        "weights": [0.2, 0.3, 0.1, 0.4],
        "resources": [1, 1, 1, 1],
        "scores": [[0.9, 0.6, 0.68], [0.3, 0.3, 0.55], [0.1, 0.1, 0.1], [0.8, 0.45, 0.12]],
    },
}

employees = {
    "E1": {
        "type": "A",
        "log": [],
        "rank": 0.8,
        "hp": 100,
    },
    "E2": {
        "type": "B",
        "log": [],
        "rank": 0.67,
        "hp": 80,
    },
    "E3": {
        "type": "C",
        "log": [],
        "rank": 0.6,
        "hp": 70,
    },
}

pheromone_trails = np.zeros((len(tasks), len(employees)))

for iteration in range(num_iterations):
    for ant in range(num_ants):
        solution = []
        total_resources = 0

        while total_resources < employees[list(employees.keys())[ant]]["hp"]:
            probabilities = np.zeros(len(tasks))
            for i, task in enumerate(tasks):
                probabilities[i] = (
                    pheromone_trails[i, ant] ** alpha
                    * employees[list(employees.keys())[ant]]["rank"] ** beta
                )

            selected_task = np.random.choice(list(tasks.keys()), p=probabilities)

            solution.append(selected_task)

            total_resources += tasks[selected_task]["resources"]

        solution_quality = sum(
            [
                tasks[task]["weights"][i] * tasks[task]["scores"][i][ant]
                for i, task in enumerate(solution)
            ]
        )

        for task in solution:
            pheromone_trails[task, ant] += solution_quality

    pheromone_trails *= (1 - rho)

    pheromone_trails = np.clip(pheromone_trails, pheromone_min, pheromone_max)

best_solution = None
best_quality = 0
for ant in range(num_ants):
    solution = []
    total_resources = 0
    while total_resources < employees[list(employees.keys())[ant]]["hp"]:
        probabilities = np.zeros(len(tasks))
        for i, task in enumerate(tasks):
            probabilities[i] = (
                pheromone_trails[i, ant] ** alpha
                * employees[list(employees.keys())[ant]]["rank"] ** beta
            )
        selected_task = np.random.choice(list(tasks.keys()), p=probabilities)
        solution.append(selected_task)
        total_resources += tasks[selected_task]["resources"]
    solution_quality = sum(
        [
            tasks[task]["weights"][i] * tasks[task]["scores"][i][ant]
            for i, task in enumerate(solution)
        ]
    )
    if solution_quality > best_quality:
        best_solution = solution
        best_quality = solution_quality

for i, employee in enumerate(employees):
    for j, task in enumerate(best_solution):
        employees[employee]["KPI"][j] = tasks[task]["scores"][j][i]

# Output the results
print("Best solution:", best_solution)
print("Best quality:", best_quality)
print("KPI values for employees:", employees)