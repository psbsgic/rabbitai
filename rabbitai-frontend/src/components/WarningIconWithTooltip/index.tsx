
import React from 'react';
import { useTheme, SafeMarkdown } from '@rabbitai-ui/core';
import Icons from 'src/components/Icons';
import { Tooltip } from 'src/components/Tooltip';

export interface WarningIconWithTooltipProps {
  warningMarkdown: string;
  size?: number;
}

function WarningIconWithTooltip({
  warningMarkdown,
}: WarningIconWithTooltipProps) {
  const theme = useTheme();
  return (
    <Tooltip
      id="warning-tooltip"
      title={<SafeMarkdown source={warningMarkdown} />}
    >
      <Icons.AlertSolid iconColor={theme.colors.alert.base} />
    </Tooltip>
  );
}

export default WarningIconWithTooltip;
