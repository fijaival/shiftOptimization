"use client";

import { createContext, useContext, ReactNode, useState } from "react";

export type User = {
  username: string;
  user_id: number;
  facility_id: number;
  is_admin: boolean;
  created_at: string;
  facility: {
    facility_id: number;
    name: string;
  };
};

type Props = {
  children: ReactNode;
};

export const AuthContext = createContext(
  {} as {
    user: User | null;
    setUser: React.Dispatch<React.SetStateAction<User | null>>;
  }
);

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }: Props) {
  const [user, setUser] = useState<User | null>(null);
  console.log({ user, setUser }); // デバッグ用

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}
