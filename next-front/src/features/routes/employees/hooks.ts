import { fetchEmployeesList } from "./endpoint";
import { EmployeesResponse } from "./type";

export const handleFetchEmployeesList =
  async (): Promise<EmployeesResponse> => {
    try {
      const response = await fetchEmployeesList();
      const data = await response.json();
      console.log(data);
      return data as EmployeesResponse;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`${error.message}`);
      } else {
        throw new Error("Error");
      }
    }
  };
