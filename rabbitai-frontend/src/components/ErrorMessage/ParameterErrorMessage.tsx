
import React from 'react';
import { t, tn } from '@rabbitai-ui/core';
import levenshtein from 'js-levenshtein';

import { ErrorMessageComponentProps } from './types';
import IssueCode from './IssueCode';
import ErrorAlert from './ErrorAlert';

interface ParameterErrorExtra {
  undefined_parameters?: string[];
  template_parameters?: object;
  issue_codes: {
    code: number;
    message: string;
  }[];
}

const maxDistanceForSuggestion = 2;
const findMatches = (undefinedParameters: string[], templateKeys: string[]) => {
  const matches: { [undefinedParameter: string]: string[] } = {};
  undefinedParameters.forEach(undefinedParameter => {
    templateKeys.forEach(templateKey => {
      if (
        levenshtein(undefinedParameter, templateKey) <= maxDistanceForSuggestion
      ) {
        if (!matches[undefinedParameter]) {
          matches[undefinedParameter] = [];
        }
        matches[undefinedParameter].push(`"${templateKey}"`);
      }
    });
  });
  return matches;
};

function ParameterErrorMessage({
  error,
  source = 'sqllab',
}: ErrorMessageComponentProps<ParameterErrorExtra>) {
  const { extra, level, message } = error;

  const triggerMessage = tn(
    'This was triggered by:',
    'This may be triggered by:',
    extra.issue_codes.length,
  );

  const matches = findMatches(
    extra.undefined_parameters || [],
    Object.keys(extra.template_parameters || {}),
  );

  const body = (
    <>
      <p>
        {Object.keys(matches).length > 0 && (
          <>
            <p>{t('Did you mean:')}</p>
            <ul>
              {Object.entries(matches).map(
                ([undefinedParameter, templateKeys]) => (
                  <li>
                    {tn(
                      '%(suggestion)s instead of "%(undefinedParameter)s?"',
                      '%(firstSuggestions)s or %(lastSuggestion)s instead of "%(undefinedParameter)s"?',
                      templateKeys.length,
                      {
                        suggestion: templateKeys.join(', '),
                        firstSuggestions: templateKeys.slice(0, -1).join(', '),
                        lastSuggestion: templateKeys[templateKeys.length - 1],
                        undefinedParameter,
                      },
                    )}
                  </li>
                ),
              )}
            </ul>
            <br />
          </>
        )}
        {triggerMessage}
        <br />
        {extra.issue_codes
          .map<React.ReactNode>(issueCode => <IssueCode {...issueCode} />)
          .reduce((prev, curr) => [prev, <br />, curr])}
      </p>
    </>
  );

  const copyText = `${message}
${triggerMessage}
${extra.issue_codes.map(issueCode => issueCode.message).join('\n')}`;

  return (
    <ErrorAlert
      title={t('Parameter error')}
      subtitle={message}
      level={level}
      source={source}
      copyText={copyText}
      body={body}
    />
  );
}

export default ParameterErrorMessage;
