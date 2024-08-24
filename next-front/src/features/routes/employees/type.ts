type EmployeeType = {
  createdAt: string;
  employeeTypeId: number;
  typeName: string;
  updatedAt: string;
};

type DependentEmployee = {
  employeeId: number;
  firstName: string;
  lastName: string;
};

type Dependencies = {
  dependencyId: number;
  dependentEmployee: DependentEmployee;
};

type Constraint = {
  constraint_id: number;
  name: string;
};

type EmployeeConstraints = {
  constraint: Constraint;
  value: number;
};

export type Employee = {
  dependencies: Dependencies[];
  employeeConstraints: EmployeeConstraints[];
  employeeId: number;
  employeeType: EmployeeType;
  facilityId: number;
  firstName: string;
  lastName: string;
  qualifications: any[];
};

export type EmployeesResponse = {
  employees: Employee[] | [];
};
