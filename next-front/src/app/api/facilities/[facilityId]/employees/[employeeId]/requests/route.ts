import { NextRequest, NextResponse } from "next/server";
import { fetchFromAPI } from "@/app/api/lib/api";

export async function POST(
  request: NextRequest,
  { params }: { params: { facilityId: string; employeeId: string } }
) {
  const facilityId = params.facilityId;
  const employeeId = params.employeeId;
  const body = await request.json();
  const res = await fetchFromAPI(
    `http://localhost:5000/v1/facilities/${facilityId}/employees/${employeeId}/requests`,
    "POST",
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
