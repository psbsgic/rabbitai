import Owner from 'src/types/Owner';

type user = {
  id: number;
  first_name: string;
  last_name: string;
};
export type ChartObject = {
  id: number;
  slice_name: string;
  viz_type: string;
};

export type DashboardObject = {
  dashboard_title: string;
  id: number;
};

export type DatabaseObject = {
  database_name: string;
  id: number;
};

export type Recipient = {
  recipient_config_json: {
    target: string;
  };
  type: string;
};

export type MetaObject = {
  id?: number;
  label?: string;
  value?: number | string;
};

export type Operator = '<' | '>' | '<=' | '>=' | '==' | '!=' | 'not null';

export type AlertObject = {
  active?: boolean;
  chart?: MetaObject;
  changed_by?: user;
  changed_on_delta_humanized?: string;
  created_by?: user;
  created_on?: string;
  crontab?: string;
  dashboard?: MetaObject;
  database?: MetaObject;
  description?: string;
  grace_period?: number;
  id: number;
  last_eval_dttm?: number;
  last_state?: 'Success' | 'Working' | 'Error' | 'Not triggered' | 'On Grace';
  log_retention?: number;
  name?: string;
  owners?: Array<Owner | MetaObject>;
  sql?: string;
  timezone?: string;
  recipients?: Array<Recipient>;
  report_format?: 'PNG' | 'CSV' | 'TEXT';
  type?: string;
  validator_config_json?: {
    op?: Operator;
    threshold?: number;
  };
  validator_type?: string;
  working_timeout?: number;
};

export type LogObject = {
  end_dttm: string;
  error_message: string;
  id: number;
  scheduled_dttm: string;
  start_dttm: string;
  state: string;
  value: string;
  uuid: string;
};

export enum AlertState {
  success = 'Success',
  working = 'Working',
  error = 'Error',
  noop = 'Not triggered',
  grace = 'On Grace',
}

export enum RecipientIconName {
  email = 'Email',
  slack = 'Slack',
}
