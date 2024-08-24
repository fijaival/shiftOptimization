export type LoginFormInputs = {
  username: string;
  password: string;
};

type FacilityType = {
  facilityId: number;
  name: string;
};

export type UserType = {
  createdAt: string;
  facility: FacilityType;
  facilityId: number;
  isAdmin: boolean;
  updatedAt: string;
  userId: number;
  username: string;
};
