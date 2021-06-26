

import React from 'react';
import moment from 'moment';
import { t } from '@rabbitai-ui/core';

interface Props {
  cachedTimestamp?: string;
}
export const TooltipContent: React.FC<Props> = ({ cachedTimestamp }) => {
  const cachedText = cachedTimestamp ? (
    <span>
      {t('Loaded data cached')}
      <b> {moment.utc(cachedTimestamp).fromNow()}</b>
    </span>
  ) : (
    t('Loaded from cache')
  );

  return (
    <span data-test="tooltip-content">
      {cachedText}. {t('Click to force-refresh')}
    </span>
  );
};
