import React from 'react';
import { t, tn } from '@superset-ui/core';

import { ErrorMessageComponentProps } from './types';
import IssueCode from './IssueCode';
import ErrorAlert from './ErrorAlert';

interface DatabaseErrorExtra {
  owners?: string[];
  issue_codes: {
    code: number;
    message: string;
  }[];
  engine_name: string | null;
}

function DatabaseErrorMessage({
  error,
  source = 'dashboard',
  subtitle,
}: ErrorMessageComponentProps<DatabaseErrorExtra>) {
  const { extra, level, message } = error;

  const isVisualization = ['dashboard', 'explore'].includes(source);

  const body = extra && (
    <>
      <p>
        {t('This may be triggered by:')}
        <br />
        {extra.issue_codes
          .map<React.ReactNode>(issueCode => (
            <IssueCode {...issueCode} key={issueCode.code} />
          ))
          .reduce((prev, curr) => [prev, <br />, curr])}
      </p>
      {isVisualization && extra.owners && (
        <>
          <br />
          <p>
            {tn(
              'Please reach out to the Chart Owner for assistance.',
              'Please reach out to the Chart Owners for assistance.',
              extra.owners.length,
            )}
          </p>
          <p>
            {tn(
              'Chart Owner: %s',
              'Chart Owners: %s',
              extra.owners.length,
              extra.owners.join(', '),
            )}
          </p>
        </>
      )}
    </>
  );

  const copyText =
    extra && extra.issue_codes
      ? `${message}
${t('This may be triggered by:')}
${extra.issue_codes.map(issueCode => issueCode.message).join('\n')}`
      : message;

  return (
    <ErrorAlert
      title={t('%s Error', (extra && extra.engine_name) || t('DB engine'))}
      subtitle={subtitle}
      level={level}
      source={source}
      copyText={copyText}
      body={body}
    />
  );
}

export default DatabaseErrorMessage;
