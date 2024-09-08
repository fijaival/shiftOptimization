type Employee = {
  employeeId: number;
  firstName: string;
  lastName: string;
};

type Request = {
  requestId: number;
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

export type CreateRequestReqestBody = {
  date: string;
  typeOfVacation: string;
};

export type UpdateRequestRequsetBody = {
  typeOfVacation: string;
};

export type CreateRequestResponse = Request;
export type UpdateRequestResponse = Request;
