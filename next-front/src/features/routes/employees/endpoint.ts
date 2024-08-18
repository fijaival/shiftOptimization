export const fetchEmployeesList = async (
  facilityId: number
): Promise<Response> => {
  try {
    const response = await fetch(`/api/facilities/${facilityId}/employees`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
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
