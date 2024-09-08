import { fetchFromAPI } from "@/app/api/lib/api";
import { NextRequest, NextResponse } from "next/server";

export async function PUT(
  request: NextRequest,
  {
    params,
  }: { params: { facilityId: string; employeeId: string; requestsId: string } }
) {
  const facilityId = params.facilityId;
  const employeeId = params.employeeId;
  const requestId = params.requestsId;
  const body = await request.json();
  const res = await fetchFromAPI(
    `http://localhost:5000/v1/facilities/${facilityId}/employees/${employeeId}/requests/${requestId}`,
    "PUT",
    request,
    body
  );
  if (res.ok) {
    return res;
  } else {
    const error = await res.json();
    return NextResponse.json({ error }, { status: res.status });
  }
}
