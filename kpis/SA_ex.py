import time
import random
import math
import json
from numpy import array
import time
import matplotlib.pyplot as plt

with open('data.json') as f:
    data = json.load(f)

# Customization section:
initial_temperature = 100
cooling_rate = 0.95  # hệ số làm lạnh
max_iterations = 1000  # số lần lặp tối đa

best_fitness = float('inf')  # Khởi tạo best_fitness
assigned_employees = set()
def sort_employees_by_cost(employees):
    return sorted(employees, key=lambda emp: emp["cost_per_hour"])

def assign_employees(tasks, employees):
    sorted_employees = sort_employees_by_cost(employees)
    assigned_tasks = []
    total_cost = 0

    

    for task in tasks:
        task_id = task["id"]
        task_name = task["name"]
        task_precedings = task["precedings"]
        task_estimate_effort = task["estimate_effort"]
        task_require_assign = task["require_assign"]

       # Tìm nhân viên có chi phí giờ làm thấp nhất và còn thời gian làm việc
        employee = None
        for emp in sorted_employees:
            if emp["time"] >= task_estimate_effort:
                employee = emp
                break

        if employee is None:
            continue

        # Gán công việc cho nhân viên
        assigned_employees.add((task_id, employee["id"]))
        task_estimate_effort = task_estimate_effort

        # Tính tổng chi phí
        total_cost += task_estimate_effort * employee["cost_per_hour"]

        # Giảm thời gian làm việc của nhân viên
        employee["time"] -= task_estimate_effort

        # Thêm công việc đã gán vào danh sách
        assigned_tasks.append(task)

        # Đưa nhân viên trở lại danh sách để gán công việc trong tương lai
        sorted_employees.append(employee)
        sorted_employees = sort_employees_by_cost(sorted_employees)

    return assigned_tasks, total_cost, assigned_employees

def simulated_annealing(tasks, employees):
    global best_fitness
    current_solution, current_cost, assigned_employees = assign_employees(tasks, employees)

    best_solution = current_solution
    best_cost = current_cost

    temperature = initial_temperature
    iterations = 0

    while temperature > 0 and best_cost > 0 and iterations < max_iterations:
        neighbor_solution, neighbor_cost, _ = assign_employees(tasks, employees)

        if neighbor_cost < current_cost:
            current_solution = neighbor_solution
            current_cost = neighbor_cost
        else:
            acceptance_probability = math.exp((current_cost - neighbor_cost) / temperature)
            if random.uniform(0, 1) < acceptance_probability:
                current_solution = neighbor_solution
                current_cost = neighbor_cost

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        temperature *= cooling_rate
        iterations += 1

    return best_solution, best_cost

# Chạy thuật toán simulated annealing để tìm giải pháp tối ưu
best_solution, best_cost = simulated_annealing(data["tasks"], data["employees"])

assigned_tasks = [task["name"] for task in best_solution]
print("Công việc đã gán:", assigned_tasks)

# In ra employee và Task trong mảng assigned_employees
for task_id, employee_id in assigned_employees:
    task_name = next(task["name"] for task in data["tasks"] if task["id"] == task_id)
    employee_name = next(employee["name"] for employee in data["employees"] if employee["id"] == employee_id)
    print("Task:", task_name, "Employee:", employee_name)