"use client";
import { AuthProvider } from "@/state/authContext";
import { CacheProvider } from "@chakra-ui/next-js";
import { ChakraProvider } from "@chakra-ui/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <CacheProvider>
      <ChakraProvider>
        <AuthProvider>{children}</AuthProvider>
      </ChakraProvider>
    </CacheProvider>
  );
}
