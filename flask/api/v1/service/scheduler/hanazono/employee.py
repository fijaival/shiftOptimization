import datetime
import pulp
from ....models import DayOffRequestSchema


class Employee:
    def __init__(self,
                 requests_arr: list[int],
                 paid_off_count: int,
                 last_month_shift,
                 facility_work_types,
                 employee_type: dict,
                 qualifications: list[dict],
                 employee_constraints: list[dict],
                 dependencies: list[dict],
                 employee_id: int,
                 first_name: str,
                 last_name: str,
                 created_at: datetime,
                 updated_at: datetime):

        self.id: int = employee_id
        self.name: str = first_name + " " + last_name
        self.paid_off: int = paid_off_count
        self.weekly_days: int = next((item['value']
                                     for item in employee_constraints if item['constraint']['name'] == '勤務数/週'), 3)
        self.over_work: bool = any(item['name'] == '超過勤務' for item in qualifications)
        self.full_time: bool = any(item['name'] == '全日勤務' for item in qualifications)
        self.work_type: list[str] = [item["name"] for item in qualifications if item["name"] in facility_work_types]
        self.last_month_consecutive_days: int = 0
        self.last_month_period_work_days: int = 0
        self.day_off_requests: list[str] = requests_arr
        self.shift_vars = {}
        self.assigned_vars = {}
        self.paid_vars = {}
        self.penalty_vars = {}
        self.shift_request_penalty_vars = {}
        self.first_week_penalty_vars = 0

    def create_shift_variables(self, days, work_types):
        # shift_vars（特定のシフトに入っているか否か）
        for day in days:
            for work_type in work_types:
                var_name = f"x({self.id},{day},{work_type})"
                self.shift_vars[(day, work_type)] = pulp.LpVariable(var_name, 0, 1, cat="Binary")

        # assigned_vars（特定の日付に１つ以上の業務に入っているか否か）
        for day in days:
            var_name = f"x({self.id},{day})"
            self.assigned_vars[day] = pulp.LpVariable(var_name, 0, 1, cat="Binary")

        # paid_vars（特定の日が有給か否か）
        for day in days:
            var_name = f"x({self.id},{day}) is paid"
            self.paid_vars[day] = pulp.LpVariable(var_name, 0, 1, cat="Binary")

    def create_penalty_variables(self, weeks_in_month):
        # 週当たりの業務日数超過のペナルティ
        for week in range(weeks_in_month):
            var_name = f"penalty({self.id},{week})"
            self.penalty_vars[week] = pulp.LpVariable(var_name, 0, 1, cat="Binary")
        var_name = f"first_week_penalty({self.id})"
        self.first_week_penalty_vars = pulp.LpVariable(var_name, 0, 1, cat="Binary")


class Full_Time_Employee:
    def __init__(self,
                 requests_arr: list[int],
                 paid_off_count: int,
                 last_month_shift,
                 facility_work_types,
                 employee_type: dict,
                 qualifications: list[dict],
                 employee_constraints: list[dict],
                 dependencies: list[dict],
                 employee_id: int,
                 first_name: str,
                 last_name: str,
                 created_at: datetime,
                 updated_at: datetime):
        self.id = employee_id
        self.name = first_name + " " + last_name
        self.paid_off = paid_off_count
        self.holiday_count_per_month = next((item['value']
                                             for item in employee_constraints if item['constraint']['name'] == '休暇日数/月'), 3)
        self.last_month_consecutive_days: int = 0
        self.day_off_requests = requests_arr
        self.shift_vars = {}
        self.paid_vars = {}

    def create_shift_variables(self, days):
        for day in days:
            var_name = f"x({self.id},{day})"
            self.shift_vars[day] = pulp.LpVariable(var_name, 0, 1, cat="Binary")

        # paid_vars（特定の日が有給か否か）
        for day in days:
            var_name = f"x({self.id},{day}) is paid"
            self.paid_vars[day] = pulp.LpVariable(var_name, 0, 1, cat="Binary")
