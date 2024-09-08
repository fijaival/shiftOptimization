import humps from "humps";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { login } from "./endpoint";
import { LoginFormInputs, UserType } from "./type";

export const handleLogin = async (
  data: LoginFormInputs,
  router: AppRouterInstance
): Promise<string | UserType> => {
  try {
    const response: Response = await login(data.username, data.password);
    if (response.ok) {
      const body = await response.json();
      router.push("/employee");
      return humps.camelizeKeys(body.user) as UserType;
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
