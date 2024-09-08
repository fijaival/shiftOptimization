"use client";

import { useAuth } from "@/state/authContext";
import { ChevronLeftIcon, ChevronRightIcon } from "@chakra-ui/icons";
import {
  Box,
  IconButton,
  Select,
  Skeleton,
  Stack,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  useToast,
} from "@chakra-ui/react";
import { FC, useEffect, useState } from "react";
import {
  addRequest,
  deleteRequest,
  handleFetchAllRequests,
  updateRequest,
} from "../hooks";
import type { EmployeeRequests } from "../type";

const generateDates = (year: string, month: string) => {
  const dates = [];
  const paddedMonth = month.padStart(2, "0"); // monthを2桁にパディング
  const daysInMonth = new Date(parseInt(year), parseInt(month), 0).getDate(); // 指定された月の日数を取得
  for (let day = 1; day <= daysInMonth; day++) {
    dates.push(`${year}-${paddedMonth}-${day.toString().padStart(2, "0")}`);
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
  const [month, setMonth] = useState<string>(
    (new Date().getMonth() + 2).toString()
  );

  const [year, setYear] = useState<string>(
    month === "1"
      ? (new Date().getFullYear() + 1).toString()
      : new Date().getFullYear().toString()
  );

  const dates = generateDates(year, month);
  const [selectedRow, setSelectedRow] = useState<number | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<number | null>(null);
  const [editingCell, setEditingCell] = useState<{
    row: number;
    col: number;
  } | null>(null);
  const toast = useToast();

  useEffect(() => {
    async function fetchData(facilityId: number) {
      try {
        const req: EmployeeRequests[] = await handleFetchAllRequests(
          facilityId,
          year,
          month
        );
        setRequests(req);
      } catch (error) {
        console.error(error);
      }
    }
    if (user && user.facilityId) {
      fetchData(user.facilityId);
    }
  }, [user, month]);

  const handleCellClick = (rowIndex: number, colIndex: number) => {
    setSelectedRow(rowIndex);
    setSelectedColumn(colIndex);
    setEditingCell({ row: rowIndex, col: colIndex });
  };

  const handleInputChange = async (
    rowIndex: number,
    colIndex: number,
    value: string
  ) => {
    setEditingCell(null);
    if (!user) return;
    const empRequest = requests[rowIndex];
    const originalRequests: EmployeeRequests[] = JSON.parse(
      JSON.stringify(requests)
    );
    const updatedRequests: EmployeeRequests[] = JSON.parse(
      JSON.stringify(requests)
    );

    // 画面の即時変更
    const updatedRequestIndex = updatedRequests[rowIndex].requests.findIndex(
      (request) => request.date === dates[colIndex]
    );
    if (updatedRequestIndex !== -1) {
      if (value === "") {
        updatedRequests[rowIndex].requests.splice(updatedRequestIndex, 1);
      } else {
        updatedRequests[rowIndex].requests[updatedRequestIndex].typeOfVacation =
          value;
      }
    } else {
      updatedRequests[rowIndex].requests.push({
        date: dates[colIndex],
        requestId: -1,
        typeOfVacation: value,
      });
    }
    setRequests(updatedRequests);
    try {
      const request = empRequest.requests.find(
        (request) =>
          request.date === dates[colIndex] && request.requestId !== -1
      );
      if (request) {
        // valueが空の場合は削除
        if (value === "") {
          await deleteRequest(
            user.facilityId,
            empRequest.employee.employeeId,
            request.requestId
          );
        } else {
          await updateRequest(
            user.facilityId,
            empRequest.employee.employeeId,
            request.requestId,
            { typeOfVacation: value }
          );
        }
      } else {
        const newRequest = await addRequest(
          user.facilityId,
          empRequest.employee.employeeId,
          {
            date: dates[colIndex],
            typeOfVacation: value,
          }
        );
        const addedRequestIndex = updatedRequests[rowIndex].requests.findIndex(
          (req) => req.date === dates[colIndex] && req.requestId === -1
        );
        updatedRequests[rowIndex].requests[addedRequestIndex].requestId =
          newRequest.requestId; // 返ってきたIDに更新
        setRequests([...updatedRequests]);
      }
    } catch (error) {
      console.error(error);
      toast({
        title: "休み希望の更新に失敗しました",
        description: "もう一度お試しください。",
        status: "error",
        duration: 5000,
        isClosable: true,
        position: "bottom-left",
      });
      setRequests(originalRequests);
    }
  };

  const handleInputBlur = () => {
    setEditingCell(null);
  };
  const handlePrevMonth = () => {
    if (month == "1") {
      setMonth("12");
      setYear((parseInt(year) - 1).toString());
    } else {
      setMonth((parseInt(month) - 1).toString());
    }
  };
  const handleNextMonth = () => {
    if (month == "12") {
      setMonth("1");
      setYear((parseInt(year) + 1).toString());
    } else {
      setMonth((parseInt(month) + 1).toString());
    }
  };

  return (
    <Stack>
      <Box justifyContent="center" alignItems="center" display="flex">
        <IconButton
          colorScheme="orange"
          fontSize="20px"
          aria-label="move to prev month"
          icon={<ChevronLeftIcon />}
          onClick={handlePrevMonth}
        ></IconButton>
        <Text fontSize="3xl" sx={{ px: "5" }}>
          {month}月シフト希望
        </Text>
        <IconButton
          colorScheme="orange"
          fontSize="20px"
          aria-label="move to next month"
          icon={<ChevronRightIcon />}
          onClick={handleNextMonth}
        ></IconButton>
      </Box>

      {requests.length > 0 ? (
        <TableContainer
          maxW="1500px"
          mx="auto"
          mb="10"
          width="90vw"
          maxHeight="80vh"
          overflowX="scroll"
          overflowY="scroll"
        >
          <Table
            variant="simple"
            size="sm"
            colorScheme="orange"
            sx={{
              borderCollapse: "collapse",
              "& td, & th": {
                border: "1px solid ",
                borderColor: "orange.200",
              },
            }}
          >
            <Thead>
              <Tr>
                <Th position="sticky" bg="white" left={0} top={0} zIndex={3}>
                  従業員
                </Th>
                {dates.map((date, colIndex) => (
                  <Th
                    key={date}
                    onClick={() => handleCellClick(-1, colIndex)}
                    cursor="pointer"
                    bg={selectedColumn === colIndex ? "orange.400" : "white"}
                    color={selectedColumn === colIndex ? "white" : "black"}
                    position="sticky"
                    top={0}
                    zIndex={2}
                  >
                    {date.split("-")[2]}
                  </Th>
                ))}
              </Tr>
              <Tr>
                <Th position="sticky" bg="white" left={0} top="24px" zIndex={3}>
                  曜日
                </Th>
                {dates.map((date, colIndex) => {
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
                      bg={selectedColumn === colIndex ? "orange.400" : "white"}
                      position="sticky"
                      top="24px"
                      zIndex={1}
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
                  {dates.map((date, colIndex) => {
                    const dayReqest = employeeData.requests.find(
                      (req) => req.date === date
                    );
                    const isEditing =
                      editingCell &&
                      editingCell.row === rowIndex &&
                      editingCell.col === colIndex;

                    return (
                      <Td
                        padding="0"
                        textAlign="center"
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
                        {isEditing ? (
                          <Select
                            value={dayReqest ? dayReqest.typeOfVacation : ""}
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
                            sx={{
                              px: 0,
                            }}
                          >
                            <option value=""> </option>
                            <option value="×">×</option>
                            <option value="有">有</option>
                            <option value="前×">前×</option>
                            <option value="後×">後×</option>
                          </Select>
                        ) : dayReqest ? (
                          dayReqest.typeOfVacation
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
          <Skeleton height="0px" width="90vw" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
          <Skeleton height="40px" />
        </Stack>
      )}
    </Stack>
  );
};
