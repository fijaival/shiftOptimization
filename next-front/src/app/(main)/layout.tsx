import { Header } from "@/features/common/Header";
import { Box } from "@chakra-ui/react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Header />
      <Box display="flex" justifyContent="center" h="40" pt="16">
        {children}
      </Box>
    </>
  );
}
