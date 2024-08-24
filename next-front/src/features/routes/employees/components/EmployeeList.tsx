"use client";

import React, { FC, useState, useEffect } from "react";
import { handleFetchEmployeesList } from "../hooks";
import { Employee } from "../type";
import { useAuth } from "@/state/authContext";
import { Text, SimpleGrid, Center, Spinner, Stack } from "@chakra-ui/react";
import EmployeeCard from "./EmployeeCard";
export const EmployeeList: FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const { user } = useAuth();

  useEffect(() => {
    async function fetchData(facilityId: number) {
      try {
        const emp: Employee[] = await handleFetchEmployeesList(facilityId);
        console.log(emp);
        setEmployees(emp);
      } catch (error) {
        console.error(error);
      }
    }
    if (user) {
      console.log(user);
      fetchData(user.facilityId);
    }
  }, [user]);

  return (
    <Stack>
      <Text fontSize="5xl">従業員一覧</Text>
      {employees ? (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} padding={6}>
          {employees.map((employee, index) => (
            <EmployeeCard
              key={index}
              name={employee.lastName + " " + employee.firstName}
              role={employee.employeeType.typeName}
              dependencies={employee.dependencies.map(
                (dep) =>
                  dep.dependentEmployee.lastName +
                  " " +
                  dep.dependentEmployee.firstName
              )}
              qualifications={employee.qualifications.map(
                (qualification) => qualification.name
              )}
              constraints={employee.employeeConstraints.map(
                (constraint) => constraint.constraint.name
              )}
              avatarUrl={employee.firstName}
            />
          ))}
        </SimpleGrid>
      ) : (
        <Center h="100vh">
          {/* ぐるぐる回るローディング */}
          <Spinner />
        </Center>
      )}
    </Stack>
  );
};
