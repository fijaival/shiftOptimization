from datetime import datetime


class Shift:
    def __init__(self, employee_id, task_id, date, shift_number):
        self.employee_id: int = employee_id
        self.task_id: int = task_id
        self.date: datetime = date
        self.shift_number: int = shift_number

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "task_id": self.task_id,
            "date": self.date.strftime('%Y-%m-%d'),
            "shift_number": self.shift_number
        }
