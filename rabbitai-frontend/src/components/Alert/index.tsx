import React, { PropsWithChildren } from 'react';
import {
  Alert as AntdAlert,
  AlertProps as AntdAlertProps,
} from 'src/common/components';
import { useTheme } from '@superset-ui/core';
import Icons from 'src/components/Icons';

export type AlertProps = PropsWithChildren<
  AntdAlertProps & { roomBelow?: boolean }
>;

export default function Alert(props: AlertProps) {
  const {
    type = 'info',
    description,
    showIcon = true,
    closable = true,
    roomBelow = false,
    children,
  } = props;

  const theme = useTheme();
  const { colors, typography, gridUnit } = theme;
  const { alert, error, info, success } = colors;

  let baseColor = info;
  let AlertIcon = Icons.InfoSolid;
  if (type === 'error') {
    baseColor = error;
    AlertIcon = Icons.ErrorSolid;
  } else if (type === 'warning') {
    baseColor = alert;
    AlertIcon = Icons.AlertSolid;
  } else if (type === 'success') {
    baseColor = success;
    AlertIcon = Icons.CircleCheckSolid;
  }

  return (
    <AntdAlert
      role="alert"
      showIcon={showIcon}
      icon={<AlertIcon aria-label={`${type} icon`} />}
      closeText={closable && <Icons.XSmall aria-label="close icon" />}
      css={{
        marginBottom: roomBelow ? gridUnit * 4 : 0,
        padding: `${gridUnit * 2}px ${gridUnit * 3}px`,
        alignItems: 'flex-start',
        border: 0,
        backgroundColor: baseColor.light2,
        '& .ant-alert-icon': {
          marginRight: gridUnit * 2,
        },
        '& .ant-alert-message': {
          color: baseColor.dark2,
          fontSize: typography.sizes.m,
          fontWeight: description
            ? typography.weights.bold
            : typography.weights.normal,
        },
        '& .ant-alert-description': {
          color: baseColor.dark2,
          fontSize: typography.sizes.m,
        },
      }}
      {...props}
    >
      {children}
    </AntdAlert>
  );
}
