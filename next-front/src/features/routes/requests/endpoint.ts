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
