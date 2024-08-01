import { login } from "./endpoint";
import { LoginFormInputs, LoginResponse } from "./type";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

export const handleLogin = async (
  data: LoginFormInputs,
  router: AppRouterInstance
): Promise<string | null> => {
  try {
    const response: LoginResponse = await login(data.username, data.password);
    if (response.redirected) {
      router.push(response.url);
      return null;
    } else {
      return "ログインに失敗しました";
    }
  } catch (error) {
    if (error instanceof Error) {
      return error.message;
    } else {
      return "ログイン中に不明なエラーが発生しました";
    }
  }
};
