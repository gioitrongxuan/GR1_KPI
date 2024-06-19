import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt

import json
with open('data.json') as f:
    data = json.load(f)

# Customization section:
initial_temperature = 1000
cooling_rate = 0.95  # hệ số làm lạnh
number_variables = 2
upper_bounds = [3, 3]
lower_bounds = [-3, -3]
computing_time = 1  # thời gian tính toán (giây)

best_fitness = float('inf')  # Khởi tạo best_fitness
def objective_function(X, data):
    x = X[0]
    y = X[1]
    value = 0

    # Tính toán giá trị công việc cho từng nhân viên
    for task in data["tasks"]:
        task_id = task["id"]
        task_name = task["name"]
        task_precedings = task["precedings"]
        task_estimate_effort = task["estimate_effort"]
        task_require_assign = task["require_assign"]

        # Tính toán giá trị công việc cho nhân viên được yêu cầu
        if task_id in task_require_assign:
            employee_id = task_require_assign[task_id]
            employee = next((emp for emp in data["employees"] if emp["id"] == employee_id), None)
            if employee:
                cost_per_hour = employee["cost_per_hour"]
                qualities = employee["qualities"]
                degree = qualities["degree"]
                year_of_exp = qualities["year_of_exp"]
                automation_test = qualities["automation_test"]

                # Tính toán giá trị công việc dựa trên các yếu tố nhân viên
                task_value = (
                    task_estimate_effort
                    * (degree + year_of_exp + automation_test)
                    / (cost_per_hour + 1)
                )

                # Cộng dồn giá trị công việc của các nhân viên
                value += task_value
        if task_id in task_require_assign:
            employee_id = task_require_assign[task_id]
            employee = next((emp for emp in data["employees"] if emp["id"] == employee_id), None)
            if employee:
                cost_per_hour = employee["cost_per_hour"]
                qualities = employee["qualities"]
                degree = qualities["degree"]
                year_of_exp = qualities["year_of_exp"]
                automation_test = qualities["automation_test"]

                # Tính toán giá trị công việc dựa trên các yếu tố nhân viên
                task_value = (
                    task_estimate_effort
                    * (degree + year_of_exp + automation_test)
                    / (cost_per_hour + 1)
                )

                # Cộng dồn giá trị công việc của các nhân viên
                value += task_value

    # Áp dụng công thức tính giá trị mục tiêu
    value = (
        3 * (1 - x) ** 2 * math.exp(-x**2 - (y + 1) ** 2)
        - 10
        * (x / 5 - x**3 - y**5)
        * math.exp(-x**2 - y**2)
        - 1
        / 3
        * math.exp(-(x + 1) ** 2 - y**2)
        + value  # Cộng dồn giá trị công việc của các nhân viên
    )

    return value


# Giải thuật Simulated Annealing:
def simulated_annealing():
    initial_solution = np.random.uniform(lower_bounds, upper_bounds, size=(number_variables))
    current_solution = initial_solution.copy()
    best_solution = initial_solution.copy()
    n = 1  # số lượng giải pháp được chấp nhận
    best_fitness = objective_function(best_solution,data)
    current_temperature = initial_temperature
    start = time.time()
    no_attempts = 100  # số lần thử trong mỗi mức nhiệt độ
    record_best_fitness = []

    while time.time() - start < computing_time:
        for _ in range(no_attempts):
            new_solution = current_solution.copy()
            # Tạo đột biến nhỏ ngẫu nhiên trong mỗi biến
            for k in range(number_variables):
                new_solution[k] = current_solution[k] + 0.1 * (
                    random.uniform(lower_bounds[k], upper_bounds[k])
                )

            new_fitness = objective_function(new_solution,data)
            delta_energy = new_fitness - best_fitness

            # Tiêu chí chấp nhận Metropolis (xem xét các giải pháp tồi hơn với xác suất)
            if delta_energy < 0 or math.exp(-delta_energy / current_temperature) > random.random():
                current_solution = new_solution.copy()
                if new_fitness < best_fitness:
                    best_solution = new_solution.copy()
                    best_fitness = new_fitness
                    n += 1

        current_temperature *= cooling_rate
        record_best_fitness.append(best_fitness)

    return best_solution, record_best_fitness


# Chạy giải thuật Simulated Annealing
best_solution, fitness_history = simulated_annealing()
print("Giải pháp tốt nhất:", best_solution)
print("Giá trị tốt nhất:", best_solution)  # Sửa tên biến

# Tùy chọn: Vẽ đồ thị lịch sử fitness
plt.plot(fitness_history)
plt.xlabel("Lần lặp")
plt.ylabel("Fitness")
plt.title("Lịch sử Fitness của Simulated Annealing")
plt.show()
