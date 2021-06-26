
import React from 'react';
import { t } from '@rabbitai-ui/core';

import getErrorMessageComponentRegistry from './getErrorMessageComponentRegistry';
import { RabbitaiError, ErrorSource } from './types';
import ErrorAlert from './ErrorAlert';

const DEFAULT_TITLE = t('Unexpected error');

type Props = {
  title?: string;
  error?: RabbitaiError;
  link?: string;
  subtitle?: React.ReactNode;
  copyText?: string;
  stackTrace?: string;
  source?: ErrorSource;
};

export default function ErrorMessageWithStackTrace({
  title = DEFAULT_TITLE,
  error,
  subtitle,
  copyText,
  link,
  stackTrace,
  source,
}: Props) {
  // Check if a custom error message component was registered for this message
  if (error) {
    const ErrorMessageComponent = getErrorMessageComponentRegistry().get(
      error.error_type,
    );
    if (ErrorMessageComponent) {
      return <ErrorMessageComponent error={error} source={source} />;
    }
  }

  return (
    <ErrorAlert
      level="warning"
      title={title}
      subtitle={subtitle}
      copyText={copyText}
      source={source}
      body={
        link || stackTrace ? (
          <>
            {link && (
              <a href={link} target="_blank" rel="noopener noreferrer">
                (Request Access)
              </a>
            )}
            <br />
            {stackTrace && <pre>{stackTrace}</pre>}
          </>
        ) : undefined
      }
    />
  );
}
