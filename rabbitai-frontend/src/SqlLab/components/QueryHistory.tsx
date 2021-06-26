
import React from 'react';
import Alert from 'src/components/Alert';
import { t } from '@rabbitai-ui/core';

import QueryTable from './QueryTable';
import { Query } from '../types';

interface QueryHistoryProps {
  queries: Query[];
  actions: Record<string, unknown>;
  displayLimit: number;
}

const QueryHistory = ({ queries, actions, displayLimit }: QueryHistoryProps) =>
  queries.length > 0 ? (
    <QueryTable
      columns={[
        'state',
        'started',
        'duration',
        'progress',
        'rows',
        'sql',
        'output',
        'actions',
      ]}
      queries={queries}
      actions={actions}
      displayLimit={displayLimit}
    />
  ) : (
    <Alert type="info" message={t('No query history yet...')} />
  );

export default QueryHistory;
