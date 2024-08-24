"use client";

import { createContext, useContext, ReactNode, useState } from "react";

export type User = {
  username: string;
  userId: number;
  facilityId: number;
  isAdmin: boolean;
  createdAt: string;
  facility: {
    facilityId: number;
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
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}
