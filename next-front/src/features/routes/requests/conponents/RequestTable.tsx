"use client";

import React, { FC, useState, useEffect } from "react";
import { handleFetchAllRequests } from "../hooks";
import { Employee } from "../../employees/type";
import type { EmployeeRequests } from "../type";
import { useAuth } from "@/state/authContext";
import { Text, SimpleGrid, Center, Spinner, Stack } from "@chakra-ui/react";
export const RequestTable: FC = () => {
  const [employees, setEmployees] = useState<EmployeeRequests[]>([]);
  const { user } = useAuth();

  useEffect(() => {
    async function fetchData(facilityId: number) {
      try {
        const req: EmployeeRequests[] = await handleFetchAllRequests(
          facilityId,
          "2024",
          "8"
        );
        console.log(req);
        setEmployees(req);
      } catch (error) {
        console.error(error);
      }
    }
    console.log(user);
    if (user && user.facilityId) {
      fetchData(user.facilityId);
    }
  }, [user]);

  return (
    <>
      {employees.map((emp) => {
        return <Stack></Stack>;
      })}
    </>
  );
};
