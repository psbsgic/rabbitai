import { JsonObject, Locale } from '@rabbitai-ui/core';


export type User = {
  createdOn: string;
  email: string;
  firstName: string;
  isActive: boolean;
  lastName: string;
  userId: number;
  username: string;
};

export interface UserWithPermissionsAndRoles extends User {
  permissions: {
    database_access?: string[];
    datasource_access?: string[];
  };
  roles: Record<string, [string, string][]>;
}

export type Dashboard = {
  dttm: number;
  id: number;
  url: string;
  title: string;
  creator?: string;
  creator_url?: string;
};

export interface CommonBootstrapData {
  flash_messages: string[][];
  conf: JsonObject;
  locale: Locale;
  feature_flags: Record<string, boolean>;
}
