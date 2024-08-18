import { login } from "./endpoint";
import { LoginFormInputs, UserType } from "./type";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

export const handleLogin = async (
  data: LoginFormInputs,
  router: AppRouterInstance
): Promise<string | UserType> => {
  try {
    const response: Response = await login(data.username, data.password);
    if (response.ok) {
      const body = await response.json();
      router.push("/employee");
      console.log(body.user);
      return body.user;
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
