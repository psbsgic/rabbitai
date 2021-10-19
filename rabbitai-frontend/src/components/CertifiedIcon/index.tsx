import React from 'react';
import { t, supersetTheme } from '@superset-ui/core';
import Icons from 'src/components/Icons';
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
      <Icons.Certified
        iconColor={supersetTheme.colors.primary.base}
        height={size}
        width={size}
      />
    </Tooltip>
  );
}

export default CertifiedIcon;
