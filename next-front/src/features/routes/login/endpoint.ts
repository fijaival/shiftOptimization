export const login = async (
  username: string,
  password: string
): Promise<Response> => {
  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (response.status == 401) {
      throw new Error("ユーザー名またはパスワードが正しくありません");
    }
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    return response;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`${error.message}`);
    } else {
      throw new Error("ログインに失敗しました");
    }
  }
};
