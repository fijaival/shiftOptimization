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

type EmployeeConstraint = {
  constraint: Constraint;
  value: number;
};

type Qualification = {
  qualificationId: number;
  name: string;
};

export type Employee = {
  dependencies: Dependencies[];
  employeeConstraints: EmployeeConstraint[];
  employeeId: number;
  employeeType: EmployeeType;
  facilityId: number;
  firstName: string;
  lastName: string;
  qualifications: Qualification[];
};

export type EmployeesResponse = {
  employees: Employee[] | [];
};
