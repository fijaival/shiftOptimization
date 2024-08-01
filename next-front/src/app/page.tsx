"use client";

import Link from "next/link";
import { Flex, Text } from "@chakra-ui/react";

export default function Home() {
  return (
    <>
      <Flex height="100vh" alignItems="center" justifyContent="center">
        <Link href="/login">
          <Text fontSize="30px">login</Text>
        </Link>
      </Flex>
    </>
  );
}
