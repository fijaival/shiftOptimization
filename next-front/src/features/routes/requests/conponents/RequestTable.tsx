"use client";

import React, { FC, useState, useEffect } from "react";
import { handleFetchAllRequests } from "../hooks";
import { handleFetchEmployeesList } from "../../employees/hooks";
import { Employee } from "../../employees/type";
import type { EmployeeRequests } from "../type";
import { useAuth } from "@/state/authContext";
import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  Skeleton,
  SkeletonCircle,
  SkeletonText,
  Text,
  SimpleGrid,
  Center,
  Spinner,
  Stack,
} from "@chakra-ui/react";

const generateAugustDates = () => {
  const dates = [];
  for (let day = 1; day <= 31; day++) {
    dates.push(`2024-08-${day.toString().padStart(2, "0")}`);
  }
  return dates;
};

const getDayOfWeek = (dateString: string) => {
  const date = new Date(dateString);
  const dayOfWeek = date.getDay();
  const days = ["日", "月", "火", "水", "木", "金", "土"];
  return days[dayOfWeek];
};
export const RequestTable: FC = () => {
  const [requests, setRequests] = useState<EmployeeRequests[]>([]);
  const { user } = useAuth();
  const augustDates = generateAugustDates();
  const [selectedRow, setSelectedRow] = useState<number | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<number | null>(null);

  useEffect(() => {
    async function fetchData(facilityId: number) {
      try {
        const req: EmployeeRequests[] = await handleFetchAllRequests(
          facilityId,
          "2024",
          "8"
        );
        console.log(req);
        setRequests(req);
      } catch (error) {
        console.error(error);
      }
    }
    if (user && user.facilityId) {
      fetchData(user.facilityId);
    }
  }, [user]);

  const handleCellClick = (rowIndex: number, colIndex: number) => {
    setSelectedRow(rowIndex);
    setSelectedColumn(colIndex);
  };

  return (
    <Stack>
      <Text fontSize="3xl">シフト希望</Text>
      {requests.length > 0 ? (
        <TableContainer maxW="1500px" mx="auto" mb="10">
          <Table
            variant="simple"
            size="sm"
            colorScheme="orange"
            sx={{
              "& td, & th": {
                border: "1px solid",
                borderColor: "orange.200",
              },
            }}
          >
            <Thead>
              <Tr>
                <Th position="sticky" left={0} zIndex={1} bg="white">
                  従業員
                </Th>
                {augustDates.map((date, colIndex) => (
                  <Th
                    key={date}
                    bg={selectedColumn === colIndex ? "orange.400" : "inherit"}
                    color={selectedColumn === colIndex ? "white" : "black"}
                  >
                    {date.split("-")[2]}
                  </Th>
                ))}
              </Tr>
              <Tr>
                <Th position="sticky" left={0} zIndex={1} bg="white">
                  曜日
                </Th>
                {augustDates.map((date, colIndex) => {
                  const dayOfWeek = getDayOfWeek(date);
                  const dayOfWeekColor =
                    dayOfWeek === "日"
                      ? "red.500"
                      : dayOfWeek === "土"
                      ? "blue.500"
                      : "inherit";

                  return (
                    <Th
                      key={date}
                      color={dayOfWeekColor}
                      bg={
                        selectedColumn === colIndex ? "orange.200" : "inherit"
                      }
                    >
                      {dayOfWeek}
                    </Th>
                  );
                })}
              </Tr>
            </Thead>
            <Tbody>
              {requests.map((employeeData, rowIndex) => (
                <Tr key={rowIndex}>
                  <Td
                    onClick={() => handleCellClick(rowIndex, -1)}
                    cursor="pointer"
                    position="sticky"
                    left={0}
                    zIndex={1}
                    bg={selectedRow === rowIndex ? "orange.400" : "white"}
                    color={selectedRow === rowIndex ? "white" : "black"}
                  >{`${employeeData.employee.lastName} ${employeeData.employee.firstName}`}</Td>
                  {augustDates.map((date, colIndex) => {
                    const request = employeeData.requests.find(
                      (request) => request.date === date
                    );
                    return (
                      <Td
                        key={date}
                        onClick={() => handleCellClick(rowIndex, colIndex)}
                        cursor="pointer"
                        bg={
                          selectedRow === rowIndex ||
                          selectedColumn === colIndex
                            ? "orange.100"
                            : "inherit"
                        }
                      >
                        {request ? request.typeOfVacation : ""}
                      </Td>
                    );
                  })}
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
      ) : (
        <Stack>
          <Skeleton height="100px" />
          <Skeleton height="20px" />
          <Skeleton height="20px" />
        </Stack>
      )}
    </Stack>
  );
};
