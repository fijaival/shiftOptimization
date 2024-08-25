type Employee = {
  employeeId: number;
  firstName: string;
  lastName: string;
};

type Request = {
  date: string;
  typeOfVacation: string;
};

export type EmployeeRequests = {
  employee: Employee;
  requests: Request[];
};

export type AllRequestsResponse = {
  requests: EmployeeRequests[] | [];
};
