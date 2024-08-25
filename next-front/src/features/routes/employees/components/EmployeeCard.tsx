import React from "react";
import {
  Box,
  Avatar,
  Text,
  Badge,
  HStack,
  VStack,
  Icon,
  Button,
  Wrap,
} from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";

interface EmployeeCardProps {
  name: string;
  role: string;
  dependencies: string[];
  qualifications: string[];
  constraints: string[];
  avatarUrl: string;
}

const EmployeeCard: React.FC<EmployeeCardProps> = ({
  name,
  role,
  dependencies,
  qualifications,
  constraints,
  avatarUrl,
}) => {
  const handleCardClick = () => {
    alert(`${name}のカードがタッチされました！`);
  };
  return (
    <Box
      p={5}
      borderWidth="1px"
      borderRadius="lg"
      boxShadow="sm"
      backgroundColor="white"
      maxW="md"
      onClick={handleCardClick}
      cursor="pointer"
      _hover={{ backgroundColor: "gray.50", boxShadow: "md" }}
    >
      <HStack spacing={4} justifyContent="space-between">
        <HStack spacing={4}>
          <Avatar size="lg" />
          <VStack align="start" spacing={1}>
            <Text fontWeight="bold" fontSize="lg">
              {name}
            </Text>
          </VStack>
          <Text color="gray.500">{role}</Text>
        </HStack>
        <Button variant="ghost" colorScheme="blue" size="sm" alignSelf="start">
          <DeleteIcon color="red.500" />
        </Button>
      </HStack>
      <Text mt={4} fontWeight="bold">
        qualifications
      </Text>
      <Wrap spacing={2} mt={2}>
        {qualifications.map((interest) => (
          <Badge key={interest} colorScheme="blue">
            {interest}
          </Badge>
        ))}
      </Wrap>

      <Text mt={4} fontWeight="bold">
        constraints
      </Text>
      <Wrap spacing={2} mt={2}>
        {constraints.map((constraint) => (
          <Badge key={constraint} colorScheme="blue">
            {constraint}
          </Badge>
        ))}
      </Wrap>
      <Text mt={4} fontWeight="bold">
        dependencies
      </Text>
      <Wrap spacing={2} mt={2}>
        {dependencies.map((dep) => (
          <Badge key={dep} colorScheme="blue">
            {dep}
          </Badge>
        ))}
      </Wrap>
    </Box>
  );
};

export default EmployeeCard;
