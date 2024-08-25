import { Box, Flex, Container, Heading } from "@chakra-ui/react";
import Link from "next/link";
import { FC } from "react";

export const Header: FC = () => {
  return (
    <Box px={4} bgColor="orange.300">
      <Container maxW="container.lg">
        <Flex
          as="header"
          py="4"
          justifyContent="space-between"
          alignItems="center"
        >
          <Link href="/dashboard" passHref>
            <Heading as="h1" fontSize="2xl" cursor="pointer">
              シフト自動生成
            </Heading>
          </Link>
          <Link href="/requests">シフト希望</Link>
        </Flex>
      </Container>
    </Box>
  );
};
