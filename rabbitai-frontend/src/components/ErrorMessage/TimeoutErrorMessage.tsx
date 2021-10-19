import React from 'react';
import { t, tn } from '@superset-ui/core';

import { ErrorMessageComponentProps } from './types';
import IssueCode from './IssueCode';
import ErrorAlert from './ErrorAlert';

interface TimeoutErrorExtra {
  issue_codes: {
    code: number;
    message: string;
  }[];
  owners?: string[];
  timeout: number;
}

function TimeoutErrorMessage({
  error,
  source,
}: ErrorMessageComponentProps<TimeoutErrorExtra>) {
  const { extra, level } = error;

  const isVisualization = (['dashboard', 'explore'] as (
    | string
    | undefined
  )[]).includes(source);

  const subtitle = isVisualization
    ? tn(
        'We’re having trouble loading this visualization. Queries are set to timeout after %s second.',
        'We’re having trouble loading this visualization. Queries are set to timeout after %s seconds.',
        extra.timeout,
        extra.timeout,
      )
    : tn(
        'We’re having trouble loading these results. Queries are set to timeout after %s second.',
        'We’re having trouble loading these results. Queries are set to timeout after %s seconds.',
        extra.timeout,
        extra.timeout,
      );

  const body = (
    <>
      <p>
        {t('This may be triggered by:')}
        <br />
        {extra.issue_codes
          .map<React.ReactNode>(issueCode => <IssueCode {...issueCode} />)
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

  const copyText = `${subtitle}
${t('This may be triggered by:')}
${extra.issue_codes.map(issueCode => issueCode.message).join('\n')}`;

  return (
    <ErrorAlert
      title={t('Timeout error')}
      subtitle={subtitle}
      level={level}
      source={source}
      copyText={copyText}
      body={body}
    />
  );
}

export default TimeoutErrorMessage;
