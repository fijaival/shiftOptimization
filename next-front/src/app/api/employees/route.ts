import { NextRequest, NextResponse } from "next/server";
import { fetchFromAPI } from "../lib/api";

export async function GET(request: NextRequest) {
  const res = await fetchFromAPI(
    "http://localhost:5000/v1/facilities/1/employees",
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
