"use client";
import { useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { useRouter } from "next/navigation";
import {
  Button,
  Flex,
  FormLabel,
  Heading,
  Input,
  FormControl,
} from "@chakra-ui/react";
import { handleLogin } from "../hooks";
import { LoginFormInputs } from "../type";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

export function UserLogin() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting, isValid },
  } = useForm<LoginFormInputs>();
  const router = useRouter();

  const onSubmit: SubmitHandler<LoginFormInputs> = async (
    data: LoginFormInputs
  ) => {
    const error: string | null = await handleLogin(data, router);
    if (error) {
      setErrorMessage(error);
    }
  };

  return (
    <Flex height="100vh" alignItems="center" justifyContent="center">
      <Flex direction="column" background="gray.100" padding={12} rounded={6}>
        <Heading mb={6}>ログイン</Heading>
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
        <form onSubmit={handleSubmit(onSubmit)}>
          <FormControl isInvalid={Boolean(errors.username)}>
            <FormLabel htmlFor="username">ユーザー名</FormLabel>
            <Input
              id="username"
              placeholder="username"
              {...register("username", {
                required: "ユーザ名を入力してください",
              })}
            />
            {errors.username && (
              <p style={{ color: "red" }}>{errors.username.message}</p>
            )}
          </FormControl>

          <FormControl isInvalid={Boolean(errors.password)}>
            <FormLabel htmlFor="password">パスワード</FormLabel>
            <Input
              id="password"
              placeholder="password"
              {...register("password", {
                required: "パスワードを入力してください",
              })}
            />
            {errors.password && (
              <p style={{ color: "red" }}>{errors.password.message}</p>
            )}
          </FormControl>

          <Button
            type="submit"
            colorScheme="teal"
            isLoading={isSubmitting}
            my={6}
            isDisabled={!isValid || isSubmitting}
          >
            Log in
          </Button>
        </form>
      </Flex>
    </Flex>
  );
}
