
type DatabaseUser = {
  first_name: string;
  last_name: string;
};

export type DatabaseObject = {
  // Connection + general
  id?: number;
  database_name: string;
  sqlalchemy_uri?: string;
  backend?: string;
  created_by?: null | DatabaseUser;
  changed_on_delta_humanized?: string;
  changed_on?: string;
  parameters?: { database_name?: string; engine?: string };
  configuration_method: CONFIGURATION_METHOD;

  // Performance
  cache_timeout?: string;
  allow_run_async?: boolean;

  // SQL Lab
  expose_in_sqllab?: boolean;
  allow_ctas?: boolean;
  allow_cvas?: boolean;
  allow_dml?: boolean;
  allow_multi_schema_metadata_fetch?: boolean;
  force_ctas_schema?: string;

  // Security
  encrypted_extra?: string;
  server_cert?: string;

  // Extra
  impersonate_user?: boolean;
  allow_csv_upload?: boolean;
  extra?: string;
};

export type DatabaseForm = {
  engine: string;
  name: string;
  parameters: {
    properties: {
      database: {
        description: string;
        type: string;
      };
      host: {
        description: string;
        type: string;
      };
      password: {
        description: string;
        nullable: boolean;
        type: string;
      };
      port: {
        description: string;
        format: string;
        type: string;
      };
      query: {
        additionalProperties: {};
        description: string;
        type: string;
      };
      username: {
        description: string;
        nullable: boolean;
        type: string;
      };
    };
    required: string[];
    type: string;
  };
  preferred: boolean;
  sqlalchemy_uri_placeholder: string;
};

// the values should align with the database
// model enum in rabbitai/rabbitai/models/core.py
export enum CONFIGURATION_METHOD {
  SQLALCHEMY_URI = 'sqlalchemy_form',
  DYNAMIC_FORM = 'dynamic_form',
}
