import { RabbitaiClient, JsonResponse } from '@rabbitai-ui/core';
import rison from 'rison';

export const getByUser = async (userId: number) => {
  const queryParams = rison.encode({
    filters: [
      {
        col: 'owners',
        opr: 'rel_m_m',
        value: userId,
      },
    ],
    order_column: 'changed_on_delta_humanized',
    order_direction: 'desc',
  });
  const endpoint = `/api/v1/dataset?q=${queryParams}`;
  const data: JsonResponse = await RabbitaiClient.get({
    endpoint,
  });
  return data.json.result;
};

export const put = async (
  datasetId: number,
  dbId: number,
  sql: string,
  columns: Array<Record<string, any>>,
  overrideColumns: boolean,
) => {
  const endpoint = `api/v1/dataset/${datasetId}?override_columns=${overrideColumns}`;
  const headers = { 'Content-Type': 'application/json' };
  const body = JSON.stringify({
    sql,
    columns,
    database_id: dbId,
  });

  const data: JsonResponse = await RabbitaiClient.put({
    endpoint,
    headers,
    body,
  });
  return data.json.result;
};
