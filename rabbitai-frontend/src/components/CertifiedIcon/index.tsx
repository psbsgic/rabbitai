
import React from 'react';
import { t, rabbitaiTheme } from '@rabbitai-ui/core';
import Icon from 'src/components/Icon';
import { Tooltip } from 'src/components/Tooltip';

export interface CertifiedIconProps {
  certifiedBy?: string;
  details?: string;
  size?: number;
}

function CertifiedIcon({
  certifiedBy,
  details,
  size = 24,
}: CertifiedIconProps) {
  return (
    <Tooltip
      id="certified-details-tooltip"
      title={
        <>
          {certifiedBy && (
            <div>
              <strong>{t('Certified by %s', certifiedBy)}</strong>
            </div>
          )}
          <div>{details}</div>
        </>
      }
    >
      <Icon
        color={rabbitaiTheme.colors.primary.base}
        height={size}
        width={size}
        name="certified"
      />
    </Tooltip>
  );
}

export default CertifiedIcon;
