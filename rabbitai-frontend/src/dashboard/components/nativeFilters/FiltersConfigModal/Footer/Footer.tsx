import React, { FC } from 'react';
import Button, { OnClickHandler } from 'src/components/Button';
import { t } from '@superset-ui/core';
import { CancelConfirmationAlert } from './CancelConfirmationAlert';

type FooterProps = {
  onCancel: OnClickHandler;
  handleSave: OnClickHandler;
  onConfirmCancel: OnClickHandler;
  onDismiss: OnClickHandler;
  saveAlertVisible: boolean;
};

const Footer: FC<FooterProps> = ({
  onCancel,
  handleSave,
  onDismiss,
  onConfirmCancel,
  saveAlertVisible,
}) => {
  if (saveAlertVisible) {
    return (
      <CancelConfirmationAlert
        key="cancel-confirm"
        title={t('There are unsaved changes.')}
        onConfirm={onConfirmCancel}
        onDismiss={onDismiss}
      >
        {t(`Are you sure you want to cancel?`)}
      </CancelConfirmationAlert>
    );
  }

  return (
    <>
      <Button
        key="cancel"
        buttonStyle="secondary"
        data-test="native-filter-modal-cancel-button"
        onClick={onCancel}
      >
        {t('Cancel')}
      </Button>
      <Button
        key="submit"
        buttonStyle="primary"
        onClick={handleSave}
        data-test="native-filter-modal-save-button"
      >
        {t('Save')}
      </Button>
    </>
  );
};

export default Footer;
