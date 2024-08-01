"use client";

import React, { FC, useState, useEffect } from "react";
import { handleFetchEmployeesList } from "../hooks";
import { Employee, EmployeesResponse } from "../type";

export const EmployeeList: FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const data: EmployeesResponse = await handleFetchEmployeesList();
        setEmployees(data.employees);
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, []);
  console.log(employees);
  return (
    <>
      <h1>EmployeeList</h1>
      {employees ? (
        employees.map((employee) => (
          <div key={employee.employee_id}>
            <p>{employee.first_name}</p>
            <p>{employee.last_name}</p>
          </div>
        ))
      ) : (
        <p>読み込み中...</p>
      )}
    </>
  );
};
