from api.v1.utils.error import InvalidAPIUsage
from . import facility_class_map
from ..day_off_requests import get_all_requests_service
from ..employees import get_all_employees_service


def run_optimization(facility_id: int, year: int, month: int) -> list | None:
    employees_data = get_all_employees_service(facility_id)
    day_off_requests = get_all_requests_service(facility_id, year, month)
    scheduler_class = facility_class_map.get(facility_id)
    last_month_shifts = None
    if not scheduler_class:
        return None

    print(employees_data)

    scheduler = scheduler_class(employees_data, day_off_requests, last_month_shifts, int(year), int(month))
    result: list = scheduler.solve()
    if result is None:
        raise InvalidAPIUsage("No optimal solution found.", 500)
    return result
