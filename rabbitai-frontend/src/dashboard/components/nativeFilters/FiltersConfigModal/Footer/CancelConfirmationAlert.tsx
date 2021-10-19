import React from 'react';
import { t } from '@superset-ui/core';
import Alert from 'src/components/Alert';
import Button, { OnClickHandler } from 'src/components/Button';

export interface ConfirmationAlertProps {
  title: string;
  children: React.ReactNode;
  onConfirm: OnClickHandler;
  onDismiss: OnClickHandler;
}

export function CancelConfirmationAlert({
  title,
  onConfirm,
  onDismiss,
  children,
}: ConfirmationAlertProps) {
  return (
    <Alert
      closable={false}
      type="warning"
      key="alert"
      message={title}
      css={{
        textAlign: 'left',
        '& .ant-alert-action': { alignSelf: 'center' },
      }}
      description={children}
      action={
        <div css={{ display: 'flex' }}>
          <Button
            key="cancel"
            buttonSize="small"
            buttonStyle="secondary"
            onClick={onDismiss}
          >
            {t('Keep editing')}
          </Button>
          <Button
            key="submit"
            buttonSize="small"
            buttonStyle="primary"
            onClick={onConfirm}
          >
            {t('Yes, cancel')}
          </Button>
        </div>
      }
    />
  );
}
