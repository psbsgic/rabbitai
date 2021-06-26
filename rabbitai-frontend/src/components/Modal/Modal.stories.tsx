
import React from 'react';
import Modal, { ModalProps } from '.';

export default {
  title: 'Modal',
  component: Modal,
};

export const InteractiveModal = (props: ModalProps) => (
  <Modal {...props}>Hi</Modal>
);

InteractiveModal.args = {
  disablePrimaryButton: false,
  primaryButtonName: 'Danger',
  primaryButtonType: 'danger',
  show: true,
  title: "I'm a modal!",
};

InteractiveModal.argTypes = {
  onHandledPrimaryAction: { action: 'onHandledPrimaryAction' },
  onHide: { action: 'onHide' },
};

InteractiveModal.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
