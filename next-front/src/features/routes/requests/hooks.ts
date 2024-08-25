import { fetchAllRequests } from "./endpoint";
import { AllRequestsResponse, EmployeeRequests } from "./type";
import humps from "humps";

export const handleFetchAllRequests = async (
  facilityId: number,
  year: string,
  month: string
): Promise<EmployeeRequests[]> => {
  try {
    const response = await fetchAllRequests(facilityId, year, month);
    const data: AllRequestsResponse = await response.json();
    console.log(data);
    return humps.camelizeKeys(data.requests) as EmployeeRequests[];
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};
