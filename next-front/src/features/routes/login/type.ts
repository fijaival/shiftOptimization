export type LoginFormInputs = {
  username: string;
  password: string;
};

export type LoginResponse = {
  redirected: boolean;
  url: string;
  status: number;
  statusText: string;
};
