import { t, supersetTheme, useTheme } from '@superset-ui/core';
import React from 'react';
import { Tooltip } from 'src/components/Tooltip';
import Icons from 'src/components/Icons';
import { AlertState } from '../types';

function getStatusColor(
  status: string,
  isReportEnabled: boolean,
  theme: typeof supersetTheme,
) {
  switch (status) {
    case AlertState.working:
      return theme.colors.primary.base;
    case AlertState.error:
      return theme.colors.error.base;
    case AlertState.success:
      return isReportEnabled
        ? theme.colors.success.base
        : theme.colors.alert.base;
    case AlertState.noop:
      return theme.colors.success.base;
    case AlertState.grace:
      return theme.colors.alert.base;
    default:
      return theme.colors.grayscale.base;
  }
}

export default function AlertStatusIcon({
  state,
  isReportEnabled = false,
}: {
  state: string;
  isReportEnabled: boolean;
}) {
  const theme = useTheme();
  const lastStateConfig = {
    icon: Icons.Check,
    label: '',
    status: '',
  };
  switch (state) {
    case AlertState.success:
      lastStateConfig.icon = isReportEnabled
        ? Icons.Check
        : Icons.AlertSolidSmall;
      lastStateConfig.label = isReportEnabled
        ? t('Report sent')
        : t('Alert triggered, notification sent');
      lastStateConfig.status = AlertState.success;
      break;
    case AlertState.working:
      lastStateConfig.icon = Icons.Running;
      lastStateConfig.label = isReportEnabled
        ? t('Report sending')
        : t('Alert running');
      lastStateConfig.status = AlertState.working;
      break;
    case AlertState.error:
      lastStateConfig.icon = Icons.XSmall;
      lastStateConfig.label = isReportEnabled
        ? t('Report failed')
        : t('Alert failed');
      lastStateConfig.status = AlertState.error;
      break;
    case AlertState.noop:
      lastStateConfig.icon = Icons.Check;
      lastStateConfig.label = t('Nothing triggered');
      lastStateConfig.status = AlertState.noop;
      break;
    case AlertState.grace:
      lastStateConfig.icon = Icons.AlertSolidSmall;
      lastStateConfig.label = t('Alert Triggered, In Grace Period');
      lastStateConfig.status = AlertState.grace;
      break;
    default:
      lastStateConfig.icon = Icons.Check;
      lastStateConfig.label = t('Nothing triggered');
      lastStateConfig.status = AlertState.noop;
  }
  const Icon = lastStateConfig.icon;
  return (
    <Tooltip title={lastStateConfig.label} placement="bottomLeft">
      <Icon
        iconColor={getStatusColor(
          lastStateConfig.status,
          isReportEnabled,
          theme,
        )}
      />
    </Tooltip>
  );
}
