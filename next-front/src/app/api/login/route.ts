import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const res: Response = await fetch("http://localhost:5000/v1/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (res.ok) {
      const setCookieHeader = res.headers.get("set-cookie");
      const response = NextResponse.redirect(new URL("/employee", request.url));

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
