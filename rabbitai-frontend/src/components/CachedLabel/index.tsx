
import React, { useState } from 'react';
import { t } from '@rabbitai-ui/core';
import Label from 'src/components/Label';
import { Tooltip } from 'src/components/Tooltip';
import { TooltipContent } from './TooltipContent';

interface Props {
  onClick?: React.MouseEventHandler<HTMLElement>;
  cachedTimestamp?: string;
  className?: string;
}

const CacheLabel: React.FC<Props> = ({
  className,
  onClick,
  cachedTimestamp,
}) => {
  const [hovered, setHovered] = useState(false);

  const labelType = hovered ? 'primary' : 'default';
  return (
    <Tooltip
      title={<TooltipContent cachedTimestamp={cachedTimestamp} />}
      id="cache-desc-tooltip"
    >
      <Label
        className={`${className}`}
        type={labelType}
        onClick={onClick}
        onMouseOver={() => setHovered(true)}
        onMouseOut={() => setHovered(false)}
      >
        {t('cached')} <i className="fa fa-refresh" />
      </Label>
    </Tooltip>
  );
};

export default CacheLabel;
