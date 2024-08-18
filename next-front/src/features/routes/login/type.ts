export type LoginFormInputs = {
  username: string;
  password: string;
};

type FacilityType = {
  facility_id: number;
  name: string;
};

export type UserType = {
  created_at: string;
  facility: FacilityType;
  facility_id: number;
  is_admin: boolean;
  updated_at: string;
  user_id: number;
  username: string;
};
