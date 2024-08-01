type EmployeeType = {
  created_at: string;
  employee_type_id: number;
  type_name: string;
  updated_at: string;
};

export type Employee = {
  dependencies: any[];
  employee_constraints: any[];
  employee_id: number;
  employee_type: EmployeeType;
  facility_id: number;
  first_name: string;
  last_name: string;
  qualifications: any[];
};

export type EmployeesResponse = {
  employees: Employee[] | [];
};
