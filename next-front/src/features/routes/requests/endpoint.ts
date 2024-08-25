import type { CreateRequestReqestBody } from "./type";
import humps from "humps";

export const fetchAllRequests = async (
  facilityId: number,
  year: string,
  month: string
): Promise<Response> => {
  try {
    const params = { year, month };
    const query = new URLSearchParams(params);
    const response = await fetch(
      `/api/facilities/${facilityId}/requests?${query}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return response;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};

export const createRequest = async (
  facilityId: number,
  employeeId: number,
  body: CreateRequestReqestBody
): Promise<Response> => {
  try {
    const response = await fetch(
      `/api/facilities/${facilityId}/employees/${employeeId}/requests`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(humps.decamelizeKeys(body)),
      }
    );
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return response;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("Error");
    }
  }
};
