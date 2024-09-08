import { NextRequest, NextResponse } from "next/server";
import { fetchFromAPI } from "../lib/api";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const res: Response = await fetchFromAPI(
      "http://localhost:5000/v1/auth/login",
      "POST",
      request,
      body
    );

    if (res.ok) {
      const setCookieHeader = res.headers.get("set-cookie");
      const response = NextResponse.json(await res.json(), { status: 200 });
      if (setCookieHeader) {
        const cookies = setCookieHeader.split(",");
        cookies.forEach((cookie) => {
          const token = cookie.split(";")[0];
          console.log(token);
          response.headers.append("Set-Cookie", token);
        });
      }

      return response;
    } else {
      const error = await res.json();
      return NextResponse.json({ error }, { status: res.status });
    }
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
