import { fetchEmployeesList } from "./endpoint";
import { EmployeesResponse, Employee } from "./type";
import humps from "humps";

export const handleFetchEmployeesList = async (
  facilityId: number
): Promise<Employee[]> => {
  try {
    const response = await fetchEmployeesList(facilityId);
    const data: EmployeesResponse = await response.json();
    console.log(data);
    return humps.camelizeKeys(data.employees) as Employee[];
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};
