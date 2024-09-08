import humps from "humps";
import { createRequest, fetchAllRequests, putRequest } from "./endpoint";
import {
  AllRequestsResponse,
  CreateRequestResponse,
  EmployeeRequests,
  UpdateRequestResponse,
} from "./type";

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

export const addRequest = async (
  facilityId: number,
  employeeId: number,
  body: { date: string; typeOfVacation: string }
): Promise<CreateRequestResponse> => {
  try {
    const response = await createRequest(facilityId, employeeId, body);
    const data: CreateRequestResponse = await response.json();
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return humps.camelizeKeys(data) as CreateRequestResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};

export const updateRequest = async (
  facilityId: number,
  employeeId: number,
  requestId: number,
  body: { typeOfVacation: string }
): Promise<UpdateRequestResponse> => {
  try {
    const response = await putRequest(facilityId, employeeId, requestId, body);
    const data: UpdateRequestResponse = await response.json();
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return humps.camelizeKeys(data) as UpdateRequestResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};
