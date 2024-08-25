"use client";

import React, { FC, useState, useEffect } from "react";
import { handleFetchAllRequests } from "../hooks";
import type { EmployeeRequests } from "../type";
import { useAuth } from "@/state/authContext";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Skeleton,
  Text,
  Stack,
  Input,
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
  const [editingCell, setEditingCell] = useState<{
    row: number;
    col: number;
  } | null>(null);

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

  const handleCellDoubleClick = (rowIndex: number, colIndex: number) => {
    setEditingCell({ row: rowIndex, col: colIndex });
  };

  const handleInputChange = (
    rowIndex: number,
    colIndex: number,
    value: string
  ) => {
    const updatedRequests = [...requests];
    const request = updatedRequests[rowIndex].requests.find(
      (request) => request.date === augustDates[colIndex]
    );
    if (request) {
      request.typeOfVacation = value;
    } else {
      updatedRequests[rowIndex].requests.push({
        date: augustDates[colIndex],
        typeOfVacation: value,
      });
    }
    setRequests(updatedRequests);
  };

  const handleInputBlur = () => {
    setEditingCell(null);
  };

  return (
    <Stack>
      <Text fontSize="3xl">シフト希望</Text>
      {requests.length > 0 ? (
        <TableContainer maxW="1500px" mx="auto" mb="10" width="90vw">
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
                    onClick={() => handleCellClick(-1, colIndex)}
                    cursor="pointer"
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
                      onClick={() => handleCellClick(-1, colIndex)}
                      cursor="pointer"
                      color={
                        selectedColumn === colIndex &&
                        dayOfWeekColor == "inherit"
                          ? "white"
                          : dayOfWeekColor
                      }
                      bg={
                        selectedColumn === colIndex ? "orange.400" : "inherit"
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
                    const isEditing =
                      editingCell &&
                      editingCell.row === rowIndex &&
                      editingCell.col === colIndex;

                    return (
                      <Td
                        key={date}
                        onClick={() => handleCellClick(rowIndex, colIndex)}
                        onDoubleClick={() =>
                          handleCellDoubleClick(rowIndex, colIndex)
                        }
                        cursor="pointer"
                        bg={
                          selectedRow === rowIndex ||
                          selectedColumn === colIndex
                            ? "orange.100"
                            : "inherit"
                        }
                      >
                        {isEditing ? (
                          <Input
                            margin="0"
                            padding="0"
                            width="100%"
                            height="100%"
                            value={request ? request.typeOfVacation : ""}
                            onChange={(e) =>
                              handleInputChange(
                                rowIndex,
                                colIndex,
                                e.target.value
                              )
                            }
                            onBlur={handleInputBlur}
                            size="sm"
                            autoFocus
                          />
                        ) : request ? (
                          request.typeOfVacation
                        ) : (
                          ""
                        )}
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
