import { NextRequest, NextResponse } from "next/server";
import { fetchFromAPI } from "@/app/api/lib/api";

export async function GET(
  request: NextRequest,
  { params }: { params: { facilityId: string } }
) {
  const facilityId = params.facilityId;
  const res = await fetchFromAPI(
    `http://localhost:5000/v1/facilities/${facilityId}/employees`,
    "GET",
    request
  );
  if (res.ok) {
    return res;
  } else {
    const error = await res.json();
    return NextResponse.json({ error }, { status: res.status });
  }
}
