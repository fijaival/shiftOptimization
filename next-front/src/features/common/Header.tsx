import { Box, Container, Flex, Heading } from "@chakra-ui/react";
import Link from "next/link";
import { FC } from "react";

export const Header: FC = () => {
  return (
    <Box
      bgColor="orange.300"
      sx={{ position: "fixed", width: "100%", zIndex: 999 }}
    >
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
          <Box>
            <Link href="/requests">シフト希望</Link>
            <Link href="/employee">従業員一覧</Link>
          </Box>
        </Flex>
      </Container>
    </Box>
  );
};
