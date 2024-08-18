"use client";

import React, { FC, useState, useEffect, use } from "react";
import { handleFetchEmployeesList } from "../hooks";
import { Employee, EmployeesResponse } from "../type";
import { useAuth } from "@/state/authContext";
import { Button } from "@chakra-ui/react";
export const EmployeeList: FC = () => {
  const { user } = useAuth();

  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const emp: Employee[] = await handleFetchEmployeesList();
        setEmployees(emp);
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, []);

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
