class Task:
    def __init__(self, task_1, task_2, task_3, kpi):
        self.task_1 = task_1
        self.task_2 = task_2
        self.task_3 = task_3
        self.kpi = kpi
class Employee:
    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
class KPIModel:
    def __init__(self):
        self.G = {}
        self.kpi_department = {
            'kpi': 10,
            # Thêm các giá trị KPI khác của bộ phận tại đây
        }
        self.kpi_employee = {
            'employee_1': Employee('e01', {
                'month_1': Task(7, 8, 5, 7),
                'month_2': Task(8, 5, 7, 7)
            }),
            'employee_2': Employee('e02', {
                'month_1': Task(7, 8, 5, 7),
                'month_2': Task(8, 5, 7, 7)
            })
            # Thêm các nhân viên và giá trị KPI của họ tại đây
        }
        self.desired_kpis = {
            'quality': 'Mục tiêu về chất lượng',
            'progress': 'Mục tiêu về tiến độ',
            # Thêm các mục tiêu KPI mong muốn khác tại đây
        }

kpi_model = KPIModel()
