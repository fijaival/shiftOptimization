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
} from "@chakra-ui/react";
import { PhoneIcon, AddIcon, WarningIcon } from "@chakra-ui/icons";

interface EmployeeCardProps {
  name: string;
  role: string;
  location: string;
  dateJoined: string;
  interests: string[];
  avatarUrl: string;
}

const EmployeeCard: React.FC<EmployeeCardProps> = ({
  name,
  role,
  location,
  dateJoined,
  interests,
  avatarUrl,
}) => {
  return (
    <Box
      p={5}
      borderWidth="1px"
      borderRadius="lg"
      boxShadow="sm"
      backgroundColor="white"
      maxW="md"
      mx="auto"
    >
      <HStack spacing={4}>
        <Avatar src={avatarUrl} size="lg" />
        <VStack align="start" spacing={1}>
          <Text fontWeight="bold" fontSize="lg">
            {name}
          </Text>
          <Text color="gray.500">{role}</Text>
          <HStack spacing={2} alignItems="center">
            <PhoneIcon />
            <Text color="gray.500" fontSize="sm">
              {location}
            </Text>
          </HStack>
          <HStack spacing={2} alignItems="center">
            <PhoneIcon />
            <Text color="gray.500" fontSize="sm">
              {dateJoined}
            </Text>
          </HStack>
        </VStack>
        <Button variant="ghost" colorScheme="blue" size="sm" alignSelf="start">
          <PhoneIcon />
          Edit
        </Button>
      </HStack>

      <Text mt={4} fontWeight="bold">
        Interests
      </Text>
      <HStack spacing={2} mt={2}>
        {interests.map((interest) => (
          <Badge key={interest} colorScheme="blue">
            {interest}
          </Badge>
        ))}
      </HStack>
    </Box>
  );
};

export default EmployeeCard;
